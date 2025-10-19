from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_database()

@app.route("/")
def home():
    return "Hello from Flask connected to MongoDB!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
