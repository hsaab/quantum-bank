from flask import render_template 

def handle_home():
    return render_template('new_home.html')
    # return "Welcome to the Home Page!"