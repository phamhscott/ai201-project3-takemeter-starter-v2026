"""Import consecutive r/workout Atom entries into an unlabeled TakeMeter CSV.

The feed files are collected separately; this script makes no network requests.
It includes original text posts, including title-only posts, and skips links
and crossposts whose text belongs to another post.
"""

import argparse
import csv
import html
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urljoin
import xml.etree.ElementTree as ET


ATOM = "{http://www.w3.org/2005/Atom}"


class BodyText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []
        self.found = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            if self.depth:
                self.depth += 1
            elif "md" in attrs.get("class", "").split() and not self.found:
                self.depth = 1
                self.found = True
            return
        if not self.depth:
            return
        if tag in {"p", "br", "blockquote", "pre", "ul", "ol", "h1", "h2", "h3"}:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "a":
            self.links.append((len(self.parts), attrs.get("href")))
        elif tag == "img" and attrs.get("alt"):
            self.parts.append(attrs["alt"])

    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth -= 1
        elif self.depth and tag == "a" and self.links:
            start, href = self.links.pop()
            if href and href not in "".join(self.parts[start:]):
                self.parts.append(f" ({href})")
        elif self.depth and tag in {"p", "blockquote", "pre", "li", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)

    def text(self):
        value = "".join(self.parts).replace("\xa0", " ")
        value = re.sub(r"[ \t]+\n", "\n", value)
        value = re.sub(r"\n[ \t]+", "\n", value)
        return re.sub(r"\n{3,}", "\n\n", value).strip()


def entries_from(path):
    root = ET.parse(path).getroot()
    for entry in root.findall(f"{ATOM}entry"):
        yield {
            "id": entry.findtext(f"{ATOM}id", ""),
            "title": entry.findtext(f"{ATOM}title", "").strip(),
            "url": entry.find(f"{ATOM}link").attrib["href"],
            "html": entry.findtext(f"{ATOM}content", ""),
        }


def post_text(entry):
    parser = BodyText()
    parser.feed(entry["html"])
    body = parser.text()
    if body:
        return entry["title"] + "\n\n" + body, False

    link = re.search(r'<a href="([^"]+)">\[link\]</a>', entry["html"])
    if link:
        destination = urljoin("https://www.reddit.com", html.unescape(link.group(1)))
        if destination.rstrip("/") == entry["url"].rstrip("/"):
            return entry["title"], True
    return None, False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feeds", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("labels.csv"))
    parser.add_argument("--count", type=int, default=200)
    parser.add_argument("--replace-unlabeled", action="store_true")
    args = parser.parse_args()

    if args.output.exists():
        with args.output.open(newline="", encoding="utf-8") as file:
            existing = list(csv.DictReader(file))
        if existing and (
            not args.replace_unlabeled
            or any(row["label"] or not row["note"].startswith("source: ") for row in existing)
        ):
            raise SystemExit(f"Refusing to overwrite {len(existing)} existing rows in {args.output}")

    seen = set()
    seen_text = set()
    rows = []
    inspected = skipped_links = skipped_duplicate_text = title_only = 0
    for path in args.feeds:
        for entry in entries_from(path):
            inspected += 1
            if entry["id"] in seen:
                continue
            seen.add(entry["id"])
            text, only_title = post_text(entry)
            if text is None:
                skipped_links += 1
                continue
            if text in seen_text:
                skipped_duplicate_text += 1
                continue
            seen_text.add(text)
            title_only += only_title
            rows.append({"text": text, "label": "", "note": f"source: {entry['url']}"})
            if len(rows) == args.count:
                break
        if len(rows) == args.count:
            break

    if len(rows) < args.count:
        raise SystemExit(f"Only {len(rows)} eligible posts found; no CSV written")
    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "note"])
        writer.writeheader()
        writer.writerows(rows)
    print(
        f"Inspected {inspected} entries; skipped {skipped_links} link/crosspost "
        f"entries and {skipped_duplicate_text} duplicate-text entries."
    )
    print(f"Saved {len(rows)} unique posts to {args.output} ({title_only} title-only).")
    print(f"First source: {rows[0]['note']}")
    print(f"Last source: {rows[-1]['note']}")


if __name__ == "__main__":
    main()
