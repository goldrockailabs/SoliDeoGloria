# CAB Dataset

## Files

| File | Format | Description |
|------|--------|-------------|
| `CAB_v2_Complete.json` | JSON | Full dataset with all metadata |
| `CAB_v2_Complete.xlsx` | Excel | Spreadsheet with summary sheets |

## JSON Structure

```json
{
  "benchmark": "Christian AI Benchmark (CAB)",
  "version": "2.0",
  "total_questions": 1150,
  "questions": [
    {
      "id": "CAB-0001",
      "scoring_mode": "objective|subjective",
      "dimension": "Pastoral Care",
      "tradition": "Catholic",
      "difficulty": "L1|L2|L3",
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "B",
      "evaluation_rubric": {...},
      "tags": ["grief", "crisis"]
    }
  ]
}
```

## Statistics

- **Total Questions:** 1,150
- **Objective:** 244 (21%)
- **Subjective:** 906 (79%)
- **Difficulty:** L1 (23%), L2 (53%), L3 (24%)

## License

CC BY-SA 4.0 - Eldest AI LLC dba GoldRock AI
