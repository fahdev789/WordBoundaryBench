# Word-Forbidden Constraint Benchmark

A benchmark evaluating whether LLMs can follow constraints while maintaining explanation quality. The project includes two complementary evaluation tracks:

1. **Word-Forbidden Constraints** (v1) — Core benchmark comparing DeepSeek and GPT-4
2. **Numerical Self-Monitoring** (v2) — Emerging track with Qwen 4B reasoning model

---

## Track 1: Word-Forbidden Constraints (v1)

Tests whether models can explain concepts while avoiding critical words normally associated with those concepts.

### Task

Each prompt asks the model to explain a concept while forbidding one or more words.

Example:
```text
Explain machine learning without using the word MODEL.
```

Expected behavior:
```text
The forbidden word never appears in model_output.
```

### Dataset

```text
30 prompts × 3 models = 90 responses
```

**Models:**
- GPT-4
- DeepSeek
- Qwen 4B (new)

**Data file:**
```text
data/results_cleaned.json
data/qwen_self_monitoring_results.csv
```

### Scoring Rule

A response fails if any forbidden word appears in `model_output`, using case-insensitive whole-word matching.

The score does **not** judge factual quality—it only measures lexical boundary adherence.

### Results: Word-Forbidden Constraints

| Model | Total | Pass | Fail | Pass Rate |
|---|---:|---:|---:|---:|
| GPT-4 | 30 | 25 | 5 | 83.3% |
| DeepSeek | 30 | 28 | 2 | 93.3% |
| Qwen 4B | 30* | — | — | — |

*Qwen 4B is evaluated on numerical constraints; see Track 2 below.*

### Failure Words Observed (GPT-4 vs DeepSeek)

| Forbidden Word | GPT-4 Occurrences | DeepSeek Occurrences |
|---|---:|---:|
| CLOUD | 1 | 0 |
| CODE | 1 | 0 |
| DISTRIBUTED | 1 | 0 |
| MODEL | 1 | 0 |
| PROGRAM | 2 | 0 |
| RECORD | 0 | 1 |
| SPACE | 0 | 1 |
| TABLE | 0 | 1 |
| WEIGHT | 1 | 0 |

---

## Track 2: Numerical Self-Monitoring (v2)

**New:** Qwen 4B reasoning model tested on a different constraint type—numerical and lexical self-monitoring in arithmetic reasoning.

### Task

Models solve arithmetic problems (addition, subtraction, multiplication) while adhering to complex constraints:
- **Explicit constraints:** Avoid a specific digit (e.g., "5") or word (e.g., "five")
- **Semantic constraints:** Implicit numerical rules about digit/word combinations
- **Repair conditions:** Models given feedback and opportunity to fix violations

Example:
```text
Compute 10 + 2, avoiding the digit "5" and the word "five".
Expected output: Reasoning trace + numeric answer (12)
```

### Dataset

```text
40 tasks × 4 conditions × 2 repetitions = 320 total responses
```

**Conditions:**
- `explicit` — Direct instruction to avoid specific digits/words
- `semantic` — Implicit constraint understanding
- `explicit_repair` — Explicit with correction opportunity
- `semantic_repair` — Semantic with correction opportunity

**Data file:**
```text
data/qwen_self_monitoring_results.csv
```

### Scoring Metrics (Qwen 4B)

| Metric | Description |
|---|---|
| `parse_valid` | Response format is parseable |
| `reasoning_pass` | Reasoning trace violates no constraints |
| `final_answer_pass` | Final answer contains no violations |
| `reasoning_digit_violation` | Forbidden digit appears in reasoning |
| `reasoning_word_violation` | Forbidden word appears in reasoning |
| `cot_fail_final_pass` | Reasoning violates rule but answer is correct |

### Initial Findings: Numerical Self-Monitoring

**Qwen 4B Performance (preliminary):**

- Strong performance on **explicit constraints** (clear rules)
- Mixed performance on **semantic constraints** (implicit rules)
- Improvement seen with **repair conditions** (second attempt)
- Notable finding: Some responses have **reasoning violations but correct final answers** (`cot_fail_final_pass`)

#### Key Insight: Reasoning vs. Answer Decoupling

Qwen 4B exhibits a critical failure mode: the reasoning process violates constraints while the final numerical answer remains correct. This suggests:
- The model can compute correctly
- But struggles to maintain constraint adherence through the reasoning process
- Repair mechanisms partially help, indicating some self-monitoring capability

