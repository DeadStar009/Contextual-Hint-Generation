from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_time_spent_minutes(timestamp: datetime) -> float:
    """Calculate time spent in minutes, handling both timezone-aware and naive datetimes."""
    now = datetime.now(timestamp.tzinfo) if timestamp.tzinfo else datetime.now()
    return (now - timestamp).total_seconds() / 60

class HintPipeline:
    def __init__(self):
        # Initialize different models for different tasks
        self.classifier_model = HuggingFaceEndpoint(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
            temperature=0.3,
            max_new_tokens=50,
        )
        
        self.hint_generator_model = HuggingFaceEndpoint(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
            temperature=0.7,
            max_new_tokens=500,
        )
        
        self.hint_verifier_model = HuggingFaceEndpoint(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
            temperature=0.5,
            max_new_tokens=200,
        )

        # Initialize prompt templates
        self.classifier_template = """You are an expert programming tutor. Your task is to analyze the student's current state and determine what type of hint would be most helpful.

Context:
- Problem: {problem}
- Current code: {code}
- Time spent: {time_spent:.1f} minutes
- Previous hints: {previous_hints}

Based on this context, classify what type of hint would be most helpful:
1. Conceptual Understanding: The student needs help understanding the core concepts
2. Implementation Guidance: The student understands the concept but needs help with implementation
3. Error Correction: The student has code but needs help fixing errors
4. Optimization Suggestion: The code works but could be improved
5. Testing/Edge Cases: The student needs help with testing or edge cases

Provide your classification as a number (1-5) followed by a brief explanation.

Classification:"""

        self.generator_template = """You are an expert programming tutor helping a student solve a coding problem. Provide a helpful hint that guides them toward the solution without giving it away completely.

Context:
- Problem: {problem}
- Current code: {code}
- Time spent: {time_spent:.1f} minutes
- Previous hints: {previous_hints}
- Hint type needed: {hint_type}

Rules for hint generation:
1. Never provide complete solutions
2. Focus on the specific hint type needed
3. Use the Socratic method - guide through questions
4. Build on previous hints if any
5. Keep hints concise and clear
6. For code examples, use only small snippets or pseudocode

Generate a hint:"""

        self.verifier_template = """You are a programming tutor verifying a hint before giving it to a student. Ensure the hint is helpful but doesn't give away too much.

Original hint: {hint}

Context:
- Problem: {problem}
- Current code: {code}
- Previous hints: {previous_hints}

First, verify that the hint:
1. Doesn't reveal the complete solution
2. Is clear and understandable
3. Is appropriate for the student's level
4. Builds on previous hints
5. Maintains appropriate difficulty

Then, do ONE of the following:
- If the hint is good as is, return EXACTLY the original hint
- If the hint needs improvement, return ONLY your improved version

DO NOT include any explanation or verification checklist in your response.
Return ONLY the final hint."""

        # Initialize LangChain
        self.classifier_chain = LLMChain(
            llm=self.classifier_model,
            prompt=PromptTemplate(
                template=self.classifier_template,
                input_variables=["problem", "code", "time_spent", "previous_hints"]
            )
        )

        self.generator_chain = LLMChain(
            llm=self.hint_generator_model,
            prompt=PromptTemplate(
                template=self.generator_template,
                input_variables=["problem", "code", "time_spent", "previous_hints", "hint_type"]
            )
        )

        self.verifier_chain = LLMChain(
            llm=self.hint_verifier_model,
            prompt=PromptTemplate(
                template=self.verifier_template,
                input_variables=["hint", "problem", "code", "previous_hints"]
            )
        )

    async def classify_hint_type(self, problem, code, timestamp, previous_hints):
        time_spent = get_time_spent_minutes(timestamp)
        result = await self.classifier_chain.arun(
            problem=problem,
            code=code,
            time_spent=time_spent,
            previous_hints=", ".join(previous_hints) if previous_hints else "None"
        )
        return result.strip()

    async def generate_hint(self, problem, code, timestamp, previous_hints, hint_type):
        time_spent = get_time_spent_minutes(timestamp)
        hint = await self.generator_chain.arun(
            problem=problem,
            code=code,
            time_spent=time_spent,
            previous_hints=", ".join(previous_hints) if previous_hints else "None",
            hint_type=hint_type
        )
        return hint.strip()

    async def verify_hint(self, hint, problem, code, previous_hints):
        result = await self.verifier_chain.arun(
            hint=hint,
            problem=problem,
            code=code,
            previous_hints=", ".join(previous_hints) if previous_hints else "None"
        )
        return result.strip() 