# Word-Forbidden Constraint Benchmark v1

A small benchmark testing whether LLMs can explain concepts while avoiding critical words normally associated with those concepts.

This v1 compares **GPT-4** and **DeepSeek** on **30 matched prompts**.

## Task

Each prompt asks the model to explain a concept while forbidding one or more words.

Example:

```text
Explain machine learning without using the word MODEL.
```

Expected behavior:

```text
The forbidden word never appears in model_output.
```

## Dataset

```text
30 prompts × 2 models = 60 responses
```

Models:

- GPT-4
- DeepSeek

Data file:

```text
data/results_cleaned.json
```

## Scoring Rule

A response fails if any forbidden word appears in `model_output`, using case-insensitive whole-word matching.

The current v1 score does **not** judge factual quality. It only measures lexical boundary adherence.

## Results

| Model | Total | Pass | Fail | Pass Rate |
|---|---:|---:|---:|---:|
| GPT-4 | 30 | 25 | 5 | 83.3% |
| DeepSeek | 30 | 28 | 2 | 93.3% |

## Failure Words Observed

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

## Why This Matters

The benchmark separates knowing a concept from obeying a lexical boundary. A model can produce a fluent and useful explanation while still violating a simple instruction such as avoiding a specific word.

## Planned Extensions

- Failure mechanism labels: direct leakage, instruction echo, reasoning leakage, format leakage.
- Severity scoring based on number and location of forbidden-word leaks.
- More models.
- More prompt categories.
- Conference-ready version with statistical analysis.

## Reproduce

```bash
python scripts/score.py data/results_cleaned.json
```

## Status

This is an exploratory v1 benchmark, not a final paper result.
