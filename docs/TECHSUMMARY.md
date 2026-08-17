# Quantum Bank - Technical Summary

## Overview

Quantum Bank is a Flask-based banking demo application designed to showcase Split.io feature flagging capabilities. The application demonstrates real-time A/B testing with instant variant switching without page refreshes.

**Tech Stack:**
- **Backend:** Flask 3.1.3 (Python 3.11)
- **Database:** SQLite (`quantum_bank.db`)
- **Feature Flags:** Split.io (server-side SDK v10.5.1 + client-side SDK v11.0.1)
- **Monitoring:** Prometheus metrics (`/metrics` endpoint)
- **Deployment:** Docker + Render.com
- **WSGI Server:** Gunicorn (production)

---

## Architecture Highlights

### Demo Mode vs Traditional Mode

The application supports **two modes** controlled by a **Split.io flag** `demo_mode` (with fallback to `DEMO_MODE` environment variable):

#### Demo Mode ON (Split.io flag `demo_mode=on` or `DEMO_MODE=on`)
- **Purpose:** Showcase instant flag switching for FME (Feature Management Experience) demos
- **Behavior:** Pre-loads all variants as iframes, instant switching without refresh
- **Use Case:** Live demos where you want to flip a flag and see immediate visual change
- **Trade-off:** Higher initial load time, but wow factor for demos
- **Visual Indicator:** Shows "⚡ DEMO MODE" badge in bottom-left corner when active

#### Traditional Mode OFF (Default: Split.io flag `demo_mode=off` or `DEMO_MODE=off`)
- **Purpose:** Better for AI testing tools and isolated variant testing
- **Behavior:** Server-side rendering of single variant, no pre-loading
- **Use Case:** AI test tools that need to test specific variants without iframe confusion
- **Trade-off:** Requires page refresh to see flag changes, but cleaner for testing
- **Default:** Traditional mode is the default (safer for AI testing)

**Configuration:**

**Priority Order:**
1. **URL Path `/demo`** - Forces demo mode ON (highest priority)
   - Visit `qbank.dev/demo` → Demo mode automatically enabled
   - Entry path stored in session, persists across requests
   
2. **Split.io Flag** (recommended for dynamic control)
   - Create a Split.io flag called `demo_mode`
   - Treatments: `on` (demo mode) or `off` (traditional mode)
   - Control via Split.io dashboard - no server restart needed!
   - **User Attributes:** Entry path (`entry_path`) is passed to Split.io for targeting
   - Example targeting rule: `entry_path = '/demo'` → `on`
   
3. **Environment Variable** (fallback)
```bash
# Demo mode (instant switching)
DEMO_MODE=on

# Traditional mode (server-side only)
DEMO_MODE=off
```

**Default Behavior:**
- Default is `off` (traditional mode) - safer for AI testing
- If Split.io returns `'control'` (flag not configured or SDK not ready), falls back to env var
- Console logs show exactly what's happening:
  - `[Demo Mode] 🎯 Entry path '/demo' detected -> Demo mode FORCED ON`
  - `[Demo Mode] ✅ Split.io flag = ON -> Demo mode ENABLED`
  - `[Demo Mode] ❌ Split.io flag = OFF -> Demo mode DISABLED`

**Split.io Targeting with Entry Path:**
- Entry path is passed as user attribute: `{'entry_path': '/demo'}`
- Use in Split.io targeting rules: `IF entry_path equals '/demo' THEN on`
- Helps handle slower Split.io initialization - URL path takes precedence

### Dual SDK Pattern (Non-Standard Approach)

**⚠️ IMPORTANT: This is a demo-specific implementation, not production best practice.**

The application uses a **hybrid approach** combining server-side and client-side Split.io SDKs:

1. **Server-Side SDK** (`split_config.py`):
   - Initializes Split.io factory on app startup
   - Used for treatment evaluation in both demo and traditional modes
   - Loads API key from `SPLIT_API_KEY` environment variable

2. **Client-Side SDK** (`static/js/split-client.js`):
   - Loaded from Split.io CDN in wrapper templates (demo mode only)
   - Handles **real-time flag updates** without page refresh
   - Listens for `SDK_UPDATE` events and instantly switches variants

**Why This Approach?**
- **Demo Purpose:** Enables instant visual feedback when flags change in Split.io dashboard
- **User Experience:** No page refresh required - variants switch instantly via CSS
- **Trade-off:** Pre-loads all variants as iframes (higher initial load, but instant switching)

