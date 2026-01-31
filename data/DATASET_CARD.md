---
license: cc-by-sa-4.0
task_categories:
  - question-answering
  - text-classification
language:
  - en
tags:
  - christianity
  - theology
  - benchmark
  - llm-evaluation
  - faith-ai
  - pastoral-care
size_categories:
  - 1K<n<10K
---

# Christian AI Benchmark (CAB) v2.0

## Dataset Description

CAB is a comprehensive benchmark for evaluating AI alignment with Christian faith across 10 theological dimensions and 10 denominational traditions.

### Dataset Summary

- **Total Questions:** 1,150
- **Dimensions:** 10 (theology-focused)
- **Traditions:** 10 (Catholic, Orthodox, Protestant denominations)
- **Scoring Modes:** Objective (21%), Subjective (79%)
- **License:** CC BY-SA 4.0

### Why CAB?

Unlike Gloo's FAI-C benchmark (807 hidden questions), CAB offers:
- ✅ All questions published
- ✅ All rubrics published  
- ✅ No conflict of interest (we don't sell AI)
- ✅ 10 theological dimensions (vs 7 secular-adapted)
- ✅ 10 denominational traditions (vs undifferentiated)

## Dataset Structure

```python
{
  "id": "CAB-0001",
  "scoring_mode": "objective" | "subjective",
  "dimension": "Pastoral Care",
  "tradition": "Catholic",
  "difficulty": "L1" | "L2" | "L3",
  "question": "...",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],  # for objective
  "correct_answer": "B",  # for objective
  "scenario": "...",  # for subjective
  "evaluation_rubric": {...},
  "tags": ["grief", "crisis"]
}
```

## Usage

```python
from datasets import load_dataset

# Load the dataset
cab = load_dataset("SoliDeoGloria/CAB")

# Filter by dimension
pastoral = [q for q in cab["train"] if q["dimension"] == "Pastoral Care"]

# Filter by tradition
catholic = [q for q in cab["train"] if q["tradition"] == "Catholic"]
```

## Dimensions

| Dimension | Questions | Focus |
|-----------|:---------:|-------|
| Pastoral Care | 200 | Crisis, grief, boundaries |
| Biblical Literacy | 150 | Scripture, hermeneutics |
| Systematic Theology | 150 | Doctrine, Christology |
| Christian Ethics | 150 | Bioethics, social ethics |
| Church History | 100 | Councils, Reformation |
| Worship & Sacraments | 100 | Liturgy, sacraments |
| Apologetics | 100 | Philosophy, objections |
| Spiritual Formation | 80 | Disciplines, growth |
| Denominational Awareness | 70 | Fair representation |
| Boundary Respect | 50 | AI limitations |

## Citation

```bibtex
@misc{cab2026,
  title={Christian AI Benchmark (CAB) v2.0},
  author={{Soli Deo Gloria Research Initiative}},
  year={2026},
  publisher={Eldest AI LLC dba GoldRock AI},
  url={https://SoliDeoGloria.ai}
}
```

## License

CC BY-SA 4.0

## Contact

- Website: https://SoliDeoGloria.ai
- GitHub: https://github.com/SoliDeoGloria-ai/CAB
- Email: contact@SoliDeoGloria.ai
