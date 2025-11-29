from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
import time
import json

from ..models.schemas import (
    OptimizeRequest,
    OptimizeResponse,
    ErrorResponse,
    HealthResponse,
)
from ..services.llm_provider import get_llm_provider
from ..services.optimizer import PromptOptimizer
from ..utils.json_parser import approximate_length

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy")


@router.post("/optimize", response_model=OptimizeResponse, responses={400: {"model": ErrorResponse}})
async def optimize_prompt(request: OptimizeRequest):
    """
    Optimize a prompt using the full pipeline:
    1. Smart Queue analysis
    2. Proposer-Critic-Verifier (PCV)
    3. D/S cycle (Diversification/Stabilization)
    4. Pairwise evaluation
    """
    start_time = time.time()
    
    try:
        # Initialize LLM provider
        provider = get_llm_provider(
            backend=request.backend,
            gemini_key=request.gemini_api_key,
            xai_key=request.xai_api_key
        )
        
        # Initialize optimizer
        optimizer = PromptOptimizer(provider)
        
        # Step 1: Smart Queue
        smart_queue_result = optimizer.smart_queue(request.prompt)
        
        # Check if optimization is needed
        if not smart_queue_result.needs_optimization and not request.force_optimization:
            # Return early if no optimization needed
            processing_time = time.time() - start_time
            
            return OptimizeResponse(
                success=True,
                original_prompt=request.prompt,
                final_prompt=request.prompt,
                smart_queue=smart_queue_result,
                pcv=None,
                ds_iterations=[],
                evaluation=None,
                original_length=approximate_length(request.prompt),
                final_length=approximate_length(request.prompt),
                length_change_percent=0.0,
                converged=True,
                convergence_iteration=0,
                processing_time_seconds=processing_time
            )
        
        # Step 2: PCV (Proposer-Critic-Verifier)
        pcv_result = optimizer.run_pcv(request.prompt)
        
        # Step 3: D/S Cycle
        final_prompt, ds_iterations, converged, convergence_iteration = optimizer.run_ds_cycle(
            initial_prompt=pcv_result.final_prompt,
            max_iterations=request.max_iterations,
            convergence_threshold=request.convergence_threshold
        )
        
        # Step 4: Pairwise Evaluation
        evaluation = optimizer.pairwise_eval(request.prompt, final_prompt)
        
        # Calculate metrics
        original_length = approximate_length(request.prompt)
        final_length = approximate_length(final_prompt)
        length_change_percent = ((final_length - original_length) / original_length) * 100
        
        processing_time = time.time() - start_time
        
        return OptimizeResponse(
            success=True,
            original_prompt=request.prompt,
            final_prompt=final_prompt,
            smart_queue=smart_queue_result,
            pcv=pcv_result,
            ds_iterations=ds_iterations,
            evaluation=evaluation,
            original_length=original_length,
            final_length=final_length,
            length_change_percent=length_change_percent,
            converged=converged,
            convergence_iteration=convergence_iteration,
            processing_time_seconds=processing_time
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/optimize-stream")
async def optimize_prompt_stream(request: OptimizeRequest):
    """
    Optimize a prompt with real-time streaming updates.
    Returns Server-Sent Events (SSE) for each stage completion.
    """
    
    async def generate_events():
        start_time = time.time()
        
        try:
            # Initialize LLM provider
            yield f"data: {json.dumps({'stage': 'init', 'message': 'Initializing LLM provider...'})}\n\n"
            
            provider = get_llm_provider(
                backend=request.backend,
                gemini_key=request.gemini_api_key,
                xai_key=request.xai_api_key
            )
            optimizer = PromptOptimizer(provider)
            
            # Stage 1: Smart Queue
            yield f"data: {json.dumps({'stage': 'smart_queue', 'status': 'running', 'message': 'Analyzing prompt quality...'})}\n\n"
            smart_queue_result = optimizer.smart_queue(request.prompt)
            yield f"data: {json.dumps({'stage': 'smart_queue', 'status': 'complete', 'data': smart_queue_result.dict()})}\n\n"
            
            # Check if optimization needed
            if not smart_queue_result.needs_optimization and not request.force_optimization:
                yield f"data: {json.dumps({'stage': 'complete', 'message': 'No optimization needed', 'final_prompt': request.prompt})}\n\n"
                return
            
            # Stage 2: PCV - Proposer
            yield f"data: {json.dumps({'stage': 'pcv_proposer', 'status': 'running', 'message': 'Proposer rewriting prompt...'})}\n\n"
            proposed = optimizer.proposer_step(request.prompt)
            yield f"data: {json.dumps({'stage': 'pcv_proposer', 'status': 'complete', 'data': {'proposed_prompt': proposed}})}\n\n"
            
            # Stage 3: PCV - Critic
            yield f"data: {json.dumps({'stage': 'pcv_critic', 'status': 'running', 'message': 'Critic analyzing proposal...'})}\n\n"
            critique = optimizer.critic_step(proposed)
            yield f"data: {json.dumps({'stage': 'pcv_critic', 'status': 'complete', 'data': {'critique': critique}})}\n\n"
            
            # Stage 4: PCV - Verifier
            yield f"data: {json.dumps({'stage': 'pcv_verifier', 'status': 'running', 'message': 'Verifier creating final version...'})}\n\n"
            pcv_final = optimizer.verifier_step(request.prompt, proposed, critique)
            yield f"data: {json.dumps({'stage': 'pcv_verifier', 'status': 'complete', 'data': {'final_prompt': pcv_final}})}\n\n"
            
            # Stage 5: D/S Cycle
            current = pcv_final
            prev_len = approximate_length(current)
            converged = False
            convergence_iteration = None
            ds_iterations = []
            
            for i in range(1, request.max_iterations + 1):
                # D-Block
                yield f"data: {json.dumps({'stage': f'ds_iteration_{i}_d', 'status': 'running', 'message': f'D/S Iteration {i}: Diversification...'})}\n\n"
                d_out = optimizer.d_block(current)
                yield f"data: {json.dumps({'stage': f'ds_iteration_{i}_d', 'status': 'complete', 'data': {'output': d_out}})}\n\n"
                
                # S-Block
                yield f"data: {json.dumps({'stage': f'ds_iteration_{i}_s', 'status': 'running', 'message': f'D/S Iteration {i}: Stabilization...'})}\n\n"
                s_out = optimizer.s_block(d_out)
                
                current = s_out
                cur_len = approximate_length(current)
                change_rate = abs(cur_len - prev_len) / max(prev_len, 1)
                
                yield f"data: {json.dumps({'stage': f'ds_iteration_{i}_s', 'status': 'complete', 'data': {'output': s_out, 'length': cur_len, 'change_rate': change_rate, 'iteration': i}})}\n\n"
                
                prev_len = cur_len
                
                if change_rate < request.convergence_threshold:
                    converged = True
                    convergence_iteration = i
                    yield f"data: {json.dumps({'stage': 'ds_converged', 'message': f'Converged at iteration {i}'})}\n\n"
                    break
            
            final_prompt = current
            
            # Stage 6: Evaluation
            yield f"data: {json.dumps({'stage': 'evaluation', 'status': 'running', 'message': 'Comparing original vs optimized...'})}\n\n"
            evaluation = optimizer.pairwise_eval(request.prompt, final_prompt)
            yield f"data: {json.dumps({'stage': 'evaluation', 'status': 'complete', 'data': evaluation.dict()})}\n\n"
            
            # Final summary
            processing_time = time.time() - start_time
            original_length = approximate_length(request.prompt)
            final_length = approximate_length(final_prompt)
            length_change_percent = ((final_length - original_length) / original_length) * 100
            
            yield f"data: {json.dumps({'stage': 'complete', 'data': {'final_prompt': final_prompt, 'original_length': original_length, 'final_length': final_length, 'length_change_percent': length_change_percent, 'converged': converged, 'convergence_iteration': convergence_iteration, 'processing_time_seconds': processing_time}})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'stage': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(generate_events(), media_type="text/event-stream")