**Production Consideration:** In production, you'd typically use server-side routing OR client-side, not both. This dual approach is optimized for demo/showcase purposes.

---

## Feature Flag Implementation

### Single Flag Controls Multiple Pages

**Flag Name:** `home_page_variant`

**Treatments:**
- `new_home` - Modern theme (default)
- `old_home` - Legacy/simple theme
- `dev_home` - Developer-focused theme

**⚠️ Non-Standard:** This single flag controls **both home and pricing pages**. In production, you'd typically have separate flags per feature/page.

**Mapping:**
```
home_page_variant = 'old_home'  → old_home.html + pricing_old.html
home_page_variant = 'new_home'  → home.html + pricing_v2.html
home_page_variant = 'dev_home'  → home_v3.html + pricing_v3.html
```

---

## Variant Switching Pattern

### Demo Mode: Wrapper Template Architecture

**When `DEMO_MODE=on` or Split.io flag `demo_mode=on`:** Both home and pricing pages use a **wrapper pattern** that pre-loads all variants:

**Home Page Flow (Demo Mode):**
```
/ → home_wrapper.html
  ├── iframe: /old-home-static → old_home.html
  ├── iframe: /new-home-static → home.html
  └── iframe: /v3-home-static → home_v3.html
```

**Pricing Page Flow (Demo Mode):**
```
/pricing → pricing_wrapper.html
  ├── iframe: /old-pricing-static → pricing_old.html
  ├── iframe: /new-pricing-static → pricing_v2.html
  └── iframe: /v3-pricing-static → pricing_v3.html
```

**How Demo Mode Works:**
1. Wrapper loads all variants as hidden iframes (`display: none`)
2. Client-side Split.io SDK evaluates treatment
3. JavaScript shows/hides iframes via CSS class toggle (`.active`)
4. When flag changes in dashboard, SDK detects update and instantly switches
5. **No page refresh required** - instant visual feedback
6. **Visual confirmation:** "⚡ DEMO MODE" badge appears in top-right corner

### Traditional Mode: Server-Side Rendering

**When `DEMO_MODE=off` or Split.io flag `demo_mode=off` (default):** Pages render single variant server-side:

**Home Page Flow (Traditional Mode):**
```
/ → api/home.py → checks Split.io → renders single template
  - old_home.html OR home.html OR home_v3.html
```

**Pricing Page Flow (Traditional Mode):**
```
/pricing → api/pricing.py → checks Split.io → renders single template
  - pricing_old.html OR pricing_v2.html OR pricing_v3.html
```

**How Traditional Mode Works:**
1. Server evaluates Split.io flag server-side
2. Renders only the selected variant template
3. No iframes, no pre-loading
4. **Requires page refresh** to see flag changes
5. **Better for AI testing tools** - cleaner DOM, no iframe confusion

**Files:**
- `templates/home_wrapper.html` - Home page wrapper (demo mode only)
- `templates/pricing_wrapper.html` - Pricing page wrapper (demo mode only)
- `static/js/split-client.js` - Client-side flag logic (demo mode only)
- `api/home_static.py` - Static route handlers for home variants (demo mode)
- `api/pricing_static.py` - Static route handlers for pricing variants (demo mode)
- `api/home.py` - Home handler (checks DEMO_MODE, routes accordingly)
- `api/pricing.py` - Pricing handler (checks DEMO_MODE, routes accordingly)

---

## Code Review

### Key Components

#### 1. Split.io Configuration (`split_config.py`)

```python
# Global singleton pattern
split_factory = None
split_client = None

def init_split():
    """Initialize Split.io client on app startup"""
    # Factory initialization with 5s timeout
    # Graceful degradation if Split.io unavailable
```

**Notes:**
- Global state management (acceptable for Flask app context)
- Graceful fallback if Split.io unavailable
- Cleanup on app shutdown via `atexit.register()`

#### 2. Route Handlers (`api/home.py`, `api/pricing.py`)

```python
def handle_home():
    """Renders wrapper template with all variants"""
    return render_template('home_wrapper.html')
```

**Design Decision:** Handlers are intentionally simple - all logic moved to client-side for instant switching.

#### 3. Client-Side SDK (`static/js/split-client.js`)

**Key Functions:**
- `showVariant(treatment)` - Handles both `.home-variant` and `.pricing-variant` elements
- `initializeSplitClient()` - Sets up SDK with session-based user key
- Listens for `SDK_UPDATE` events for real-time flag changes

