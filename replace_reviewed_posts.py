"""Replace three unsuitable r/workout rows after the first annotation pass.

Run once after collecting the three saved Atom feed pages. Existing reviewed
labels are retained; replacement suggestions still require human review.
"""

import csv
from pathlib import Path

from import_workout_atom import entries_from, post_text
from review_labels import save


CSV_PATH = Path("labels.csv")
FEED_PATH = Path("_workout_feed_page3.xml")

# Data row number: (expected old Reddit ID, replacement Reddit ID, suggestion, reason)
REPLACEMENTS = {
    86: ("1ww1y4x", "1wuwwhm", "help_request", "non-English/off-topic post"),
    160: ("1wv9zco", "1wuwpzp", "help_request", "non-English post"),
    174: ("1wv5s84", "1wuwg1n", "discussion_prompt", "near-duplicate of row 173"),
}


def main():
    with CSV_PATH.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if len(rows) != 200:
        raise SystemExit(f"Expected 200 rows, found {len(rows)}")

    entries = {entry["id"].removeprefix("t3_"): entry for entry in entries_from(FEED_PATH)}
    existing_text = {row["text"] for row in rows}
    existing_urls = {row["note"].split("source: ", 1)[-1] for row in rows}
    if rows[172]["text"].split("\n\n", 1)[-1][:400] != rows[173]["text"].split("\n\n", 1)[-1][:400]:
        raise SystemExit("Rows 173 and 174 are no longer the expected near-duplicate pair")

    for number, (old_id, new_id, label, reason) in REPLACEMENTS.items():
        row = rows[number - 1]
        if f"/comments/{old_id}/" not in row["note"]:
            raise SystemExit(f"Row {number} no longer contains expected post {old_id}")
        if number in (86, 160) and "review required" not in row["note"]:
            raise SystemExit(f"Row {number} was reviewed; refusing to replace it")
        entry = entries[new_id]
        text, _ = post_text(entry)
        if text is None or text in existing_text or entry["url"] in existing_urls:
            raise SystemExit(f"Replacement {new_id} is unsuitable or already present")
        rows[number - 1] = {
            "text": text,
            "label": label,
            "note": f"pre-labelled by Codex; review required; replacement for {reason}; source: {entry['url']}",
        }
        print(f"Row {number}: {old_id} -> {new_id} ({label} suggestion)")

    save(CSV_PATH, rows)


if __name__ == "__main__":
    main()
