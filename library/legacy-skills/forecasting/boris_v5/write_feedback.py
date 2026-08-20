#!/usr/bin/env python3
import argparse
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(ROOT, "feedback_template.md")
FEEDBACK_DIR = os.path.join(ROOT, "feedback")


def main():
    parser = argparse.ArgumentParser(description="Create Boris feedback file from template.")
    parser.add_argument("--idea", required=True, help="Idea name/slug for filename.")
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"), help="Date to write into template.")
    args = parser.parse_args()

    os.makedirs(FEEDBACK_DIR, exist_ok=True)

    with open(TEMPLATE, "r", encoding="utf-8") as f:
        tpl = f.read()

    content = tpl.replace("{{idea_name}}", args.idea).replace("{{date}}", args.date)
    fname = f"{args.idea.replace(' ', '_')}.md"
    out_path = os.path.join(FEEDBACK_DIR, fname)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Feedback saved to {out_path}")


if __name__ == "__main__":
    main()