**User Identification:**
```javascript
// Currently uses sessionStorage for user key
// In production, replace with actual user ID
let userKey = sessionStorage.getItem('split_user_key');
```

**⚠️ Production Note:** User key is session-based. For consistent A/B testing, use authenticated user IDs.

#### 4. Static Route Handlers (`api/home_static.py`, `api/pricing_static.py`)

Simple template renderers for iframe content. No Split.io evaluation needed since wrapper handles it.

---

## Database Schema

**SQLite Database:** `quantum_bank.db`

**Tables:**
- `users` - User accounts (id, username, email, full_name)
- `accounts` - Bank accounts (id, user_id, account_type, account_number, balance)
- `transactions` - Transaction history (id, account_id, transaction_type, amount, description)
- `cards` - Payment cards (id, account_id, card_type, card_last4, expiry_date) — synthetic demo data only; no CVV or full PAN

**Initialization:** `models.py` auto-creates sample data on first run (demo user: `demo`).

---

## Environment Variables

**Required:**
- `SPLIT_API_KEY` - Split.io server-side API key (from `.env` file)
- `SECRET_KEY` - Flask session secret key
- `PORT` - Server port (defaults to 10000, Render.com sets this)

**Client-Side Key:** Hardcoded in `static/js/split-client.js` (safe to expose):
```javascript
const SPLIT_CLIENT_KEY = '5lra47f9qtsf0dcrgcdur3k5sjhfblck0l67';
```

---

## Monitoring & Metrics

**Prometheus Integration:**
- Endpoint: `/metrics`
- Metrics:
  - `app_request_count` - Request counter (labeled by method, endpoint, status)
  - `app_request_latency_seconds` - Request latency histogram

**Implementation:** A plain Flask `/metrics` route serves output from a tiny,
dependency-free exposition module (`prometheus_minimal.py`) — no `prometheus_client`
and no `DispatcherMiddleware`. Per-request count and latency are recorded via
`before_request`/`after_request` hooks in `app.py`.

---

## Deployment

### Docker Configuration

**Dockerfile:**
- Base: `python:3.11-slim`
- Installs dependencies from `requirements.txt`
- Adds Gunicorn for production
- Exposes port 10000 (Render.com default)

**Render.com:**
- Auto-deploys from GitHub `main` branch
- Uses `render.yaml` for service configuration
- Environment variables set in Render dashboard
- **Important:** With `runtime: docker`, Render uses the Dockerfile for build/start commands
  - `buildCommand` and `startCommand` in `render.yaml` are ignored when using Docker runtime
  - All build/start logic is in `Dockerfile` instead

**Database Persistence:**
- ⚠️ **Free tier:** SQLite database resets on deploys/restarts
- For production: Consider PostgreSQL or persistent disk mount

---

## Demo Mode Visual Indicator

### Badge Display

When `DEMO_MODE=on` or Split.io flag `demo_mode=on`, a visual indicator badge appears in the bottom-left corner of the page:

