# Split.io Feature Flag Setup

This document explains how to set up and use Split.io feature flags in Quantum Bank.

## Configuration

### Server-Side SDK Key

The server-side API key is loaded from environment variables using a `.env` file.

**Setup:**
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your server-side API key:
   ```
   SPLIT_API_KEY=your_server_side_api_key_here
   ```

3. The `.env` file is already in `.gitignore` and will NOT be committed to git.

**Important:** Never commit your `.env` file! The server-side key is a secret.

### Client-Side SDK Key

The client-side SDK key is configured in `static/js/split-client.js`. This key is safe to expose in the browser and enables real-time feature flag updates without page refresh.

## Feature Flags

### home_page_variant
Controls which version of the home page is displayed to users.

**Split Name:** `home_page_variant`

This one flag drives **both** the home and pricing pages (see [TECHSUMMARY.md](TECHSUMMARY.md#feature-flag-implementation) — intentionally simplified for the demo).

**Treatments:**
- `new_home` - Modern theme (`templates/home.html` + `templates/pricing_v2.html`)
- `old_home` - Legacy theme (`templates/old_home.html` + `templates/pricing_old.html`)
- `dev_home` - Developer-focused theme (`templates/home_v3.html` + `templates/pricing_v3.html`)
- `control` - Default fallback when the flag is unconfigured or the SDK isn't ready; resolves to `new_home`

**User Key:** A random per-browser id generated on first load and cached in
`sessionStorage` (`split_user_key`). For consistent A/B targeting in production,
replace it with the authenticated user id.

## Split.io Dashboard Setup

1. Go to https://app.split.io
2. Create a new Split called `home_page_variant`
3. Add the treatments you want to serve:
   - `new_home`
   - `old_home`
   - `dev_home`
4. Set targeting rules (e.g., 50/50 split, or based on user attributes)
5. **Turn the split ON**
6. Save and deploy

## Real-Time Flag Updates (demo mode)

In **demo mode**, the client-side SDK switches the visible variant **instantly,
without any page reload or confirmation dialog**:

- When you change `home_page_variant` in the Split.io dashboard, the browser's
  SDK fires an `SDK_UPDATE` event.
- The handler re-reads the treatment and, if it changed, swaps the active
  variant in place via CSS — no refresh.

**How it works:**
1. Server-side SDK determines the initial treatment on page load.
2. Client-side SDK listens for `SDK_UPDATE` events in real time.
3. On a treatment change, `showVariant()` toggles the new variant into view.
4. The change is visible immediately; no refresh required.

**Note:** The client-side SDK uses `sessionStorage` to keep the same user key
across page loads. (In **traditional mode** — the default — the server renders a
single variant and you refresh to pick up a flag change.)

## Testing

### Testing Server-Side Feature Flags

```bash
# Run the app (see the README quick start for venv setup)
python app.py

# Visit http://localhost:5001
# Check the console output for Split.io treatment decisions
```

### Testing Real-Time Updates (demo mode)

1. Load the home page in demo mode (`/demo`, or `DEMO_MODE=on`) at http://localhost:5001
2. Open browser DevTools Console (F12)
3. You should see the initial treatment logged for `home_page_variant`
4. Go to the Split.io dashboard and change the treatment (e.g., switch to 100% `old_home`)
5. Watch the console — you should see an `⚡ INSTANT SWITCH!` line and the variant change on screen with no refresh

**Console messages to look for:**
- `[Split.io] New treatment for home_page_variant: X` - Treatment re-read after an SDK update
- `[Split.io] Feature flags updated from server` - New data received
- `[Split.io] ⚡ INSTANT SWITCH! Treatment changed from … to …` - Variant swapped in place

## Implementation Details

### Server-Side
- **Server initialization:** `split_config.py` - initializes the Split.io server-side SDK
- **Feature flag usage:** `api/home.py` - checks the feature flag and selects template
- **Cleanup:** Automatically destroys the client on app shutdown

### Client-Side (demo mode)
- **Client SDK:** Loaded from the Split.io CDN in the demo-mode wrapper templates (`templates/home_wrapper.html`, `templates/pricing_wrapper.html`), pinned with SRI hashes.
- **Client logic:** `static/js/split-client.js` - handles real-time flag updates and in-place variant swapping
- **User tracking:** Uses `sessionStorage` to maintain a consistent user key across page loads

## Future Feature Flags

Consider adding feature flags for:
- Transfer limits
- New dashboard widgets
- Two-factor authentication
- Dark mode theme
- Premium account features
