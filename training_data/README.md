# Training Data for Teachable Machine

756 images across 54 classes (14 per class), generated from `final_artwork/` with augmentations (rotation, brightness, contrast).

## Upload to Teachable Machine

1. Go to [teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com)
2. **New project** → **Image project** → **Standard image model**
3. For each class folder (spades_A, spades_K, … joker_red):
   - Click **Add a class**
   - Name it exactly as the folder (e.g. `spades_A`)
   - Drag the folder contents or use **Upload** to add images
4. **Train** (epochs: 50–100)
5. **Export model** → **TensorFlow.js** → Download
6. Extract `model.json` and `weights.bin` into `model/`

Class names must match `model/metadata.json` exactly.
