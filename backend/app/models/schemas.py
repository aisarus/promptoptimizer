from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class OptimizeRequest(BaseModel):
    """Request model for prompt optimization"""
    prompt: str = Field(..., min_length=1, description="Prompt to optimize")
    backend: Literal["gemini", "grok"] = Field(default="gemini", description="LLM backend to use")
    gemini_api_key: Optional[str] = Field(None, description="Gemini API key (if not set in env)")
    xai_api_key: Optional[str] = Field(None, description="xAI API key (if not set in env)")
    max_iterations: int = Field(default=3, ge=1, le=6, description="Max D/S iterations")
    convergence_threshold: float = Field(default=0.05, ge=0.01, le=0.20, description="Convergence threshold")
    force_optimization: bool = Field(default=True, description="Force optimization even if Smart Queue says no")


class SmartQueueResult(BaseModel):
    """Smart Queue analysis result"""
    clarity: float = Field(..., ge=0.0, le=1.0)
    structure: float = Field(..., ge=0.0, le=1.0)
    constraints: float = Field(..., ge=0.0, le=1.0)
    needs_optimization: bool
    comment: str


class PCVResult(BaseModel):
    """Proposer-Critic-Verifier result"""
    proposed_prompt: str
    critique: str
    final_prompt: str


class DSIteration(BaseModel):
    """Single D/S iteration result"""
    iteration: int
    d_block_output: str
    s_block_output: str
    length: int
    change_rate: float


class PairwiseEvaluation(BaseModel):
    """Pairwise comparison result"""
    clarity: float = Field(..., ge=-1.0, le=1.0)
    structure: float = Field(..., ge=-1.0, le=1.0)
    constraints: float = Field(..., ge=-1.0, le=1.0)
    usefulness: float = Field(..., ge=-1.0, le=1.0)
    comment: str


class OptimizeResponse(BaseModel):
    """Response model for prompt optimization"""
    success: bool
    original_prompt: str
    final_prompt: str
    
    # Pipeline results
    smart_queue: SmartQueueResult
    pcv: PCVResult
    ds_iterations: list[DSIteration]
    evaluation: PairwiseEvaluation
    
    # Metadata
    original_length: int
    final_length: int
    length_change_percent: float
    converged: bool
    convergence_iteration: Optional[int] = None
    
    # Timing
    processing_time_seconds: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
