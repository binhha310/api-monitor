from flask import Flask, send_file
app = Flask(__name__)

@app.route("/")
def home():
    return send_file("../logs/events.log", mimetype='text/plain')
