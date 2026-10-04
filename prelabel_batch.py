"""Add review-required AI label suggestions without changing cold labels."""

import argparse
import csv
from pathlib import Path
import tempfile


LABELS = {"help_request", "discussion_prompt", "sharing"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assignments", nargs="+", help="1-based row=label")
    parser.add_argument("--uncertain", default="", help="comma-separated row numbers")
    parser.add_argument("--csv", type=Path, default=Path("labels.csv"))
    args = parser.parse_args()

    with args.csv.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    uncertain = {int(value) for value in args.uncertain.split(",") if value}
    edits = {}
    for assignment in args.assignments:
        number, label = assignment.split("=", 1)
        number = int(number)
        if not 22 <= number <= len(rows) or label not in LABELS:
            raise SystemExit(f"Invalid suggestion: {assignment}")
        if rows[number - 1]["label"]:
            raise SystemExit(f"Row {number} already has a label; refusing to overwrite")
        edits[number] = label

    for number, label in edits.items():
        row = rows[number - 1]
        row["label"] = label
        tag = "pre-labelled by Codex; review required"
        if number in uncertain:
            tag += "; hard case"
        row["note"] = tag + "; " + row["note"]

    with tempfile.NamedTemporaryFile(
        mode="w", newline="", encoding="utf-8", dir=args.csv.parent,
        prefix=".labels-", suffix=".csv", delete=False,
    ) as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "note"])
        writer.writeheader()
        writer.writerows(rows)
        temporary = Path(file.name)
    temporary.replace(args.csv)
    print(f"Added {len(edits)} review-required suggestions; cold labels unchanged.")


if __name__ == "__main__":
    main()
