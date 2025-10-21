from flask import Flask
from sqlalchemy import create_engine
import os

app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL")
engine = create_engine(database_url)

@app.route("/")
def home():
    return "Hello from Flask connected to PostgreSQL!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
