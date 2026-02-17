# Mezcal Card Scanner

A zero-cost web app that uses the device camera and TensorFlow.js to recognize Mezcal Omano playing cards and redirect users to the corresponding page on mezcalomano.com.

## Setup

1. **Add the trained model** to the `model/` folder:
   - `model.json` — model topology (from Teachable Machine export)
   - `weights.bin` (or weight shards) — model weights
   - `metadata.json` — optional; contains `labels` array. If missing, built-in class order is used.

   **Teachable Machine:** Run `python scripts/prepare_training_data.py` to generate 756 training images in `training_data/` (14 per card). Upload the class folders to [Teachable Machine](https://teachablemachine.withgoogle.com) (Image project, 54 classes). Export as TensorFlow.js and copy `model.json` + weight file(s) into `model/`. See `training_data/README.md` for step-by-step instructions.

2. **Run locally** — serve via any static server (e.g. `npx serve .`). HTTPS is required for camera access.

3. **Deploy** — push to Cloudflare Pages and add CNAME `scan.mezcalomano.com`.

## Demo mode

Append `?demo=1` to the URL to test the full flow without a model. Tap the viewfinder to simulate a card detection.
