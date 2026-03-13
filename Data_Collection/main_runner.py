import argparse
import json
import os
from datetime import datetime

from utils.company_loader import load_company_config
from utils.prompt_loader import load_base_prompt, load_instruction_block
from utils.storage import append_jsonl
from models.model_dispatcher import call_model


# --------------------------------
# LOAD RUN CONFIG
# --------------------------------

def load_run_config(path="run_config.json"):
    with open(path, "r") as f:
        return json.load(f)


# --------------------------------
# BUILD PROMPT
# --------------------------------

def build_prompt(base_prompt, instruction_block,
                 company, product,
                 feature, constraint):

    dynamic_block = f"""
Feature: {feature}
Constraint: {constraint}

User Intent:
I want to buy {product['product_name']}
that focuses on "{feature}" and satisfies "{constraint}".
"""

    return f"{instruction_block}\n\n{base_prompt}\n\n{dynamic_block}".strip()


# --------------------------------
# OUTPUT PATH
# --------------------------------

def get_output_path(company_id, product_id, model_name):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join("data", company_id, product_id, model_name)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{today}.jsonl")


# --------------------------------
# MAIN
# --------------------------------

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True, help="Company ID (e.g., adidas)")
    parser.add_argument("--product", required=False, help="Product ID (optional)")
    args = parser.parse_args()

    company_id = args.company
    product_id_filter = args.product

    run_config = load_run_config()
    models = run_config["models"]
    num_runs = run_config.get("num_runs_per_combination", 1)

    company = load_company_config(company_id)

    base_prompt = load_base_prompt()
    instruction_block = load_instruction_block()

    products_to_run = []

    if product_id_filter:
        product = next(
            (p for p in company["products"] if p["product_id"] == product_id_filter),
            None
        )

        if not product:
            raise ValueError(f"Product '{product_id_filter}' not found in '{company_id}'")

        products_to_run.append(product)
    else:
        products_to_run = company["products"]

    for product in products_to_run:
        for feature in product["features"]:
            for constraint in product["constraints"]:
                for model in models:
                    for run_index in range(num_runs):

                        print(
                            f"[RUN] {company_id} | "
                            f"{product['product_id']} | "
                            f"{feature} | "
                            f"{constraint} | "
                            f"{model['name']} | "
                            f"Run {run_index+1}"
                        )

                        prompt = build_prompt(
                            base_prompt,
                            instruction_block,
                            company,
                            product,
                            feature,
                            constraint
                        )

                        response = call_model(
                            model_config=model,
                            prompt=prompt
                        )

                        record = {
                            "timestamp": datetime.now().isoformat(),
                            "company_id": company_id,
                            "product_id": product["product_id"],
                            "feature": feature,
                            "constraint": constraint,
                            "model": model,
                            "run_number": run_index + 1,
                            "response": response
                        }

                        output_path = get_output_path(
                            company_id,
                            product["product_id"],
                            model["name"]
                        )

                        append_jsonl(output_path, record)

    print("Execution completed.")


if __name__ == "__main__":
    main()