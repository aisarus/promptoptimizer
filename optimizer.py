import textwrap
from typing import Optional
from ..models.schemas import (
    SmartQueueResult,
    PCVResult,
    DSIteration,
    PairwiseEvaluation,
)
from ..services.llm_provider import LLMProvider
from ..utils.json_parser import safe_json_from_llm, approximate_length


class PromptOptimizer:
    """Main service for prompt optimization pipeline"""
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
    
    def smart_queue(self, prompt: str) -> SmartQueueResult:
        """Analyze prompt quality and decide if optimization is needed"""
        system = textwrap.dedent(
            """
            You are a prompt quality analyzer.

            Task:
            - Evaluate the user's prompt on three axes:
              1) clarity (0..1)
              2) structure (0..1)
              3) constraints (0..1)

            - Decide if optimization is recommended.

            Respond ONLY with a JSON object:
            {
              "clarity": float,
              "structure": float,
              "constraints": float,
              "needs_optimization": bool,
              "comment": "short English string"
            }
            No code fences, no extra text.
            """
        )
        
        raw = self.provider.call(system, prompt)
        data = safe_json_from_llm(raw)
        
        if data is None:
            data = {
                "clarity": 0.5,
                "structure": 0.5,
                "constraints": 0.5,
                "needs_optimization": True,
                "comment": f"[parser failed, model said]: {str(raw)[:400]}",
            }
        
        return SmartQueueResult(
            clarity=data.get("clarity", 0.5),
            structure=data.get("structure", 0.5),
            constraints=data.get("constraints", 0.5),
            needs_optimization=data.get("needs_optimization", True),
            comment=data.get("comment", "")
        )
    
    def proposer_step(self, prompt: str) -> str:
        """Rewrite prompt with better structure (Proposer phase)"""
        system = textwrap.dedent(
            """
            You are the PROPOSER in a Proposer–Critic–Verifier loop.

            Task:
            - Rewrite the user prompt into a clearer, more structured LLM instruction.
            - Preserve the original intent.
            - Add explicit structure (steps, sections), constraints, and output format where helpful.
            - Do NOT answer the task, only rewrite the prompt.
            """
        )
        return self.provider.call(system, prompt)
    
    def critic_step(self, proposed_prompt: str) -> str:
        """Analyze proposed prompt and suggest improvements (Critic phase)"""
        system = textwrap.dedent(
            """
            You are the CRITIC in a Proposer–Critic–Verifier loop.

            Task:
            - Analyse the proposed LLM prompt.
            - Identify issues in:
              - clarity
              - completeness
              - specificity
              - constraints
              - structure

            Output:
            - A short, numbered list of concrete improvements that should be applied to the prompt.
            - Write in English.
            """
        )
        return self.provider.call(system, proposed_prompt)
    
    def verifier_step(self, original_prompt: str, proposed_prompt: str, critique: str) -> str:
        """Create final verified prompt (Verifier phase)"""
        system = textwrap.dedent(
            """
            You are the VERIFIER in a Proposer–Critic–Verifier loop.

            Task:
            - You receive:
              1) the original user prompt,
              2) a proposed improved prompt,
              3) a critique of the proposed prompt.

            - Produce a final, polished prompt that:
              - Preserves the original user's intent.
              - Applies critique suggestions where they make sense.
              - Removes redundancy, improves clarity, adds missing constraints.

            Output:
            - Return ONLY the final improved prompt text.
            - Do NOT include explanations or meta-commentary.
            """
        )
        
        user = textwrap.dedent(
            f"""
            ORIGINAL PROMPT:
            {original_prompt}

            PROPOSED PROMPT:
            {proposed_prompt}

            CRITIQUE:
            {critique}
            """
        )
        
        return self.provider.call(system, user)
    
    def run_pcv(self, prompt: str) -> PCVResult:
        """Run full Proposer-Critic-Verifier cycle"""
        proposed = self.proposer_step(prompt)
        critique = self.critic_step(proposed)
        final = self.verifier_step(prompt, proposed, critique)
        
        return PCVResult(
            proposed_prompt=proposed,
            critique=critique,
            final_prompt=final
        )
    
    def d_block(self, prompt: str) -> str:
        """Diversification step - expand the prompt"""
        system = textwrap.dedent(
            """
            You are in the DIVERSIFICATION (D) phase of a D/S cycle.

            Task:
            - Take the given prompt and expand it with:
              - More detailed instructions
              - Additional constraints or edge cases
              - Clarifications on ambiguous points
              - Examples if helpful

            - Do NOT change the core intent.
            - Output ONLY the expanded prompt text.
            """
        )
        return self.provider.call(system, prompt)
    
    def s_block(self, prompt: str) -> str:
        """Stabilization step - refine and consolidate"""
        system = textwrap.dedent(
            """
            You are in the STABILIZATION (S) phase of a D/S cycle.

            Task:
            - Take the (potentially verbose) prompt and:
              - Remove redundancy
              - Improve coherence
              - Ensure clarity
              - Keep all important details

            Output:
            - Return ONLY the stabilized prompt text.
            """
        )
        return self.provider.call(system, prompt)
    
    def run_ds_cycle(
        self,
        initial_prompt: str,
        max_iterations: int = 3,
        convergence_threshold: float = 0.05
    ) -> tuple[str, list[DSIteration], bool, Optional[int]]:
        """
        Run D/S (Diversification/Stabilization) cycle
        
        Returns:
            - final_prompt: str
            - iterations: list of DSIteration
            - converged: bool
            - convergence_iteration: Optional[int]
        """
        current = initial_prompt
        iterations = []
        prev_len = approximate_length(current)
        converged = False
        convergence_iteration = None
        
        for i in range(1, max_iterations + 1):
            d_out = self.d_block(current)
            s_out = self.s_block(d_out)
            
            current = s_out
            cur_len = approximate_length(current)
            change_rate = abs(cur_len - prev_len) / max(prev_len, 1)
            
            iterations.append(
                DSIteration(
                    iteration=i,
                    d_block_output=d_out,
                    s_block_output=s_out,
                    length=cur_len,
                    change_rate=change_rate
                )
            )
            
            prev_len = cur_len
            
            if change_rate < convergence_threshold:
                converged = True
                convergence_iteration = i
                break
        
        return current, iterations, converged, convergence_iteration
    
    def pairwise_eval(self, original_prompt: str, final_prompt: str) -> PairwiseEvaluation:
        """Compare original vs final prompt"""
        system = textwrap.dedent(
            """
            You are an evaluator for prompt quality.

            Compare ORIGINAL and FINAL prompts along 4 axes:
            - clarity
            - structure
            - constraints
            - overall usefulness for an LLM

            For each axis, assign a vote:
            - +1.0  = FINAL is much better
            - +0.66 = FINAL is moderately better
            - +0.33 = FINAL is slightly better
            - 0.0   = similar
            - -0.33 = ORIGINAL slightly better
            - -0.66 = ORIGINAL moderately better
            - -1.0  = ORIGINAL much better

            Respond ONLY with a JSON object (no code fences, no extra text), for example:
            {
              "clarity": 1.0,
              "structure": 0.66,
              "constraints": 0.33,
              "usefulness": 1.0,
              "comment": "short English explanation"
            }
            """
        )
        
        user = textwrap.dedent(
            f"""
            ORIGINAL PROMPT:
            {original_prompt}

            FINAL PROMPT:
            {final_prompt}
            """
        )
        
        raw = self.provider.call(system, user)
        data = safe_json_from_llm(raw)
        
        if data is None:
            data = {
                "clarity": 0.0,
                "structure": 0.0,
                "constraints": 0.0,
                "usefulness": 0.0,
                "comment": f"[parser failed, model said]: {str(raw)[:400]}",
            }
        
        return PairwiseEvaluation(
            clarity=data.get("clarity", 0.0),
            structure=data.get("structure", 0.0),
            constraints=data.get("constraints", 0.0),
            usefulness=data.get("usefulness", 0.0),
            comment=data.get("comment", "")
        )
