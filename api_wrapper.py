from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
import asyncio
import json
import uuid
from welsh_hunter import WELSHFounderHunter, create_welsh_hunter_config

app = FastAPI(
    title="WELSH-Founder Hunter API",
    description="Blockchain forensics agent for identifying WELSH token founder",
    version="1.0.0"
)

class InvestigationRequest(BaseModel):
    welsh_contract: str
    arkadiko_wallets: List[str]
    philip_wallets: Optional[List[str]] = None
    config_overrides: Optional[Dict] = None

class InvestigationResponse(BaseModel):
    investigation_id: str
    status: str
    message: str

class InvestigationResult(BaseModel):
    success: bool
    deployer_address: Optional[str] = None
    cluster_size: Optional[int] = None
    evidence_count: Optional[int] = None
    confidence_score: Optional[float] = None
    conclusion: Optional[str] = None
    report: Optional[str] = None
    error: Optional[str] = None

# In-memory storage for demo (use Redis/DB in production)
investigations = {}

@app.post("/investigate", response_model=InvestigationResponse)
async def start_investigation(request: InvestigationRequest, background_tasks: BackgroundTasks):
    """Start a new WELSH founder investigation"""
    
    investigation_id = str(uuid.uuid4())
    
    # Initialize investigation
    investigations[investigation_id] = {
        'status': 'started',
        'result': None
    }
    
    # Run investigation in background
    background_tasks.add_task(
        run_investigation,
        investigation_id,
        request.welsh_contract,
        request.arkadiko_wallets,
        request.philip_wallets,
        request.config_overrides or {}
    )
    
    return InvestigationResponse(
        investigation_id=investigation_id,
        status="started",
        message="Investigation started successfully"
    )

@app.get("/investigate/{investigation_id}", response_model=InvestigationResult)
async def get_investigation_result(investigation_id: str):
    """Get investigation results"""
    
    if investigation_id not in investigations:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    investigation = investigations[investigation_id]
    
    if investigation['status'] == 'running':
        return InvestigationResult(
            success=False,
            error="Investigation still running"
        )
    elif investigation['status'] == 'completed':
        return InvestigationResult(**investigation['result'])
    else:
        return InvestigationResult(
            success=False,
            error="Investigation failed"
        )

@app.get("/investigate/{investigation_id}/status")
async def get_investigation_status(investigation_id: str):
    """Get investigation status"""
    
    if investigation_id not in investigations:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    return {"investigation_id": investigation_id, "status": investigations[investigation_id]['status']}

async def run_investigation(investigation_id: str, welsh_contract: str, 
                          arkadiko_wallets: List[str], philip_wallets: List[str],
                          config_overrides: Dict):
    """Run the investigation asynchronously"""
    
    try:
        investigations[investigation_id]['status'] = 'running'
        
        # Create configuration
        config = create_welsh_hunter_config()
        config.update(config_overrides)
        
        # Initialize hunter
        hunter = WELSHFounderHunter(config)
        
        # Run investigation
        result = hunter.run_full_investigation(
            welsh_contract=welsh_contract,
            arkadiko_wallets=arkadiko_wallets,
            philip_wallets=philip_wallets
        )
        
        investigations[investigation_id]['status'] = 'completed'
        investigations[investigation_id]['result'] = result
        
    except Exception as e:
        investigations[investigation_id]['status'] = 'failed'
        investigations[investigation_id]['result'] = {
            'success': False,
            'error': str(e)
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "welsh-founder-hunter"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "WELSH-Founder Hunter",
        "description": "Blockchain forensics agent for identifying WELSH token founder",
        "version": "1.0.0",
        "endpoints": {
            "start_investigation": "POST /investigate",
            "get_result": "GET /investigate/{investigation_id}",
            "get_status": "GET /investigate/{investigation_id}/status",
            "health": "GET /health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)