from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb+srv://***db_user***:****pass***@ghostapi.3qe1pdk.mongodb.net/?appName=GHOSTapi"
client = MongoClient(MONGO_URI)

db = client["GHOSTapi"]
collection = db["readings"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin/data")
def get_data():
    docs = list(collection.find({}, {
        "_id": 1,
        "voltage": 1,
        "current": 1,
        "timestamp": 1
    }))

    if not docs:
        return jsonify(voltage=[], current=[], timestamp=[])

    voltages, currents, timestamps, ids = [], [], [], []

    for d in docs:
        voltages.append(d["voltage"])
        currents.append(d["current"])
        ts = datetime.fromtimestamp(d["timestamp"])
        timestamps.append(ts.strftime("%H:%M:%S"))
        ids.append(d["_id"])

    collection.delete_many({"_id": {"$in": ids}})

    return jsonify(
        voltage=voltages,
        current=currents,
        timestamp=timestamps
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=False
    )
