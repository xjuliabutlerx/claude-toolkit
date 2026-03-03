"""Convert a CSV file to a JSON file using the first row as column headers.

Reads a CSV file with csv.DictReader (first row becomes dict keys) and writes
the rows as a JSON array. The output file path defaults to the same name as
the input with a .json extension.

Usage examples:
    python tools/csv_to_json.py data.csv
    python tools/csv_to_json.py data.csv --output result.json
    python tools/csv_to_json.py data.csv --indent 4
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a CSV file to a JSON file.")
    parser.add_argument("input", type=Path, help="Path to the CSV file")
    parser.add_argument("--output", "-o", type=Path, help="Output JSON file path (default: input with .json extension)")
    parser.add_argument("--indent", "-i", type=int, default=4, help="JSON indentation level (default: 4; use 0 for compact)")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if args.input.suffix.lower() != ".csv":
        print(f"Warning: '{args.input}' does not have a .csv extension.", file=sys.stderr)

    output = args.output if args.output else args.input.with_suffix(".json")
    indent = args.indent if args.indent > 0 else None

    with args.input.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with output.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=indent)

    print(f"Converted {len(rows)} rows → {output}")


if __name__ == "__main__":
    main()
