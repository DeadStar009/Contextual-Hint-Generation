from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging
import traceback
from hint_pipeline import HintPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HintRequest(BaseModel):
    problem_statement: str
    current_code: str
    timestamp: str  # ISO format string
    previous_hints: list[str] = []

class HintResponse(BaseModel):
    hint: str
    hint_type: str

# Initialize the pipeline
pipeline = HintPipeline()

@app.post("/api/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    try:
        logger.info("Received hint request")
        
        # Parse the timestamp
        timestamp = datetime.fromisoformat(request.timestamp.replace('Z', '+00:00'))
        
        # Get hint type
        hint_type = await pipeline.classify_hint_type(
            request.problem_statement,
            request.current_code,
            timestamp,
            request.previous_hints
        )
        logger.info(f"Classified hint type: {hint_type}")
        
        # Generate hint
        hint = await pipeline.generate_hint(
            request.problem_statement,
            request.current_code,
            timestamp,
            request.previous_hints,
            hint_type
        )
        logger.info("Generated initial hint")
        
        # Verify hint
        verified_hint = await pipeline.verify_hint(
            hint,
            request.problem_statement,
            request.current_code,
            request.previous_hints
        )
        logger.info("Verified hint")
        
        return HintResponse(hint=verified_hint, hint_type=hint_type)
        
    except Exception as e:
        logger.error(f"Error generating hint: {str(e)}\n{traceback.format_exc()}")
        if "huggingface" in str(e).lower():
            raise HTTPException(status_code=503, detail="Model service temporarily unavailable")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    try:
        # Test the models with a simple request
        result = await pipeline.classify_hint_type(
            "Print Hello World",
            "print('Hello')",
            datetime.now(),
            []
        )
        return {"status": "healthy", "models": "operational"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)} 