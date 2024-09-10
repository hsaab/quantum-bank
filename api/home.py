from flask import render_template 

def handle_home():
    return render_template('home.html')