**Features:**
- **Text:** "⚡ DEMO MODE" with lightning bolt icon
- **Style:** Brand color gradient (#605dba), rounded pill shape
- **Animation:** Subtle pulse effect (2s ease-in-out infinite)
- **Position:** Fixed top-right (20px from edges, responsive on mobile)
- **Z-index:** 9999 (always on top)
- **Behavior:** Non-interactive (pointer-events: none)

**Purpose:**
- Confirms instant switching mode is active
- Helps distinguish demo mode from traditional mode
- Provides visual feedback during live demos

**Implementation:**
- Badge is conditionally rendered in wrapper templates (`home_wrapper.html`, `pricing_wrapper.html`)
- Only displays when `demo_mode=True` is passed from handlers
- Styled with CSS animations for subtle attention-grabbing effect

---

## Testing & Variant Detection

### Test Identifiers

All variants include `data-testid` attributes for automated testing:

**Home Page:**
- `data-testid="home-variant-old"` - Old variant
- `data-testid="home-variant-new"` - New variant
- `data-testid="home-variant-dev"` - Dev variant
- `data-testid="nav-login"` vs `data-testid="nav-signin"` - Navigation links

**Pricing Page:**
- `data-testid="pricing-variant-old"` - Old variant
- `data-testid="pricing-variant-v2"` - V2 variant
- `data-testid="pricing-variant-v3"` - V3 variant

**Variant Differences:**
- **Old:** "Login" link, simple table layout
- **V2:** "Sign In" link, modern card design, financial products focus
- **V3:** "Login" link, developer-focused content (API calls, CLI, MCP)

---

## Known Limitations & Considerations

### 1. User Identification
- Currently uses IP address or session storage
- **Production:** Should use authenticated user IDs for consistent targeting

### 2. Single Flag for Multiple Pages
- One flag (`home_page_variant`) controls both home and pricing
- **Production:** Consider separate flags per page/feature

### 3. Pre-loaded Variants (Demo Mode Only)
- In demo mode, all variants load as iframes (higher initial load time)
- **Trade-off:** Instant switching vs. performance
- **Solution:** Use `DEMO_MODE=off` (default) or Split.io flag `demo_mode=off` for traditional server-side rendering

### 4. AI Testing Tool Compatibility
- Demo mode with iframes can confuse AI testing tools (they may navigate into iframes)
- **Solution:** Default is `DEMO_MODE=off` - perfect for AI testing! Or use Split.io flag `demo_mode=off`
- Traditional mode renders single variant, no iframes, cleaner for automation
- Console logs show: `[Demo Mode] ✅ Split.io flag = ON` or `[Demo Mode] ❌ Split.io flag = OFF`

### 5. Database Persistence
- SQLite on free tier resets on deploy
- **Production:** Use PostgreSQL or persistent storage

### 6. Error Handling
- Graceful degradation if Split.io unavailable
- Falls back to default variant (new_home)

---

## Handoff Checklist

### For New Engineers

1. **Environment Setup:**
   - Copy `.env.example` to `.env`
   - Add `SPLIT_API_KEY` from Split.io dashboard
   - Set `SECRET_KEY` for Flask sessions
   - Set `DEMO_MODE=on` for instant switching or `DEMO_MODE=off` for traditional mode (default)
   - Or use Split.io flag `demo_mode` (treatments: `on`/`off`) - no server restart needed!

2. **Split.io Configuration:**
   - Create `home_page_variant` split in Split.io dashboard
   - Add treatments: `new_home`, `old_home`, `dev_home`
   - Configure targeting rules (50/50 split, user attributes, etc.)

3. **Local Development:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py  # Runs on port 5001
   ```

4. **Testing Variants:**
   - **Demo Mode (`DEMO_MODE=on` or Split.io flag `demo_mode=on`):**
     - Visit `http://localhost:5001`
     - Change flag in Split.io dashboard
     - Verify instant switching without refresh (check browser console for logs)
     - Check server logs: `[Demo Mode] ✅ Split.io flag = ON -> Demo mode ENABLED`
   - **Traditional Mode (`DEMO_MODE=off` or Split.io flag `demo_mode=off` - default):**
     - Visit `http://localhost:5001`
     - Change flag in Split.io dashboard
     - Refresh page to see new variant (better for AI testing tools)
     - Check server logs: `[Demo Mode] ❌ Split.io flag = OFF -> Demo mode DISABLED`

5. **Adding New Variants:**
   - Create new template (e.g., `home_v4.html`)
   - Add static route handler
   - Update wrapper template with new iframe
   - Update `showVariant()` function in `split-client.js`

---

## File Structure

```
QuantumBank/
├── app.py                 # Main Flask app, routes, Prometheus setup
├── models.py              # Database models & SQLite operations
├── split_config.py        # Split.io server-side initialization
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
├── render.yaml            # Render.com deployment config
│
├── api/                   # Route handlers (modular architecture)
│   ├── home.py           # Home page handler (wrapper)
│   ├── home_static.py    # Static home variant routes
│   ├── pricing.py        # Pricing page handler (wrapper)
│   ├── pricing_static.py # Static pricing variant routes
│   ├── login.py          # Authentication
│   ├── dashboard.py      # User dashboard
│   └── ...
│
├── templates/             # Jinja2 templates
│   ├── home_wrapper.html      # Home page wrapper (all variants)
│   ├── pricing_wrapper.html  # Pricing page wrapper (all variants)
│   ├── home.html              # V2 home variant
│   ├── old_home.html          # Old home variant
│   ├── home_v3.html           # Dev home variant
│   ├── pricing_v2.html        # V2 pricing variant
│   ├── pricing_old.html       # Old pricing variant
│   ├── pricing_v3.html        # Dev pricing variant
│   └── ...
│
└── static/
    ├── js/
    │   └── split-client.js    # Client-side Split.io SDK integration
    ├── css/                    # Stylesheets
    └── images/                 # Assets
```

---

## Key Design Decisions

1. **Wrapper Pattern:** Pre-loads all variants for instant switching (demo-optimized)
2. **Dual SDK:** Server-side + client-side for real-time updates (non-standard)
3. **Single Flag:** One flag controls multiple pages (simplified for demo)
4. **Iframe Approach:** Each variant is a full-page iframe (allows independent styling)
5. **Session-Based User Key:** Uses sessionStorage (should be user ID in production)

---

## Questions for Handoff

1. **Split.io Account:** Who has access to the Split.io dashboard?
2. **API Keys:** Where are production API keys stored/managed?
3. **Database:** Is SQLite acceptable, or should we migrate to PostgreSQL?
4. **User Identification:** How should we identify users for consistent targeting?
5. **New Variants:** What's the process for adding new variants/pages?

---

## Mythos Demo — Replay Architecture (why these branches/tags exist)

The repo carries a set of **saved git refs that are deliberately retained** — do **not**
prune them as stale. They drive the *"Mythos-Ready: AI Security Remediation with Harness +
Cursor"* live demo (`.cursor/rules/mythos-demo.mdc`, scripts under `demo/mythos-v1/`).

**Design rationale.** A live demo that asks an AI agent to fix CVEs *from scratch* is risky:
the generation is **non-deterministic** — different pins, different ordering, occasional
regressions — so a recorded run can stall or fail unpredictably. Instead the demo **replays
real, previously-made commits**: faster, reliable, and still authentic (the fixes are genuine
code from genuine remediation work, just pre-recorded for determinism). The agent narrates as
if solving it live while a silent `git checkout <tag> -- <files>` stages the known-good diff.

**The story arc it preserves** (a real, instructive outcome worth capturing): the first fix
pass **resolved 12 findings but introduced 3 new ones** — a common real-world LLM remediation
failure mode (over-eager upgrades / partial fixes). A future model may one-shot it cleanly;
keeping the replay lets the demo show *both* the messy-middle and the clean recovery. The
second pass closes it out (notably: replacing `prometheus_client` rather than chasing CVEs that
were actually mis-attributed to the Prometheus *server*).

### Canonical refs (load-bearing — the demo replays from the TAGS)

| Tag | Commit | Demo act | Represents |
|-----|--------|----------|------------|
| `mythos-v1-act0` | `d57563ef` | baseline | green pipeline, 12 SCA findings unfixed |
| `mythos-v1-act1` | `dcdec421` | Act 1B | first dep-pin pass (Flask/Werkzeug/Jinja2/pytest/dotenv) |
| `mythos-v1-act2` | `fbadc81d` | Act 2 | Pygments pin + `prometheus_client` removed for local `/metrics` |
| `mythos-v1-act3` | `8b20c7e2` | Act 3 | final state (= `main` at demo time) |

The Cursor rule's `git checkout mythos-v1-act1 …` / `…-act2 …` commands depend on these **tags**.
Tags are immutable, so the demo does not depend on the branches below.

### Saved branches (mirror the tags; named in `demo/mythos-v1/RUNBOOK.md`)

| Branch | Commit | Canonical? |
|--------|--------|-----------|
| `pre-security-sca-baseline` | `d57563ef` | ✅ baseline source (RUNBOOK) |
| `security-issues-fix1` | `dcdec421` | ✅ act1 source (RUNBOOK) |
| `security-issues-fix2` | `fbadc81d` | ✅ act2 source (RUNBOOK) |
| `security-issues-original` | `d57563ef` | ⚠️ **duplicate** of `pre-security-sca-baseline`; not referenced — safe to delete |
| `security-fix-issue` | `dcdec421` | ⚠️ **duplicate** of `security-issues-fix1`; not referenced — safe to delete |

> The two ⚠️ duplicates are retained for now (documented rather than pruned). Because the demo
> replays from the **tags**, deleting them would not affect the demo — they are simply redundant
> pointers to commits already preserved by both a tag and a canonical branch.

## Additional Resources

- **Split.io Setup:** See `SPLITIO_SETUP.md`
- **Deployment:** See `RENDER_DEPLOYMENT.md`
- **Split.io Docs:** https://help.split.io/hc/en-us
- **Flask Docs:** https://flask.palletsprojects.com/

---

**Last Updated:** 2026-06-20  
**Demo Purpose:** Showcase Split.io real-time feature flagging capabilities
