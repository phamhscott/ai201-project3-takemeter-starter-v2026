"""Read and confirm or correct each AI-suggested label in labels.csv."""

import argparse
import csv
from pathlib import Path
import sys
import tempfile


CHOICES = {"h": "help_request", "d": "discussion_prompt", "s": "sharing"}
PENDING = "pre-labelled by Codex; review required"


def save(path, rows):
    with tempfile.NamedTemporaryFile(
        mode="w", newline="", encoding="utf-8", dir=path.parent,
        prefix=".labels-", suffix=".csv", delete=False,
    ) as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "note"])
        writer.writeheader()
        writer.writerows(rows)
        temporary = Path(file.name)
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("labels.csv"))
    parser.add_argument("--status", action="store_true", help="show progress and exit")
    args = parser.parse_args()
    with args.csv.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    pending = [i for i, row in enumerate(rows) if PENDING in row["note"]]
    if args.status:
        print(f"{len(pending)} AI suggestions still require review.")
        return

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass
    print("Read the entire post before responding. Enter=keep suggestion; h/d/s=change; n=skip; q=quit.")
    print("h help_request | d discussion_prompt | s sharing\n")
    for index in pending:
        row = rows[index]
        print(f"{'=' * 72}\nCSV data row {index + 1} | suggested: {row['label']}")
        if "hard case" in row["note"]:
            print("FLAGGED HARD CASE: check the taxonomy boundary closely.")
        print(f"{row['text']}\n")
        print(row["note"].split("source: ", 1)[-1])
        while True:
            answer = input("Keep [Enter], change [h/d/s], skip [n], quit [q]: ").strip().lower()
            if answer in {"", "h", "d", "s", "n", "q"}:
                break
            print("Use Enter, h, d, s, n, or q.")
        if answer == "q":
            break
        if answer == "n":
            continue
        if answer in CHOICES:
            row["label"] = CHOICES[answer]
        row["note"] = row["note"].replace(PENDING, "pre-labelled by Codex; checked by Scott", 1)
        save(args.csv, rows)
        print("Saved.\n")
    remaining = sum(PENDING in row["note"] for row in rows)
    print(f"{remaining} AI suggestions still require review.")


if __name__ == "__main__":
    main()
