#!/usr/bin/env python3
"""
Process agave species PNGs (transparent) from SPECIES folder:
- Composite onto white background
- Resize to 224x224 for Teachable Machine
- Generate augmented samples (rotation, brightness, contrast)
- Save to output folder, organized by class for TM upload
"""

import os
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageEnhance
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow --quiet")
    from PIL import Image, ImageEnhance

SOURCE = Path(r"C:\Users\kimbe\Dropbox\Kimber\Business\Edward Kimber Sykes\Clients\Mezcalomano\ARTWORK\Discovery Deck\SPECIES")
OUTPUT = Path(__file__).resolve().parent.parent / "species_white"
TARGET_SIZE = 224
TARGET_PER_CLASS = 20

# Filename patterns:
# - COLOURED_PENCIL_001_Hearts_2_Espadin.png -> hearts_2
# - Hearts_2_Espadin.png, Clubs_10_Cincoañero.png -> hearts_2, clubs_10
def filename_to_class(name: str) -> Optional[str]:
    stem = Path(name).stem
    parts = stem.split("_")
    suit_map = {"hearts": "hearts", "spades": "spades", "clubs": "clubs", "diamonds": "diamonds"}
    suit_lower = parts[0].lower() if parts else ""
    if suit_lower not in suit_map:
        # Try COLOURED_PENCIL_001_Hearts_2_Espadin
        if stem.startswith("COLOURED_PENCIL_") and len(parts) >= 5:
            suit_lower = parts[3].lower()
            rank_part = parts[4]
            rank = rank_part.split("_")[0] if "_" in rank_part else rank_part[:1]
            return f"{suit_lower}_{rank}" if suit_lower in suit_map else None
        return None
    if len(parts) < 2:
        return None
    rank = parts[1]  # 2-10 or A
    return f"{suit_lower}_{rank}"


def augment(img: Image.Image, seed: int) -> list:
    """Generate augmented variants of an image."""
    results = [img.copy()]
    # Rotations (-12, -6, 6, 12 degrees)
    for angle in [-12, -6, 6, 12]:
        results.append(img.rotate(angle, expand=False, fillcolor=(255, 255, 255)))
    # Brightness
    for factor in [0.85, 1.15]:
        results.append(ImageEnhance.Brightness(img).enhance(factor))
    # Contrast
    for factor in [0.9, 1.1]:
        results.append(ImageEnhance.Contrast(img).enhance(factor))
    # Rotation + brightness/contrast
    r1 = img.rotate(-8, expand=False, fillcolor=(255, 255, 255))
    results.append(ImageEnhance.Brightness(r1).enhance(1.08))
    r2 = img.rotate(8, expand=False, fillcolor=(255, 255, 255))
    results.append(ImageEnhance.Contrast(r2).enhance(1.05))
    # Sharpen
    results.append(ImageEnhance.Sharpness(img).enhance(1.3))
    # Extra rotations
    for angle in [-4, 4]:
        results.append(img.rotate(angle, expand=False, fillcolor=(255, 255, 255)))
    return results


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    total = 0

    for f in sorted(SOURCE.glob("*.png")):
        cls = filename_to_class(f.name)
        if not cls:
            print(f"  Skip: {f.name}")
            continue

        img = Image.open(f).convert("RGBA")
        w, h = img.size

        # White background
        white = Image.new("RGB", (w, h), (255, 255, 255))
        white.paste(img, (0, 0), img)

        # Resize to target
        base = white.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)

        augs = augment(base, seed=hash(cls) % 10000)
        class_dir = OUTPUT / cls
        class_dir.mkdir(exist_ok=True)
        n = min(len(augs), TARGET_PER_CLASS)
        for i, aug in enumerate(augs[:TARGET_PER_CLASS]):
            out_path = class_dir / f"{cls}_{i:02d}.jpg"
            aug.save(out_path, "JPEG", quality=92)
            total += 1
        print(f"  {cls}: {n} images")

    print(f"\nDone. {total} images in {OUTPUT}")
    print("\nNext: Upload species_white/ class folders to Teachable Machine.")


if __name__ == "__main__":
    main()
