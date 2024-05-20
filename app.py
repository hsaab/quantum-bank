from flask import Flask
from api.hello import handle_hello
from api.home import handle_home
from api.time import handle_time
from api.about import handle_about
from api.four_o_four import handle_404

app = Flask(__name__)

@app.route('/')
def home():
    return handle_home()

@app.route('/hello')
def hello():
    return handle_hello()

@app.route('/time')
def time():
    # adding new route
    return handle_time()

@app.route('/about')
def about():
    return handle_about()

@app.errorhandler(404)
def page_not_found(e):
    return handle_404()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
