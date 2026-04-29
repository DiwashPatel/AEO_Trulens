# Analytics Backend – AI-Powered Search & Recommendation Engine

> **Track AI brand visibility and sentiment across multiple LLM providers in real-time.**

This backend system runs large-scale batch queries against OpenAI, Google Gemini, Anthropic Claude, and Perplexity AI using dynamically generated prompts. It collects raw and parsed recommendations into a SQLite database for downstream analysis, visualization, and reporting.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [Installation & Setup](#installation--setup)


---

## 🎯 Project Overview

### The Problem
How do AI models "see" your brand, products, and competitors? What recommendations does GPT-4 vs. Claude give users searching for your category? Are there blind spots, red flags, or opportunities in AI-generated content?

### The Solution
This analytics system:

1. **Generates multi-variant prompts** based on company configs (products, features, constraints)
2. **Queries multiple LLM providers** in parallel and logs raw responses
3. **Parses structured recommendations** into a unified JSON format
4. **Ingests results into SQLite** for trend analysis and reporting
5. **Exposes REST APIs** for frontend dashboards and real-time query triggers

### Key Metrics
- **Visibility**: How often is your brand mentioned in AI-generated recommendations?
- **Sentiment**: Positive, negative, or neutral mentions across providers?
- **Competitive Presence**: How does your brand rank vs. competitors in AI responses?
- **AI-Friendliness**: Which prompts/features perform best across models?

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend Dashboard                         │
│          (Next.js / React – separate repo)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│           FastAPI Server (api_server.py)                    │
│  ┌──────────────────┬──────────────────┬──────────────────┐ │
│  │ POST /config     │ POST /analysis   │ GET /analysis    │ │
│  │ /update          │ /trigger         │ /results         │ │
│  └──────────────────┴──────────────────┴──────────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────────────┐   ┌─────────────────────┐
│  Batch Orchestrator  │   │  Config/Prompt      │
│  (main_runner.py)    │   │  Management         │
│                      │   │                     │
│  - Loads configs     │   └─────────────────────┘
│  - Builds prompts    │
│  - Dispatches calls  │
│  - Writes JSONL      │
└──────────┬───────────┘
           │
    ┌──────┼──────┬──────────┬──────────┐
    ▼      ▼      ▼          ▼          ▼
┌────────┐┌─────┐┌───────┐┌────────┐┌──────────┐
│ OpenAI ││ Gemini Claude │Perplexity│ Responses│
│ GPT-4  │└─────┘└───────┘└────────┘│  API     │
└────────┘                          └──────────┘
    │      │      │        │           │
    └──────┴──────┴────────┴───────────┘
             │
             ▼
┌─────────────────────────────────┐
│   data/{company}/{product}/     │
│   {model}/{YYYY-MM-DD}.jsonl    │
│                                 │
│   (Raw responses + parsed JSON) │
└────────────────┬────────────────┘
                 │
                 ▼
     ┌───────────────────────┐
     │ Ingestion Script      │
     │ (ingest_to_db.py)     │
     └───────────┬───────────┘
                 │
                 ▼
     ┌───────────────────────┐
     │  SQLite Database      │
     │  (botb.db)            │
     │                       │
     │ - runs table          │
     │ - recommendations tbl │
     └───────────┬───────────┘
                 │
                 ▼
     ┌───────────────────────┐
     │ Analysis Notebook     │
     │ (analysis_1.ipynb)    │
     │                       │
     │ Metrics & Reporting   │
     └───────────────────────┘
```

---

## 📁 Folder Structure

```
Data_Collection/
├── main_runner.py              # CLI: batch runner orchestrator
├── api_server.py               # FastAPI service
├── run_config.json             # Model configs + run parameters
│
├── config/
│   └── companies/              # Company JSON definitions
│       ├── adidas.json
│       ├── nike.json
│       └── apple.json
│
├── prompts/
│   ├── base_prompts.txt        # Base prompt template
│   └── instruction_block.txt   # Instruction prepended to all prompts
│
├── models/                     # LLM provider adapters
│   ├── model_dispatcher.py     # Router: selects adapter by provider
│   ├── openai_adapter.py       # OpenAI / ChatGPT integration
│   ├── gemini_adapter.py       # Google Gemini integration
│   ├── claude_adapter.py       # Anthropic Claude integration
│   └── perplexity_adapter.py   # Perplexity (OpenAI SDK wrapper)
│
├── scripts/
│   └── ingest_to_db.py         # ETL: JSONL → SQLite
│
└── utils/
    ├── company_loader.py       # Load & validate company configs
    ├── prompt_loader.py        # Load prompt templates
    ├── storage.py              # Append JSONL records
    └── json_cleaner.py         # Extract JSON from wrapped responses

Data_fAnalysis/
└── analysis_1.ipynb            # Pandas + chart analysis of botb.db

root/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── botb.db                     # SQLite database (generated)
└── dem_venv/                   # Virtual environment
```


---
# 🚀 Analytics Backend

> **Query multiple AI models (GPT-4, Claude, Gemini, Perplexity) and track brand visibility in AI recommendations.**

Batch-query LLM providers, collect responses, store in SQLite, analyze results.

---

## 📋 Quick Start

### 1️⃣ Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set API keys
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
export CLAUDE_API_KEY="sk-ant-..."
export PERPLEXITY_API_KEY="pplx-..."
```

### 2️⃣ Configure Your Company

Create a company file in `Data_Collection/config/companies/`:

```json
{
  "company_id": "adidas",
  "company_name": "Adidas",
  "website": "https://www.adidas.com",
  "products": [
    {
      "product_id": "running_shoes",
      "product_name": "Adidas Running Shoes",
      "features": ["lightweight", "responsive"],
      "constraints": ["$100-$200 price range"]
    }
  ]
}
```

### 3️⃣ Run Batch Analysis

```bash
# Query all models for a company
python Data_Collection/main_runner.py --company adidas

# Or specific product
python Data_Collection/main_runner.py --company adidas --product running_shoes
```

Results saved to: `Data_Collection/data/adidas/running_shoes/{model}/{date}.jsonl`

---

## 🔄 How It Works

```
1. You run: main_runner.py --company adidas
   ↓
2. System loads:
   - Company config (products, features, constraints)
   - Model configs (which LLMs to use)
   - Prompt templates
   ↓
3. For each combination:
   product × feature × constraint × model
   ↓
4. Builds a prompt and sends to LLM
   ↓
5. Saves results as JSONL
   ↓
6. Ingest into SQLite: python Data_Collection/scripts/ingest_to_db.py
   ↓
7. Analyze in Jupyter: Data_fAnalysis/analysis_1.ipynb
```

---

## 📁 Folder Overview

| Folder | Purpose |
|--------|---------|
| `Data_Collection/` | Main pipeline & APIs |
| `Data_Collection/config/companies/` | Brand configs (JSON) |
| `Data_Collection/prompts/` | Prompt templates |
| `Data_Collection/models/` | LLM adapters (OpenAI, Gemini, Claude, Perplexity) |
| `Data_Collection/scripts/` | Database ingestion |
| `Data_Collection/data/` | Raw JSONL outputs |
| `Data_fAnalysis/` | Analysis notebook |

---

## 🌐 API Server (Optional)

Run the FastAPI service for frontend integration:

```bash
python Data_Collection/api_server.py
# Server at: http://localhost:8000
```

**Key endpoints:**
- `POST /config/update` → Save company config
- `POST /analysis/trigger/{company_id}` → Start batch job
- `GET /analysis/results/{company_id}` → Get results

---

## 💾 Database

After running batch jobs, ingest data into SQLite:

```bash
python Data_Collection/scripts/ingest_to_db.py
```

Creates `botb.db` with:
- `runs` table (metadata + raw responses)
- `recommendations` table (parsed outputs)

Analyze with Jupyter:
```bash
jupyter notebook Data_fAnalysis/analysis_1.ipynb
```

---
---
```
Note: This project was vibe-coded and also this readme.md is generated by chatGPT. 

```
---