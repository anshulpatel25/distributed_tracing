from flask import Flask
import time
import random


app = Flask(__name__)


@app.route("/")
def index():
    time.sleep(random.randint(1,10))
    return "Order Confirmed", 200
