from flask import render_template


def handle_old_home_static():
    """Serve the old home page statically (for dynamic swapping)"""
    return render_template("old_home.html")


def handle_new_home_static():
    """Serve the new home page statically (for dynamic swapping)"""
    return render_template("home.html")


def handle_v3_home_static():
    """Serve the v3 developer-focused home page statically (for dynamic swapping)"""
    return render_template("home_v3.html")
