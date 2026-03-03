"""Convert HEIC/HEIF image files to JPEG format.

Converts a single .heic file or all HEIC files in a directory to JPEG.
Output filenames keep the same stem with a .jpg extension. Skips files
whose destination already exists (with a warning).

Requires: Pillow, pillow-heif
    pip install Pillow pillow-heif

Usage examples:
    python tools/heic_to_jpeg.py photo.heic
    python tools/heic_to_jpeg.py ./photos/ --output ./converted/
    python tools/heic_to_jpeg.py photo.heic --quality 95 --dry-run
"""

import argparse
import sys
from pathlib import Path

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    from PIL import Image
except ImportError:
    print(
        "Error: pillow-heif and Pillow are required.\n"
        "Install them with: pip install Pillow pillow-heif",
        file=sys.stderr,
    )
    sys.exit(1)


def convert_file(src: Path, dst: Path, quality: int, dry_run: bool) -> None:
    if dst.exists():
        print(f"Warning: '{dst}' already exists, skipping.")
        return
    if dry_run:
        print(f"[dry-run] Would convert {src} → {dst}")
        return
    Image.open(src).convert("RGB").save(dst, "JPEG", quality=quality)
    print(f"Converted {src} → {dst}")


def collect_heic(directory: Path) -> list[Path]:
    return [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == ".heic"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert HEIC/HEIF files to JPEG.")
    parser.add_argument("input", type=Path, help=".heic file or directory of HEIC files")
    parser.add_argument("--output", "-o", type=Path, help="Output directory (default: same directory as input)")
    parser.add_argument("--quality", "-q", type=int, default=90, metavar="1-95", help="JPEG quality 1–95 (default: 90)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Print what would be done without writing files")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not (1 <= args.quality <= 95):
        print("Error: --quality must be between 1 and 95.", file=sys.stderr)
        sys.exit(1)

    if args.input.is_dir():
        files = collect_heic(args.input)
        if not files:
            print(f"No .heic files found in '{args.input}'.")
            return
        out_dir = args.output if args.output else args.input
        if not args.dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
        for src in files:
            dst = out_dir / (src.stem + ".jpg")
            convert_file(src, dst, args.quality, args.dry_run)
    else:
        if args.input.suffix.lower() != ".heic":
            print(f"Warning: '{args.input}' does not have a .heic extension.", file=sys.stderr)
        out_dir = args.output if args.output else args.input.parent
        if not args.dry_run and args.output:
            out_dir.mkdir(parents=True, exist_ok=True)
        dst = out_dir / (args.input.stem + ".jpg")
        convert_file(args.input, dst, args.quality, args.dry_run)


if __name__ == "__main__":
    main()
