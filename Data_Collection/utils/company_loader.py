# utils/company_loader.py

import json
import os


def load_company_config(company_id: str) -> dict:
    path = os.path.join("config", "companies", f"{company_id}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Company config not found: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    required_keys = ["company_id", "company_name", "website", "industry", "products"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key '{key}' in {company_id}.json")

    return data