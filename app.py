from flask import Flask
from prometheus_client import make_wsgi_app, Counter, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from api.hello import handle_hello
from api.home import handle_home
from api.time import handle_time
from api.about import handle_about
from api.four_o_four import handle_404

import time as t

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)

@app.route('/')
def home():
    start_time = t.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(t.time() - start_time)
    return handle_home()

@app.route('/hello')
def hello():
    start_time = t.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(t.time() - start_time)
    return handle_hello()

@app.route('/time')
def time():
    # adding new route
    start_time = t.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(t.time() - start_time)
    return handle_time()

@app.route('/about')
def about():
    start_time = t.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(t.time() - start_time)
    return handle_about()

@app.errorhandler(404)
def page_not_found(e):
    start_time = t.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(t.time() - start_time)
    return handle_404()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
