from flask import render_template


def handle_old_pricing_static():
    """Serve the old pricing page statically (for dynamic swapping)"""
    return render_template("pricing_old.html")


def handle_new_pricing_static():
    """Serve the v2 pricing page statically (for dynamic swapping)"""
    return render_template("pricing_v2.html")


def handle_v3_pricing_static():
    """Serve the v3 developer-focused pricing page statically (for dynamic swapping)"""
    return render_template("pricing_v3.html")
