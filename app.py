from flask import Flask
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load .env file from project root
load_dotenv()

# Construct DATABASE_URL from individual env vars
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
    raise Exception("One or more DB environment variables are missing")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

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
