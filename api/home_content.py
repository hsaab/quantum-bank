from flask import request, jsonify
from split_config import get_split_client


def handle_home_content():
    """Handle home page content API - returns just the body content for dynamic swapping"""

    # Get Split.io client
    split_client = get_split_client()

    # Default to new home page
    template = "home.html"

    if split_client:
        # Get user key (using IP address or session ID as identifier)
        user_key = request.remote_addr or "anonymous"

        # Get treatment for home_page_variant feature flag
        treatment = split_client.get_treatment(user_key, "home_page_variant")

        # Select template based on treatment
        if treatment == "old_home":
            template = "old_home.html"
        elif treatment == "new_home":
            template = "home.html"
        else:
            # Default treatment (control)
            template = "home.html"

        print(f"[API] User {user_key} received treatment: {treatment} -> {template}")
    else:
        print("[API] Split.io client not available, using default template")

    # Return JSON with template name and rendered content
    return jsonify(
        {
            "treatment": treatment if split_client else "default",
            "template": template,
            "url": "/",
        }
    )
