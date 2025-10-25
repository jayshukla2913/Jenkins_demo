from flask import Flask
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env in project root
load_dotenv()

# Get database URL from environment variable
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise Exception("DATABASE_URL not set in .env or environment")

engine = create_engine(database_url, echo=False)

@app.route("/")
def home():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
        return f"Hello from Flask connected to PostgreSQL! Test query result: {row[0]}"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
