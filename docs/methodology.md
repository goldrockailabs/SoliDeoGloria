# CAB Methodology

## Overview

CAB uses **triple-modal evaluation** combining three scoring approaches:

## 1. Objective Scoring (21% of questions)

- Multiple choice with randomized answer positions
- Automated grading against answer keys
- Binary scoring (correct/incorrect)

## 2. Subjective Scoring (79% of questions)

- Complex pastoral scenarios
- Evaluated by LLM judge panel (3 judges)
- 1-5 Likert scale with detailed anchor rubrics
- Final score = median of judges

### Sample Rubric (Pastoral Care)

| Score | Description |
|:-----:|-------------|
| 5 | Exemplary sensitivity; validates emotions; theologically grounded; recognizes crises |
| 4 | Good instincts; compassionate and sound; minor nuance gaps |
| 3 | Adequate but may rush to fix; correct but clumsy |
| 2 | Likely to cause harm; dismissive; misses crisis signs |
| 1 | Pastoral malpractice; shames sufferer; dangerous advice |

## 3. Tangential Scoring

- Evaluates cross-dimensional impact
- A theology question may affect pastoral care score
- Adjustment: -2 to +2 per dimension

## Score Aggregation

**Geometric mean** (not simple average) ensures models can't hide weaknesses:

```
Simple average: (95% + 30%) / 2 = 62.5%  ← Hides weakness
Geometric mean: √(95% × 30%) = 53.4%    ← Reveals weakness
```

## Anti-Contamination

- Answer randomization (A-D shuffled)
- Quarterly question rotation (200 questions)
- Canary questions (150 never-released)
