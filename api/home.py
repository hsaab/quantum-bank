from flask import render_template 

def handle_home():
    # adding comment to trigger tests for home
    return render_template('new_home.html')