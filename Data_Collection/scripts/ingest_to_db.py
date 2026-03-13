import os
import json
import sqlite3
from datetime import datetime

DB_FILE = "botb.db"  # This will be created in your root folder
DATA_DIR = "data"

def setup_db():
    """Creates the SQLite tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Table for general run info
    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            company_id TEXT,
            product_id TEXT,
            feature TEXT,
            constraint_text TEXT,
            model_name TEXT,
            raw_text TEXT
        )
    """)
    
    # Table for specific recommendations (The "Gold" data)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            product_name TEXT,
            reason TEXT,
            source_url TEXT,
            FOREIGN KEY (run_id) REFERENCES runs (id)
        )
    """)
    conn.commit()
    conn.close()

def parse_timestamp(ts):
    try:
        return datetime.fromisoformat(ts).isoformat()
    except Exception:
        return datetime.now().isoformat()

def main():
    setup_db() # Ensure tables exist
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    count = 0

    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if not file.endswith(".jsonl"):
                continue

            path = os.path.join(root, file)
            print(f"Ingesting: {path}")

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                    except Exception:
                        continue

                    model_data = record.get("model", {})
                    response_data = record.get("response", {})
                    timestamp = parse_timestamp(record.get("timestamp"))

                    # Insert run (SQLite uses '?' instead of '%s')
                    cur.execute("""
                        INSERT INTO runs (
                            timestamp, company_id, product_id, feature, 
                            constraint_text, model_name, raw_text
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        timestamp,
                        record.get("company_id"),
                        record.get("product_id"),
                        record.get("feature"),
                        record.get("constraint"),
                        model_data.get("name"),
                        response_data.get("raw_text")
                    ))
                    
                    run_id = cur.lastrowid # Get the ID of the run we just inserted
                    
                    parsed = response_data.get("parsed_json") or {}
                    recommendations = parsed.get("recommendations") or []

                    for rec in recommendations:
                        cur.execute("""
                            INSERT INTO recommendations (run_id, product_name, reason, source_url)
                            VALUES (?, ?, ?, ?)
                        """, (
                            run_id,
                            rec.get("product"),
                            rec.get("reason"),
                            rec.get("source_url")
                        ))
                    
                    count += 1

    conn.commit()
    conn.close()
    print(f"Ingestion complete. {count} records processed.")

if __name__ == "__main__":
    main()