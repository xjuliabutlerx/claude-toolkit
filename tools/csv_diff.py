"""Compare two CSV files by a key column and report shared and unique values.

Reads both CSVs with csv.DictReader, extracts the set of values in the specified
key column from each file, then writes a three-column output CSV showing which
values appear in both files, only in the first, or only in the second.

Usage examples:
    python tools/csv_diff.py csv1.csv csv2.csv --key name
    python tools/csv_diff.py csv1.csv csv2.csv --key id --output diff.csv
"""

import argparse
import csv
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare two CSVs by a key column and report shared and unique values."
    )
    parser.add_argument("csv1", type=Path, help="First CSV file")
    parser.add_argument("csv2", type=Path, help="Second CSV file")
    parser.add_argument("--key", "-k", required=True, help="Column name to compare")
    parser.add_argument("--output", "-o", type=Path, help="Output CSV file path (default: <csv1>_<csv2>_diff.csv)")
    args = parser.parse_args()

    if not args.csv1.exists():
        print(f"Error: '{args.csv1}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not args.csv2.exists():
        print(f"Error: '{args.csv2}' does not exist.", file=sys.stderr)
        sys.exit(1)

    with args.csv1.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if args.key not in (reader.fieldnames or []):
            print(f"Error: key column '{args.key}' not found in '{args.csv1}'.", file=sys.stderr)
            sys.exit(1)
        keys1 = {row[args.key] for row in reader}

    with args.csv2.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if args.key not in (reader.fieldnames or []):
            print(f"Error: key column '{args.key}' not found in '{args.csv2}'.", file=sys.stderr)
            sys.exit(1)
        keys2 = {row[args.key] for row in reader}

    same = sorted(keys1 & keys2)
    only_in_csv1 = sorted(keys1 - keys2)
    only_in_csv2 = sorted(keys2 - keys1)

    max_len = max(len(same), len(only_in_csv1), len(only_in_csv2))
    same += [""] * (max_len - len(same))
    only_in_csv1 += [""] * (max_len - len(only_in_csv1))
    only_in_csv2 += [""] * (max_len - len(only_in_csv2))

    output = args.output if args.output else Path(f"{args.csv1.stem}_{args.csv2.stem}_diff.csv")

    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["same", "only_in_csv1", "only_in_csv2"])
        for row in zip(same, only_in_csv1, only_in_csv2):
            writer.writerow(row)

    print(f"same: {len([v for v in same if v])}, only_in_csv1: {len([v for v in only_in_csv1 if v])}, only_in_csv2: {len([v for v in only_in_csv2 if v])} → {output}")


if __name__ == "__main__":
    main()
