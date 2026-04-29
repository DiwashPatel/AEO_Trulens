import os
import json
import subprocess
from fastapi import FastAPI, HTTPException, Security, BackgroundTasks, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AI Search Optimization API")

# --- SECURITY ---
API_KEY = "" #Removed when pushing # we can just get from .env file
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

async def validate_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return key

# --- DATA MODELS ---
class Product(BaseModel):
    product_id: str
    product_name: str
    features: List[str]
    constraints: List[str]

class CompanyConfig(BaseModel):
    company_id: str
    company_name: str
    website: str
    industry: str
    products: List[Product]

# --- BACKGROUND WORKER ---
def run_analysis_script(company_id: str):
    """Triggers your existing main_runner script"""
    try:
        # This calls your script just like you do in the terminal
        subprocess.run(["python", "main_runner.py", "--company", company_id], check=True)
    except Exception as e:
        print(f"Error running analysis for {company_id}: {e}")

# --- ENDPOINTS ---

@app.post("/config/update", dependencies=[Depends(validate_api_key)])
async def update_config(config: CompanyConfig):
    """Saves or updates a company JSON file"""
    file_path = f"config/companies/{config.company_id}.json"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w") as f:
        json.dump(config.model_dump(), f, indent=2)
        
    return {"status": "success", "message": f"Config for {config.company_id} updated."}

@app.post("/analysis/trigger/{company_id}", dependencies=[Depends(validate_api_key)])
async def trigger_analysis(company_id: str, background_tasks: BackgroundTasks):
    """Triggers the long-running loop without making the frontend wait"""
    # Check if config exists first
    if not os.path.exists(f"config/companies/{company_id}.json"):
        raise HTTPException(status_code=404, detail="Company config not found. Please register first.")
    
    background_tasks.add_task(run_analysis_script, company_id)
    return {"status": "processing", "message": f"Analysis started for {company_id}. Check back in a few minutes."}

@app.get("/analysis/results/{company_id}", dependencies=[Depends(validate_api_key)])
async def get_results(company_id: str):
    """Returns the analyzed data from your 'data' folder"""
    result_path = f"data/{company_id}/summary.json" # Adjust based on your script's output
    
    if os.path.exists(result_path):
        with open(result_path, "r") as f:
            return json.load(f)
    
    # Mock data
    return {
        "status": "partial",
        "metrics": {
            "ai_visibility": 65,
            "top_referring_urls": ["https://techcrunch.com", "https://runnersworld.com"],
            "suggestion": "Mock Suggestions"
        }
    }
