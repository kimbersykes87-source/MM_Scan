#!/usr/bin/env python3
"""
Prepare training data for Teachable Machine from final_artwork.
- Copies images into class folders (e.g., training_data/spades_A/)
- Generates augmented versions (rotation, brightness, contrast) to reach ~20 samples per class
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

ROOT = Path(__file__).resolve().parent.parent
ARTWORK_DIR = ROOT / "final_artwork"
OUTPUT_DIR = ROOT / "training_data"
TARGET_PER_CLASS = 20
EXCLUDE = {"055_promo_front.jpg", "056_promo_back.jpg", "057_card-back.jpg"}

# Filename pattern: 001_spades_A.jpg -> class "spades_A"
def filename_to_class(name: str) -> Optional[str]:
    if name in EXCLUDE:
        return None
    stem = Path(name).stem  # e.g. "001_spades_A"
    parts = stem.split("_", 1)  # ["001", "spades_A"]
    if len(parts) == 2:
        return parts[1]  # "spades_A" or "joker_black"
    return None


def augment(img: Image.Image, seed: int) -> list:
    """Generate augmented variants of an image."""
    results = [img.copy()]
    rng = lambda i: (seed * 31 + i) % 100 / 100

    # Slight rotations (-12, -6, 6, 12 degrees)
    for angle in [-12, -6, 6, 12]:
        results.append(img.rotate(angle, expand=False, fillcolor=(255, 255, 255)))

    # Brightness
    for i, factor in enumerate([0.85, 1.15]):
        enh = ImageEnhance.Brightness(img)
        results.append(enh.enhance(factor))

    # Contrast
    for i, factor in enumerate([0.9, 1.1]):
        enh = ImageEnhance.Contrast(img)
        results.append(enh.enhance(factor))

    # Combined (rotation + brightness/contrast)
    rotated = img.rotate(-8, expand=False, fillcolor=(255, 255, 255))
    results.append(ImageEnhance.Brightness(rotated).enhance(1.08))

    rotated2 = img.rotate(8, expand=False, fillcolor=(255, 255, 255))
    results.append(ImageEnhance.Contrast(rotated2).enhance(1.05))

    # Sharpen (simulates different focus)
    results.append(ImageEnhance.Sharpness(img).enhance(1.3))

    # Additional rotations for robustness
    for angle in [-4, 4]:
        results.append(img.rotate(angle, expand=False, fillcolor=(255, 255, 255)))

    return results


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    total = 0

    for f in sorted(ARTWORK_DIR.glob("*.jpg")):
        name = f.name
        cls = filename_to_class(name)
        if not cls:
            continue

        class_dir = OUTPUT_DIR / cls
        class_dir.mkdir(exist_ok=True)

        img = Image.open(f).convert("RGB")
        augs = augment(img, seed=hash(cls) % 10000)

        for i, aug in enumerate(augs[:TARGET_PER_CLASS]):
            out_path = class_dir / f"{cls}_{i:02d}.jpg"
            aug.save(out_path, "JPEG", quality=90)
            total += 1

        print(f"  {cls}: {min(len(augs), TARGET_PER_CLASS)} images")

    print(f"\nDone. {total} images in {OUTPUT_DIR}")
    print("\nNext: Open https://teachablemachine.withgoogle.com")
    print("  -> Image Project -> Standard Image Model")
    print("  -> Upload training_data/ folders as classes (drag each class folder)")
    print("  -> Train -> Export as TensorFlow.js -> Download")
    print("  -> Extract model.json and weights into model/")


if __name__ == "__main__":
    main()
