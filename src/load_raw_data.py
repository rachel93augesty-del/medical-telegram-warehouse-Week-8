import os
import json
import psycopg2
from pathlib import Path

# -----------------------------
# PostgreSQL connection settings
# -----------------------------
DB_HOST = "localhost"
DB_NAME = "medical_warehouse"
DB_USER = "postgres"
DB_PASSWORD = "Rachelsemer@db93"  # <-- your new password
DB_PORT = 5432

# -----------------------------
# Connect to PostgreSQL
# -----------------------------
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("✅ Connected to PostgreSQL!")
except Exception as e:
    print("❌ Connection failed:", e)
    exit(1)

# -----------------------------
# Create raw schema and table
# -----------------------------
cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    date TIMESTAMP,
    text_content TEXT,
    views INT,
    forwards INT,
    has_image BOOLEAN
);
""")
conn.commit()
print("✅ Table raw.telegram_messages ready!")

# -----------------------------
# Path to your JSON data lake
# -----------------------------
data_path = Path("data/raw/telegram_messages")

if not data_path.exists():
    print(f"❌ Data path does not exist: {data_path}")
    exit(1)

# -----------------------------
# Load JSON files into PostgreSQL
# -----------------------------
for json_file in data_path.rglob("*.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages 
                        (message_id, channel_name, date, text_content, views, forwards, has_image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (message_id) DO NOTHING;
                """, (
                    msg.get("message_id"),
                    json_file.stem,       # use filename as channel_name
                    msg.get("date"),
                    msg.get("text"),
                    msg.get("views"),
                    msg.get("forwards"),
                    msg.get("has_media")
                ))
        print(f"✅ Loaded {json_file}")
    except Exception as e:
        print(f"❌ Failed to load {json_file}: {e}")

# -----------------------------
# Close connection
# -----------------------------
conn.commit()
cur.close()
conn.close()
print("✅ Raw data loaded into PostgreSQL!")
