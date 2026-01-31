<p align="center">
  <img src="assets/cab-logo.png" alt="Christian AI Benchmark" width="200"/>
</p>

<h1 align="center">Christian AI Benchmark (CAB) v2.0</h1>

<p align="center">
  <strong>The most comprehensive open-source framework for evaluating AI alignment with Christian faith</strong>
</p>

<p align="center">
  <a href="https://SoliDeoGloria.ai">Website</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="docs/specification.md">Specification</a> •
  <a href="docs/gloo-comparison.md">vs Gloo FAI-C</a> •
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/questions-1,150-blue" alt="Questions"/>
  <img src="https://img.shields.io/badge/dimensions-10-green" alt="Dimensions"/>
  <img src="https://img.shields.io/badge/traditions-10-purple" alt="Traditions"/>
  <img src="https://img.shields.io/badge/transparency-100%25-brightgreen" alt="Transparency"/>
  <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-orange" alt="License"/>
</p>

---

## Why CAB?

As AI increasingly serves as a de facto spiritual advisor, the Christian community needs transparent, conflict-free evaluation standards.

| Problem | CAB Solution |
|---------|--------------|
| Existing benchmarks hide their questions | **All 1,150 questions published** |
| Benchmark creators sell AI products | **No commercial AI products** |
| Generic "flourishing" dimensions | **10 theology-focused dimensions** |
| Christianity treated as monolithic | **10 denominational traditions** |
| Rubrics and methodology hidden | **Everything open source** |

---

## Quick Comparison: CAB vs Gloo FAI-C

| Feature | Gloo FAI-C | CAB v2.0 |
|---------|:----------:|:--------:|
| Questions | 807 (hidden) | **1,150 (public)** |
| Transparency | Closed | **100% open** |
| Conflict of Interest | Yes (Gloo sells AI) | **None** |
| Dimensions | 7 (secular-adapted) | **10 (theological)** |
| Denominations | Undifferentiated | **10 traditions** |
| Rubrics | Hidden | **Published** |
| Code | Closed | **Open source** |

[Detailed comparison →](docs/gloo-comparison.md)

---

## The 10 Dimensions

| Dimension | Questions | Focus |
|-----------|:---------:|-------|
| **Pastoral Care** | 200 | Crisis, grief, spiritual direction, boundaries |
| **Biblical Literacy** | 150 | Scripture, hermeneutics, interpretation |
| **Systematic Theology** | 150 | Doctrine, Trinity, Christology, soteriology |
| **Christian Ethics** | 150 | Bioethics, sexuality, social justice |
| **Church History** | 100 | Councils, Reformation, movements |
| **Worship & Sacraments** | 100 | Liturgy, Eucharist, baptism, prayer |
| **Apologetics** | 100 | Philosophy, objections, science/faith |
| **Spiritual Formation** | 80 | Disciplines, contemplation, growth |
| **Denominational Awareness** | 70 | Fair representation of traditions |
| **Boundary Respect** | 50 | AI limitations, appropriate referrals |

---

## Quick Start

```bash
# Clone
git clone https://github.com/SoliDeoGloria-ai/CAB.git
cd CAB

# Install
pip install -r evaluation/requirements.txt

# Set API key
export OPENAI_API_KEY="your-key"

# Run (50 questions, ~5 min)
python evaluation/run_benchmark.py --model gpt-4 --questions 50

# Full benchmark (1,150 questions, ~4-8 hours)
python evaluation/run_benchmark.py --model gpt-4 --full
```

---

## Score Interpretation

| Score | Rating | Meaning |
|:-----:|--------|---------|
| 90-100 | 🟢 Exceptional | Safe for pastoral applications |
| 75-89 | 🔵 Proficient | Good for general education |
| 60-74 | 🟡 Adequate | Requires human oversight |
| <60 | 🔴 Deficient | Not recommended for ministry |

We use **geometric mean** scoring—models cannot hide weaknesses.

---

## Repository Structure

```
CAB/
├── data/
│   ├── CAB_v2_Complete.json    # All 1,150 questions
│   └── CAB_v2_Complete.xlsx    # Excel with summaries
├── docs/
│   ├── specification.md        # Full technical spec
│   ├── methodology.md          # Scoring details
│   ├── gloo-comparison.md      # vs Gloo FAI-C
│   └── dimensions.md           # Dimension descriptions
├── evaluation/
│   ├── run_benchmark.py        # Evaluation script
│   └── requirements.txt
├── paper/
│   ├── CAB_Whitepaper.pdf
│   └── CAB_One_Pager.pdf
└── README.md
```

---

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

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

- 📝 Review and improve questions
- 🌍 Translate to other languages
- 🔧 Improve evaluation tooling
- 📊 Run validation studies

---

## License

[CC BY-SA 4.0](LICENSE) — Free to use, modify, share with attribution.

---

<p align="center">
  <strong>Developed by <a href="https://SoliDeoGloria.ai">Soli Deo Gloria Research Initiative</a></strong><br/>
  A project of Eldest AI LLC dba GoldRock AI<br/><br/>
  <em>Soli Deo Gloria</em> — To God Alone Be the Glory
</p>
