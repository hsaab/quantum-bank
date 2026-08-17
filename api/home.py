from flask import render_template, request, session
from split_config import get_split_client
import os


def is_demo_mode(user_key=None, entry_path=None):
    """Check if demo mode is enabled (instant switching with iframes)

    Priority order:
    1. URL path (/demo) - forces demo mode ON
    2. Split.io flag 'demo_mode' with user attributes (entry_path)
    3. DEMO_MODE env var (default: 'off')

    Handles Split.io SDK initialization timing gracefully.
    """
    # Priority 1: Check if entry path contains 'demo'
    if entry_path and "demo" in entry_path.lower():
        print(
            f"[Demo Mode] 🎯 Entry path contains 'demo' ({entry_path}) -> Demo mode FORCED ON"
        )
        return True

    # Priority 2: Try Split.io flag with user attributes
    split_client = get_split_client()
    if split_client and user_key:
        try:
            # Build user attributes for Split.io targeting
            attributes = None
            if entry_path:
                attributes = {
                    "url-entry": entry_path
                }  # Match Split.io targeting rule attribute name

            if attributes:
                treatment = split_client.get_treatment(
                    user_key, "demo_mode", attributes=attributes
                )
            else:
                treatment = split_client.get_treatment(user_key, "demo_mode")
            print(
                f"[Demo Mode] Split.io flag 'demo_mode' = {treatment} (user: {user_key}, url-entry: {entry_path})"
            )

            # Explicit treatments
            if treatment in ("on", "true", "1", "yes"):
                print("[Demo Mode] ✅ Split.io flag = ON -> Demo mode ENABLED")
                return True
            elif treatment in ("off", "false", "0", "no"):
                print("[Demo Mode] ❌ Split.io flag = OFF -> Demo mode DISABLED")
                return False
            # If treatment is 'control' or unknown, Split.io isn't configured or SDK not ready
            # Fall through to env var as safe default
            elif treatment == "control":
                print(
                    "[Demo Mode] Split.io returned 'control' - flag may not be configured, using env var"
                )
            else:
                print(
                    f"[Demo Mode] Split.io returned unknown treatment '{treatment}' - using env var"
                )
        except Exception as e:
            print(f"[Demo Mode] Error getting Split.io treatment: {e} - using env var")

    # Priority 3: Fallback to environment variable
    # If entry_path contains 'demo', default to 'on', otherwise 'off' (safer for AI testing)
    default_mode = "on" if (entry_path and "demo" in entry_path.lower()) else "off"
    demo_mode = os.environ.get("DEMO_MODE", default_mode).lower()
    result = demo_mode in ("true", "1", "yes", "on")
    print(
        f"[Demo Mode] Using env var DEMO_MODE = {demo_mode} (default: '{default_mode}') -> {result}"
    )
    return result


def handle_home():
    """Handle home page - renders wrapper or single variant based on demo mode"""

    user_key = request.remote_addr or "anonymous"
    # Check session for entry path (set by /demo route), or use current path
    try:
        entry_path = session.get("entry_path", request.path)
    except Exception as e:
        print(f"[Home] Warning: Could not access session: {e}, using request.path")
        entry_path = request.path
    demo_mode_enabled = is_demo_mode(user_key, entry_path)
    print(f"[Home] DEMO_MODE check -> {demo_mode_enabled}")

    if demo_mode_enabled:
        # Demo mode: Pre-load all variants as iframes for instant switching
        print("[Home] Rendering wrapper template (DEMO MODE ON)")
        return render_template("home_wrapper.html", demo_mode=True)
    else:
        # Traditional mode: Server-side rendering of single variant
        # Better for AI testing tools that need isolated variants
        print("[Home] Rendering single template (DEMO MODE OFF - no badge)")
        split_client = get_split_client()
        template_by_treatment = {
            "old_home": "old_home.html",
            "dev_home": "home_v3.html",
        }
        template = "home.html"  # Default

        if split_client:
            user_key = request.remote_addr or "anonymous"
            treatment = split_client.get_treatment(user_key, "home_page_variant")

            template = template_by_treatment.get(treatment, "home.html")

            print(
                f"[Home] Traditional mode - User {user_key} received treatment: {treatment} -> {template}"
            )
        else:
            print(
                "[Home] Traditional mode - Split.io unavailable, using default template"
            )

        # Explicitly pass demo_mode=False to ensure badge doesn't show
        return render_template(template, demo_mode=False)
