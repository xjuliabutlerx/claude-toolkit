"""
Rename files in a directory by replacing spaces in filenames with underscores.

Usage:
    python tools/rename_files.py /path/to/folder
    python tools/rename_files.py /path/to/folder --dry-run
    python tools/rename_files.py /path/to/folder --recursive
"""

import argparse
import os


def rename_files(folder: str, dry_run: bool = False, recursive: bool = False) -> None:
    folder_path = os.path.realpath(folder)

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder}' is not a valid directory.")
        return

    if recursive:
        entries = (
            (dirpath, filename)
            for dirpath, _, filenames in os.walk(folder_path)
            for filename in filenames
        )
    else:
        entries = (
            (folder_path, filename)
            for filename in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, filename))
        )

    for dirpath, filename in entries:
        if " " not in filename:
            continue

        new_filename = filename.replace(" ", "_")
        src = os.path.join(dirpath, filename)
        dst = os.path.join(dirpath, new_filename)

        if os.path.exists(dst):
            print(f"Warning: '{dst}' already exists — skipping '{src}'.")
            continue

        if dry_run:
            print(f"[dry-run] '{src}' -> '{dst}'")
        else:
            os.rename(src, dst)
            print(f"Renamed: '{src}' -> '{dst}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename files by replacing spaces in filenames with underscores."
    )
    parser.add_argument("folder", help="Path to the target directory.")
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Print what would be renamed without making changes.",
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Also process files in subdirectories.",
    )
    args = parser.parse_args()

    rename_files(args.folder, dry_run=args.dry_run, recursive=args.recursive)