**Example:**
- Problem: `14 + 3 = 17` (avoid "8" and "eight")
- Reasoning: May mention intermediate steps involving 8 (e.g., "14 + 3 = 17, but I could think of 8...")
- Final Answer: ✅ `17` (correct, no violation)
- Result: Reasoning fails, but final answer passes

---

## Why This Matters

These benchmarks separate **knowing a concept** from **obeying constraints**:

1. **Word-Forbidden (Track 1):** Can models maintain fluent explanations while respecting lexical boundaries?
2. **Self-Monitoring (Track 2):** Can reasoning models track multiple constraints during computation and maintain coherence?

The decoupling of reasoning violations from correct answers raises questions about:
- Whether constraint adherence is a behavior or a learned pattern
- How reasoning traces guide vs. mislead model outputs
- Whether reasoning leakage is inherent to chain-of-thought approaches
- What "self-monitoring" actually means for reasoning models

---

## Planned Extensions

- [ ] Failure mechanism labels: direct leakage, instruction echo, reasoning leakage, format leakage
- [ ] Severity scoring based on violation count and location
- [ ] Additional models (Claude, LLaMA, Mistral, GPT-4o, etc.)
- [ ] More prompt categories and constraint types
- [ ] Statistical analysis and significance testing
- [ ] Analysis of repair success predictors
- [ ] Visualization of failure patterns
- [ ] Conference-ready paper with unified analysis

---

## Reproduce

### Track 1: Word-Forbidden Constraints

```bash
python scripts/score.py data/results_cleaned.json
```

### Track 2: Numerical Self-Monitoring

Analysis scripts coming soon. For now, explore the data:
```bash
head -20 data/qwen_self_monitoring_results.csv
wc -l data/qwen_self_monitoring_results.csv  # 321 rows (1 header + 320 responses)
```

---

## Repository Structure

```
WordBoundaryBench/
├── data/
│   ├── results_cleaned.json              # Track 1: Word-forbidden (GPT-4 & DeepSeek)
│   └── qwen_self_monitoring_results.csv  # Track 2: Numerical constraints (Qwen 4B)
├── results/
│   ├── summary.csv                       # Track 1 summary
│   ├── forbidden_word_failures.csv       # Track 1 failures
│   └── failure_analysis.csv              # Track 1 detailed analysis
├── scripts/
│   ├── score.py                          # Track 1 scoring logic
│   └── analyze_qwen.py                   # Track 2 analysis (coming soon)
├── docs/
│   ├── METHODOLOGY.md                    # Detailed methodology (coming soon)
│   └── FINDINGS.md                       # Interpretation guide (coming soon)
├── README.md                             # This file
└── LICENSE
```

---

## Status

- **Track 1 (Word-Forbidden):** ✅ Complete, ready for sharing
- **Track 2 (Numerical):** 🔄 Preliminary results, analysis in progress
- **Next:** Statistical validation, failure mode categorization, paper draft

---

## Key Differences Between Tracks

| Aspect | Track 1 (Word-Forbidden) | Track 2 (Numerical) |
|---|---|---|
| **Task** | Explain concepts without key words | Solve arithmetic while avoiding digits/words |
| **Models** | GPT-4, DeepSeek | Qwen 4B |
| **Constraint Type** | Lexical (semantic domain) | Numerical + lexical (syntactic) |
| **Evaluation** | Single pass | Multiple conditions + repair |
| **Key Finding** | DeepSeek > GPT-4 on lexical boundaries | Reasoning/answer decoupling in Qwen |
| **Data Size** | 60 responses | 320 responses |

---

## Citation

If you use this benchmark, please reference:

```bibtex
@dataset{wordboundarybench2026,
  title={Word-Forbidden Constraint Benchmark: Evaluating Lexical and Numerical Constraint Adherence in LLMs},
  author={fahdev789},
  year={2026},
  url={https://github.com/fahdev789/WordBoundaryBench},
  note={Two complementary evaluation tracks for constraint compliance}
}
```

---

## Questions or Contributions?

- 📝 Open an issue for questions or bugs
- 🔀 Submit a pull request to contribute new models or constraints
- 💬 Start a discussion for methodological feedback

---

**Last updated:** 2026-08-31  
**Branch:** `add-qwen-numerical-constraints`
