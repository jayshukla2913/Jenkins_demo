from flask import Flask
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL")
engine = create_engine(database_url)

@app.route("/")
def home():
    # Simple test query
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        row = result.fetchone()
    return f"Hello from Flask connected to PostgreSQL! Test query result: {row[0]}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
