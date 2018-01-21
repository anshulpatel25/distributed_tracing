from flask import Flask
import random
import time



app = Flask(__name__)


@app.route("/")
def index():
    time.sleep(random.randint(1,10))
    return "Payment Processed", 200
