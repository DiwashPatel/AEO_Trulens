import os
import json
import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "database": "botb",
    "user": "postgres",
    "password": "botbpatel"   
}

DATA_DIR = "data"


def parse_timestamp(ts):
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def main():

    conn = psycopg2.connect(**DB_CONFIG)
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
                    usage = response_data.get("usage") or {}

                    timestamp = parse_timestamp(record.get("timestamp"))


                    # Insert run
                    cur.execute("""
                        INSERT INTO runs (
                            timestamp,
                            company_id,
                            product_id,
                            feature,
                            constraint_text,
                            model_id,
                            model_name,
                            provider,
                            search_enabled,
                            run_number,
                            input_tokens,
                            output_tokens,
                            total_tokens,
                            raw_text
                        )
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        RETURNING id
                    """, (
                        timestamp,
                        record.get("company_id"),
                        record.get("product_id"),
                        record.get("feature"),
                        record.get("constraint"),
                        model_data.get("id"),
                        model_data.get("name"),
                        model_data.get("provider"),
                        model_data.get("search_enabled", False),
                        record.get("run_number"),
                        usage.get("input_tokens"),
                        usage.get("output_tokens"),
                        usage.get("total_tokens"),
                        response_data.get("raw_text")
                    ))
                    
                    count +=1 
                    print("....ingested..{count}...data")

                    run_id = cur.fetchone()[0]

                    parsed = response_data.get("parsed_json") or {}
                    recommendations = parsed.get("recommendations") or []

                    for rec in recommendations:
                        cur.execute("""
                            INSERT INTO recommendations (
                                run_id,
                                product_name,
                                reason,
                                source_url
                            )
                            VALUES (%s,%s,%s,%s)
                        """, (
                            run_id,
                            rec.get("product"),
                            rec.get("reason"),
                            rec.get("source_url")
                        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Ingestion complete.")


if __name__ == "__main__":
    main()