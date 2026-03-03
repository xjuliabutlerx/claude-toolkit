"""Resize image files or all images in a directory to specified dimensions.

Resizes a single image or all images in a directory using Pillow. When only
one dimension is provided, the image is scaled proportionally. When both
dimensions are provided, the image is resized to exact dimensions.

Usage examples:
    python tools/resize_images.py photo.jpg --width 800
    python tools/resize_images.py ./photos/ --width 1920 --height 1080 --output ./resized/
    python tools/resize_images.py photo.jpg --width 800 --dry-run
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install it with: pip install Pillow", file=sys.stderr)
    sys.exit(1)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}


def resize_image(src: Path, dst: Path, width: int | None, height: int | None, quality: int, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] Would resize {src} → {dst}")
        return

    img = Image.open(src)
    if width and height:
        img = img.resize((width, height), Image.Resampling.LANCZOS)
    elif width:
        ratio = width / img.width
        img = img.resize((width, round(img.height * ratio)), Image.Resampling.LANCZOS)
    else:
        ratio = height / img.height
        img = img.resize((round(img.width * ratio), height), Image.Resampling.LANCZOS)

    dst.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {}
    if dst.suffix.lower() in {".jpg", ".jpeg"}:
        save_kwargs["quality"] = quality
    img.save(dst, **save_kwargs)
    print(f"Resized {src} → {dst}")


def collect_images(directory: Path) -> list[Path]:
    return [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]


def main() -> None:
    parser = argparse.ArgumentParser(description="Resize image files to specified dimensions.")
    parser.add_argument("input", type=Path, help="Image file or directory of images to resize")
    parser.add_argument("--width", "-W", type=int, help="Target width in pixels")
    parser.add_argument("--height", "-H", type=int, help="Target height in pixels")
    parser.add_argument("--output", "-o", type=Path, help="Output file or directory (default: <name>_resized.<ext> or resized/)")
    parser.add_argument("--quality", "-q", type=int, default=85, metavar="1-95", help="JPEG save quality 1–95 (default: 85)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Print what would be done without writing files")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not args.width and not args.height:
        print("Error: at least one of --width or --height is required.", file=sys.stderr)
        sys.exit(1)

    if not (1 <= args.quality <= 95):
        print("Error: --quality must be between 1 and 95.", file=sys.stderr)
        sys.exit(1)

    if args.input.is_dir():
        images = collect_images(args.input)
        if not images:
            print(f"No supported image files found in '{args.input}'.")
            return
        out_dir = args.output if args.output else args.input / "resized"
        for src in images:
            dst = out_dir / src.name
            resize_image(src, dst, args.width, args.height, args.quality, args.dry_run)
    else:
        if args.output:
            dst = args.output
        else:
            stem = args.input.stem
            dst = args.input.with_name(f"{stem}_resized{args.input.suffix}")
        resize_image(args.input, dst, args.width, args.height, args.quality, args.dry_run)


if __name__ == "__main__":
    main()
