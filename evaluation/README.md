# CAB Evaluation Tools

## Setup

```bash
pip install -r requirements.txt
```

## Set API Key

```bash
# OpenAI
export OPENAI_API_KEY="sk-your-key"

# Anthropic
export ANTHROPIC_API_KEY="your-key"

# Google
export GOOGLE_API_KEY="your-key"
```

## Run Benchmark

```bash
# Quick test (50 questions, ~5 min)
python run_benchmark.py --model gpt-4 --questions 50

# Standard test (200 questions, ~30-60 min)
python run_benchmark.py --model gpt-4 --questions 200

# Full benchmark (1,150 questions, ~4-8 hours)
python run_benchmark.py --model gpt-4 --full

# Specific dimensions only
python run_benchmark.py --model gpt-4 --dimensions "Pastoral Care" "Christian Ethics"

# Use different judge model
python run_benchmark.py --model gpt-3.5-turbo --judge gpt-4
```

## Output

Results saved to `cab_results.json` with:
- Per-question scores
- Dimension summaries
- Overall score and rating

## Supported Models

- OpenAI: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- Anthropic: claude-3-opus, claude-3-sonnet
- Google: gemini-pro
- Any OpenAI-compatible API
