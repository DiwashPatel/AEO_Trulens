#!/bin/bash

set -e

BASE_DIR="med_demo"

echo "Creating company-centric project structure..."

# -----------------------
# Core Directories
# -----------------------

mkdir -p $BASE_DIR/config/companies
mkdir -p $BASE_DIR/prompts
mkdir -p $BASE_DIR/data
mkdir -p $BASE_DIR/models
mkdir -p $BASE_DIR/utils

# -----------------------
# Company Config Files
# -----------------------

touch $BASE_DIR/config/companies/nike.json
touch $BASE_DIR/config/companies/adidas.json
touch $BASE_DIR/config/companies/apple.json

# -----------------------
# Prompt Files
# -----------------------

touch $BASE_DIR/prompts/base_prompts.txt
touch $BASE_DIR/prompts/instruction_block.txt

# -----------------------
# Model Adapter
# -----------------------

touch $BASE_DIR/models/openai_adapter.py

# -----------------------
# Utils
# -----------------------

touch $BASE_DIR/utils/company_loader.py
touch $BASE_DIR/utils/prompt_loader.py
touch $BASE_DIR/utils/storage.py
touch $BASE_DIR/utils/json_cleaner.py

# -----------------------
# Root Config + Runner
# -----------------------

touch $BASE_DIR/run_config.json
touch $BASE_DIR/main_runner.py
touch $BASE_DIR/requirements.txt

echo "Structure created successfully."