from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

from model import Model

app = Flask(__name__)
db = Model()


@app.route("/")
def index():
    """
    Homepage
    :return: render_template()
    """
    db.save_event({
        "action": "view",
        "body": "User opened page"
    })
    return render_template('index.html')


@app.route("/api/events", methods=["POST"])
def save_event():
    """
    API handler that saves event to DB
    :return: str(JSON)
    """
    db.save_event({
        "action": request.form['action'],
        "body": request.form['body']
    })
    return jsonify({"status": "ok"})


@app.route("/api/events", methods=["GET"])
def get_events():
    """
    API handler responds with JSON data of last 20 events
    :return: str(JSON)
    """
    rows = db.get_events()
    return jsonify(rows)


@app.route("/api/events/stats", methods=["GET"])
def get_events_stats():
    """
    API handler responds with JSON data with events stats
    :return: str(JSON)
    """
    stats = db.get_events_stats()
    return jsonify(stats)

