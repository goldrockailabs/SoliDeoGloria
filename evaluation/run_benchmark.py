#!/usr/bin/env python3
"""
CAB v2.0 - Benchmark Evaluation Runner
=====================================

This script runs the Christian AI Benchmark against any LLM and produces scores.

SIMPLE OVERVIEW:
1. Load the benchmark questions
2. Send each question to the model being tested
3. For OBJECTIVE questions: Check if answer matches (automatic scoring)
4. For SUBJECTIVE questions: Send response to judge LLMs for evaluation
5. Calculate dimension scores and overall score

REQUIREMENTS:
    pip install openai anthropic google-generativeai

USAGE:
    python run_cab_benchmark.py --model gpt-4 --questions 100
    python run_cab_benchmark.py --model claude-3-opus --full
    python run_cab_benchmark.py --model gemini-pro --sample
"""

import json
import os
import re
import time
import argparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from statistics import geometric_mean, median
import random

# ============================================================================
# CONFIGURATION - Add your API keys here or set as environment variables
# ============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key-here")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-anthropic-key-here")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your-google-key-here")

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class QuestionResult:
    question_id: str
    dimension: str
    scoring_mode: str
    model_response: str
    score: float
    max_score: float
    judge_scores: List[float] = None
    correct_answer: str = None
    model_answer: str = None

@dataclass 
class DimensionScore:
    dimension: str
    questions_answered: int
    total_score: float
    max_possible: float
    percentage: float

@dataclass
class BenchmarkResult:
    model_name: str
    total_questions: int
    dimension_scores: Dict[str, DimensionScore]
    overall_score: float
    rating: str
    timestamp: str

# ============================================================================
# MODEL CLIENTS - Simplified interfaces to major LLM providers
# ============================================================================

class ModelClient:
    """Base class for LLM API clients"""
    
    def query(self, prompt: str, system_prompt: str = None) -> str:
        raise NotImplementedError

class OpenAIClient(ModelClient):
    def __init__(self, model: str = "gpt-4"):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = model
        except ImportError:
            print("Install openai: pip install openai")
            raise
    
    def query(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2000,
            temperature=0.3
        )
        return response.choices[0].message.content

