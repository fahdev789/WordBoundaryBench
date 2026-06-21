import json
import re
import sys
from collections import defaultdict, Counter


def extract_forbidden_words(prompt: str):
    match = re.search(r"without using (?:the )?words? (.+?)\.?$", prompt, flags=re.I)
    if not match:
        return []
    return re.findall(r"\b[A-Z][A-Z0-9-]*\b", match.group(1))


def count_whole_word(text: str, word: str) -> int:
    return len(re.findall(r"\b" + re.escape(word) + r"\b", text or "", flags=re.I))


def main(path: str):
    data = json.load(open(path, encoding="utf-8"))
    summary = defaultdict(lambda: {"total": 0, "pass": 0, "fail": 0, "violations": 0})
    word_stats = defaultdict(Counter)

    for item in data:
        model = item.get("model", "UNKNOWN")
        prompt = item.get("prompt", "")
        output = item.get("model_output", "")
        forbidden = extract_forbidden_words(prompt)
        violations = {w: count_whole_word(output, w) for w in forbidden}
        violations = {w: c for w, c in violations.items() if c > 0}

        summary[model]["total"] += 1
        if violations:
            summary[model]["fail"] += 1
            summary[model]["violations"] += sum(violations.values())
            for word, count in violations.items():
                word_stats[word][model] += count
        else:
            summary[model]["pass"] += 1

    print("Model Results")
    for model, stats in sorted(summary.items()):
        pass_rate = stats["pass"] / stats["total"] if stats["total"] else 0
        print(f"{model}: {stats['pass']}/{stats['total']} pass, {stats['fail']} fail, pass_rate={pass_rate:.2%}")

    print("\nForbidden Word Failures")
    for word, counter in sorted(word_stats.items()):
        print(word, dict(counter))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/score.py data/results_cleaned.json")
    main(sys.argv[1])
