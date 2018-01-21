from flask import Flask

from jaeger_client import Config
from flask_opentracing import FlaskTracer
import requests
import opentracing
from os import environ

order_url = environ['ORDER_URL']
payment_url = environ['PAYMENT_URL']

app = Flask(__name__)

def initialize_tracer():
    config = Config(
        config={
            'sampler': {'type':'const','param':1}
        },
        service_name='myservice'
    )
    return config.initialize_tracer()

flask_tracer = FlaskTracer(initialize_tracer,True,app)

@app.route('/')
def index():
    return "Welcome to MyService", 200


@app.route('/productflow')
def productFlow():
    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('order-api',child_of=parent_span) as span:
        span.set_tag("http.url",order_url)
        r = requests.get(order_url)
        span.set_tag("http_status_code",r.status_code)

    with opentracing.tracer.start_span('payment-api',child_of=parent_span) as span:
        span.set_tag("http.url",payment_url)
        r = requests.get(payment_url)
        span.set_tag("http_status_code",r.status_code)

    return "Product Flow complete", 200
