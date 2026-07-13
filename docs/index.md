# WordBoundaryBench: Repository Index

**WordBoundaryBench** evaluates whether Large Language Models (LLMs) can follow word-forbidden constraints while explaining concepts. Inspired by findings from "Reasoning Models Struggle with Chain[...]

---

## Quick Navigation

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Key Files](#key-files)
- [How to Use](#how-to-use)
- [Results Summary](#results-summary)
- [Technical Details](#technical-details)
- [Citations](#citations)

---

## Overview

### Purpose
This benchmark tests a simple but fundamental capability: can LLMs explain a concept while adhering to a lexical constraint (avoiding specified words)?

### Key Metrics
- **Task**: Explain concepts without using forbidden words
- **Dataset**: 30 matched prompts × 2 models = 60 responses
- **Models Evaluated**: GPT-4, DeepSeek
- **Scoring**: Case-insensitive whole-word matching (lexical boundary adherence only)

### Current Results (v1)

| Model | Total | Pass | Fail | Pass Rate |
|-------|------:|-----:|-----:|----------:|
| DeepSeek | 30 | 28 | 2 | 93.3% |
| GPT-4 | 30 | 25 | 5 | 83.3% |

---

## Repository Structure

```
WordBoundaryBench/
├── README.md                          # Main overview and results
├── LICENSE                            # MIT License
├── docs/
│   └── index.md                       # This file (live site)
│
├── data/
│   └── results_cleaned.json           # Full dataset: 60 responses with prompts & outputs
│
├── scripts/
│   └── score.py                       # Scoring script: evaluates constraint adherence
│
└── results/
    ├── summary.csv                    # Model-level summary (pass/fail/violation counts)
    ├── forbidden_word_failures.csv    # Which forbidden words violated and by which model
    └── failure_analysis.csv           # Detailed per-prompt failure analysis
```

---

## Key Files

### `data/results_cleaned.json`
The complete dataset containing:
- **Prompts**: 30 explanation tasks with forbidden word constraints
- **Model Outputs**: Responses from GPT-4 and DeepSeek
- **Size**: ~216 KB

**Structure** (per item):
```json
{
  "prompt": "Explain [concept] without using [forbidden words]",
  "model": "GPT-4" | "DeepSeek",
  "model_output": "..." // The full response to evaluate
}
```

### `scripts/score.py`
**Purpose**: Evaluate all responses and generate constraint adherence metrics

**Key Functions**:
- `extract_forbidden_words(prompt)`: Parses forbidden words from prompt using regex
- `count_whole_word(text, word)`: Case-insensitive whole-word occurrence counter
- `main(path)`: Aggregates results into summary statistics by model

**Usage**:
```bash
python scripts/score.py data/results_cleaned.json
```

**Output**: Model results and forbidden word failure breakdown

### `results/summary.csv`
Quick view of overall model performance:
- Pass/fail counts
- Pass rates
- Total violation counts per model

### `results/forbidden_word_failures.csv`
Breakdown of which forbidden words were leaked:
- Word name
- Count per model
- Frequency data

### `results/failure_analysis.csv`
Per-prompt detailed analysis (larger, ~6 KB):
- Individual prompt results
- Which model violated which constraint
- Specific word leak locations

---

## How to Use

### 1. **View Results**
Read `README.md` for a quick summary of findings, or open `results/summary.csv` for tabular data.

### 2. **Reproduce Scoring**
```bash
python scripts/score.py data/results_cleaned.json
```
This regenerates the summary statistics from raw responses.

### 3. **Analyze Data**
Load `data/results_cleaned.json` in Python for custom analysis:
```python
import json
data = json.load(open("data/results_cleaned.json"))
# Access individual responses, prompts, and models
```

### 4. **Deep Dive**
- Check `results/failure_analysis.csv` to find specific failure cases
- Look at `results/forbidden_word_failures.csv` to identify patterns in word leakage

---

## Results Summary

### Performance Overview
- **DeepSeek**: 93.3% pass rate (28/30), 3 total violations
- **GPT-4**: 83.3% pass rate (25/30), 7 total violations

### Failure Patterns

| Forbidden Word | GPT-4 Leaks | DeepSeek Leaks |
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

### Key Insight
DeepSeek demonstrates stronger lexical boundary adherence. GPT-4's failures are concentrated in domain-specific terms (PROGRAM, MODEL, CODE).

---

## Technical Details

### Scoring Methodology
1. **Extraction**: Parse forbidden words from prompt using regex pattern:
   ```
   "without using (?:the )?words? (.+?)\.?$"
   ```
2. **Matching**: Case-insensitive whole-word search in model output
   ```regex
   \b[word]\b
   ```
3. **Pass/Fail**: A response fails if ANY forbidden word appears even once

### Constraints
- **v1 Scope**: Lexical adherence only—does not judge factual quality or explanation coherence
- **Matching**: Whole-word only (e.g., "model" in "model output" counts; "model" within another word does not)
- **Case**: Case-insensitive (e.g., "Model", "MODEL", "model" all count as violations)

---

## Planned Extensions (Roadmap)

- [ ] Failure mechanism labels: direct leakage, instruction echo, reasoning leakage, format leakage
- [ ] Severity scoring based on number and location of violations
- [ ] Additional models (Claude, Llama, etc.)
- [ ] More prompt categories and concepts
- [ ] Statistical significance testing
- [ ] Conference-ready paper version

---

## Citations

1. **CoTControl**: YuehHanChen/CoTControl - [https://github.com/YuehHanChen/CoTControl](https://github.com/YuehHanChen/CoTControl)

2. **OpenAI Reasoning Models**: "Reasoning Models Struggle with Chain-of-Thought Controllability" - [https://openai.com/index/reasoning-models-chain-of-thought-controllability/](https://openai.com/index/reasoning-models-chain-of-thought-controllability/)

---

## Metadata

- **Repository**: [fahdev789/WordBoundaryBench](https://github.com/fahdev789/WordBoundaryBench)
- **License**: MIT
- **Language**: Python
- **Status**: Exploratory v1 (not final research output)
- **Created**: ~21 days ago

---

## Questions?

For issues, questions, or suggestions, open an issue on the repository or consult the `README.md` for more background context.