class AnthropicClient(ModelClient):
    def __init__(self, model: str = "claude-3-opus-20240229"):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            self.model = model
        except ImportError:
            print("Install anthropic: pip install anthropic")
            raise
    
    def query(self, prompt: str, system_prompt: str = None) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class GoogleClient(ModelClient):
    def __init__(self, model: str = "gemini-pro"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(model)
        except ImportError:
            print("Install google-generativeai: pip install google-generativeai")
            raise
    
    def query(self, prompt: str, system_prompt: str = None) -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.model.generate_content(full_prompt)
        return response.text

def get_client(model_name: str) -> ModelClient:
    """Factory function to get the right client for a model"""
    model_lower = model_name.lower()
    
    if "gpt" in model_lower or "openai" in model_lower:
        return OpenAIClient(model_name)
    elif "claude" in model_lower or "anthropic" in model_lower:
        return AnthropicClient(model_name)
    elif "gemini" in model_lower or "google" in model_lower:
        return GoogleClient(model_name)
    else:
        # Default to OpenAI-compatible API
        return OpenAIClient(model_name)

# ============================================================================
# SCORING FUNCTIONS
# ============================================================================

def score_objective_question(question: dict, model_response: str) -> Tuple[float, str]:
    """
    Score an objective (multiple choice) question.
    Returns (score, extracted_answer)
    
    HOW IT WORKS:
    1. Look for the model's answer choice (A, B, C, or D)
    2. Compare to the correct answer
    3. Return 1.0 for correct, 0.0 for incorrect
    """
    correct = question.get("correct_answer", "").strip().upper()
    
    # Extract answer from response - look for patterns like "A)", "Answer: B", etc.
    response_upper = model_response.upper()
    
    # Try various patterns
    patterns = [
        r'\b([A-D])\)',           # "A)" or "B)"
        r'ANSWER[:\s]+([A-D])',   # "Answer: A"
        r'CORRECT[:\s]+([A-D])',  # "Correct: A"  
        r'\b([A-D])\s+IS\s+CORRECT', # "A is correct"
        r'^([A-D])\b',            # Starts with letter
        r'\(([A-D])\)',           # "(A)"
    ]
    
    extracted = None
    for pattern in patterns:
        match = re.search(pattern, response_upper)
        if match:
            extracted = match.group(1)
            break
    
    # If no pattern matched, look for standalone letter
    if not extracted:
        for letter in ['A', 'B', 'C', 'D']:
            if letter in response_upper.split():
                extracted = letter
                break
    
    if extracted and extracted == correct:
        return 1.0, extracted
    else:
        return 0.0, extracted or "UNCLEAR"

def create_judge_prompt(question: dict, model_response: str) -> str:
    """
    Create the prompt for judge LLMs to evaluate a subjective response.
    
    HOW IT WORKS:
    1. Include the original question/scenario
    2. Include the rubric with anchor descriptions
    3. Include the model's response
    4. Ask for a 1-5 score with justification
    """
    rubric = question.get("evaluation_rubric", {})
    anchors = rubric.get("anchors", {})
    dimension = question.get("dimension", "Unknown")
    
    anchor_text = "\n".join([
        f"Score {score}: {desc}" 
        for score, desc in sorted(anchors.items(), reverse=True)
    ])
    
    prompt = f"""You are an expert evaluator for the Christian AI Benchmark, specializing in {dimension}.

TASK: Evaluate the following AI response to a pastoral/theological scenario.

SCENARIO:
{question.get('scenario', question.get('question', ''))}

AI RESPONSE TO EVALUATE:
{model_response}

SCORING RUBRIC (1-5 scale):
{anchor_text}

INSTRUCTIONS:
1. Read the scenario and response carefully
2. Consider theological accuracy, pastoral sensitivity, and practical helpfulness
3. Assign a score from 1-5 based on the rubric anchors above
4. Provide brief justification

Respond in this exact format:
SCORE: [1-5]
JUSTIFICATION: [Your reasoning in 2-3 sentences]"""

    return prompt

def score_subjective_question(
    question: dict, 
    model_response: str, 
    judge_client: ModelClient
) -> Tuple[float, List[float]]:
    """
    Score a subjective question using an LLM judge.
    Returns (final_score, list_of_judge_scores)
    
    HOW IT WORKS:
    1. Create evaluation prompt with rubric
    2. Send to judge LLM(s)
    3. Extract numeric score from judge response
    4. Return median of judge scores (if multiple judges)
    """
    judge_prompt = create_judge_prompt(question, model_response)
    
    # Get judge evaluation
    judge_response = judge_client.query(
        judge_prompt,
        system_prompt="You are a rigorous but fair theological evaluator."
    )
    
    # Extract score from response
    score_match = re.search(r'SCORE:\s*(\d)', judge_response)
    if score_match:
        score = float(score_match.group(1))
        score = max(1.0, min(5.0, score))  # Clamp to 1-5
    else:
        # Try to find any number 1-5
        numbers = re.findall(r'\b([1-5])\b', judge_response)
        score = float(numbers[0]) if numbers else 3.0  # Default to middle
    
    return score, [score]

# ============================================================================
# MAIN BENCHMARK RUNNER
# ============================================================================

class CABBenchmarkRunner:
    """
    Main class to run the CAB benchmark.
    
    PROCESS OVERVIEW:
    1. Load questions from JSON
    2. For each question:
       - Send to model being tested
       - Score the response (objective or subjective)
       - Record the result
    3. Calculate dimension scores
    4. Calculate overall score using geometric mean
    5. Generate report
    """
    
    def __init__(self, questions_file: str):
        with open(questions_file, 'r') as f:
            data = json.load(f)
        self.questions = data.get('questions', data)
        self.results: List[QuestionResult] = []
        
    def run(
        self, 
        model_client: ModelClient,
        judge_client: ModelClient,
        num_questions: int = None,
        dimensions: List[str] = None,
        verbose: bool = True
    ) -> BenchmarkResult:
        """
        Run the benchmark.
        
        Args:
            model_client: Client for the model being tested
            judge_client: Client for the judge LLM (can be same or different)
            num_questions: Limit number of questions (None = all)
            dimensions: Filter to specific dimensions (None = all)
            verbose: Print progress
        """
        # Filter questions if needed
        questions = self.questions
        if dimensions:
            questions = [q for q in questions if q['dimension'] in dimensions]
        if num_questions:
            questions = questions[:num_questions]
        
        total = len(questions)
        if verbose:
            print(f"\n{'='*60}")
            print(f"Running CAB v2.0 Benchmark")
            print(f"Questions: {total}")
            print(f"{'='*60}\n")
        
        for i, question in enumerate(questions):
            if verbose:
                print(f"[{i+1}/{total}] {question['id']} ({question['dimension']})...", end=" ")
            
            try:
                # Get model response
                if question['scoring_mode'] == 'objective':
                    prompt = self._format_objective_prompt(question)
                else:
                    prompt = self._format_subjective_prompt(question)
                
                response = model_client.query(prompt)
                
                # Score the response
                if question['scoring_mode'] == 'objective':
                    score, answer = score_objective_question(question, response)
                    result = QuestionResult(
                        question_id=question['id'],
                        dimension=question['dimension'],
                        scoring_mode='objective',
                        model_response=response,
                        score=score,
                        max_score=1.0,
                        correct_answer=question.get('correct_answer'),
                        model_answer=answer
                    )
                else:
                    score, judge_scores = score_subjective_question(
                        question, response, judge_client
                    )
                    result = QuestionResult(
                        question_id=question['id'],
                        dimension=question['dimension'],
                        scoring_mode='subjective',
                        model_response=response,
                        score=score,
                        max_score=5.0,
                        judge_scores=judge_scores
                    )
                
                self.results.append(result)
                
                if verbose:
                    if question['scoring_mode'] == 'objective':
                        status = "✓" if score == 1.0 else "✗"
                        print(f"{status} ({answer})")
                    else:
                        print(f"Score: {score}/5")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                if verbose:
                    print(f"ERROR: {e}")
                continue
        
        return self._calculate_final_scores()
    
    def _format_objective_prompt(self, question: dict) -> str:
        """Format prompt for objective questions"""
        options = "\n".join(question.get('options', []))
        return f"""Answer the following multiple choice question. 
Respond with ONLY the letter of the correct answer (A, B, C, or D).

Question: {question['question']}

{options}

Your answer (letter only):"""

    def _format_subjective_prompt(self, question: dict) -> str:
        """Format prompt for subjective questions"""
        scenario = question.get('scenario', question.get('question', ''))
        return f"""You are a knowledgeable Christian assistant. Please respond thoughtfully to the following:

{scenario}

Provide a helpful, theologically informed, and pastorally sensitive response."""

    def _calculate_final_scores(self) -> BenchmarkResult:
        """
        Calculate dimension and overall scores.
        
        METHODOLOGY:
        1. Group results by dimension
        2. For each dimension: (total_earned / total_possible) * 100
        3. Overall score: GEOMETRIC MEAN of dimension percentages
           (This prevents compensation - can't offset bad Pastoral Care with good Biblical Literacy)
        """
        # Group by dimension
        dim_results: Dict[str, List[QuestionResult]] = {}
        for result in self.results:
            dim = result.dimension
            if dim not in dim_results:
                dim_results[dim] = []
            dim_results[dim].append(result)
        
        # Calculate dimension scores
        dimension_scores = {}
        dim_percentages = []
        
        for dim, results in dim_results.items():
            total_score = sum(r.score for r in results)
            max_possible = sum(r.max_score for r in results)
            percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
            
            dimension_scores[dim] = DimensionScore(
                dimension=dim,
                questions_answered=len(results),
                total_score=total_score,
                max_possible=max_possible,
                percentage=percentage
            )
            dim_percentages.append(max(1, percentage))  # Avoid 0 in geometric mean
        
        # Calculate overall score (geometric mean)
        if dim_percentages:
            overall = geometric_mean(dim_percentages)
        else:
            overall = 0
        
        # Determine rating
        if overall >= 90:
            rating = "Exceptional"
        elif overall >= 75:
            rating = "Proficient"
        elif overall >= 60:
            rating = "Adequate"
        else:
            rating = "Deficient"
        
        return BenchmarkResult(
            model_name="Unknown",  # Set externally
            total_questions=len(self.results),
            dimension_scores=dimension_scores,
            overall_score=overall,
            rating=rating,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )

# ============================================================================
# REPORT GENERATION
# ============================================================================

def print_report(result: BenchmarkResult, model_name: str):
    """Print a formatted benchmark report"""
    print("\n" + "="*70)
    print("CHRISTIAN AI BENCHMARK (CAB) v2.0 - EVALUATION REPORT")
    print("="*70)
    print(f"\nModel Evaluated: {model_name}")
    print(f"Timestamp: {result.timestamp}")
    print(f"Questions Answered: {result.total_questions}")
    
    print("\n" + "-"*70)
    print("DIMENSION SCORES")
    print("-"*70)
    print(f"{'Dimension':<30} {'Questions':>10} {'Score':>15} {'Percentage':>12}")
    print("-"*70)
    
    for dim, score in sorted(result.dimension_scores.items()):
        pct_str = f"{score.percentage:.1f}%"
        score_str = f"{score.total_score:.1f}/{score.max_possible:.1f}"
        print(f"{dim:<30} {score.questions_answered:>10} {score_str:>15} {pct_str:>12}")
    
    print("-"*70)
    print(f"\n{'OVERALL SCORE (Geometric Mean):':<40} {result.overall_score:.1f}/100")
    print(f"{'RATING:':<40} {result.rating}")
    
    # Interpretation
    print("\n" + "-"*70)
    print("INTERPRETATION")
    print("-"*70)
    if result.rating == "Exceptional":
        print("✓ Suitable for sensitive pastoral applications and seminary education")
    elif result.rating == "Proficient":
        print("✓ Good for general Christian education and basic Q&A")
    elif result.rating == "Adequate":
        print("⚠ Low-stakes use only; requires human oversight for pastoral matters")
    else:
        print("✗ Not recommended for ministry contexts; may cause spiritual harm")
    
    print("\n" + "="*70)

def save_detailed_results(results: List[QuestionResult], filename: str):
    """Save detailed results to JSON for analysis"""
    output = []
    for r in results:
        output.append({
            "question_id": r.question_id,
            "dimension": r.dimension,
            "scoring_mode": r.scoring_mode,
            "score": r.score,
            "max_score": r.max_score,
            "model_response": r.model_response[:500] + "..." if len(r.model_response) > 500 else r.model_response,
            "judge_scores": r.judge_scores,
            "correct_answer": r.correct_answer,
            "model_answer": r.model_answer
        })
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nDetailed results saved to: {filename}")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run CAB v2.0 Benchmark against an LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
    # Run 50 sample questions against GPT-4
    python run_cab_benchmark.py --model gpt-4 --questions 50

    # Run full benchmark against Claude
    python run_cab_benchmark.py --model claude-3-opus-20240229 --full
    
    # Run only Pastoral Care dimension
    python run_cab_benchmark.py --model gpt-4 --dimensions "Pastoral Care"
    
    # Use different judge model
    python run_cab_benchmark.py --model gpt-3.5-turbo --judge gpt-4
        """
    )
    
    parser.add_argument("--model", required=True, help="Model to evaluate (e.g., gpt-4, claude-3-opus)")
    parser.add_argument("--judge", default=None, help="Model to use as judge (default: same as --model)")
    parser.add_argument("--questions", type=int, default=50, help="Number of questions to run (default: 50)")
    parser.add_argument("--full", action="store_true", help="Run all 1,150 questions")
    parser.add_argument("--dimensions", nargs="+", help="Filter to specific dimensions")
    parser.add_argument("--dataset", default="CAB_v2_Complete_Dataset.json", help="Path to dataset JSON")
    parser.add_argument("--output", default="cab_results.json", help="Output file for detailed results")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    # Initialize clients
    print(f"Initializing model client for: {args.model}")
    model_client = get_client(args.model)
    
    judge_model = args.judge or args.model
    print(f"Initializing judge client for: {judge_model}")
    judge_client = get_client(judge_model)
    
    # Load and run benchmark
    print(f"Loading dataset: {args.dataset}")
    runner = CABBenchmarkRunner(args.dataset)
    
    num_questions = None if args.full else args.questions
    
    result = runner.run(
        model_client=model_client,
        judge_client=judge_client,
        num_questions=num_questions,
        dimensions=args.dimensions,
        verbose=not args.quiet
    )
    
    # Output results
    print_report(result, args.model)
    save_detailed_results(runner.results, args.output)

if __name__ == "__main__":
    main()
