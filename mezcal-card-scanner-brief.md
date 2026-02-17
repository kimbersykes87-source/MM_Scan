# Project Brief: Mezcal Card Scanner

## Overview

Build a lightweight, zero-cost web application hosted at `scan.mezcalomano.com` that uses the device camera to recognize playing cards from a custom 40-card mezcal/agave deck and redirects users to the corresponding page on `mezcalomano.com`.

## Context

The client has a physical deck of 40 custom playing cards (A through 10, across 4 suits). Each card features a unique agave species illustration, a mezcal variety name (e.g., "Alto", "Papalote", "Masparillo", "Mexicano", "Pulquero"), a nickname, tasting notes, and botanical details. The goal is to let someone scan any card with their phone camera and be taken to a detail page for that agave/mezcal on the main website.

### Example Cards (Spades suit)

| Card | Mezcal Name | Nickname | Agave Species | Tasting Notes |
|------|-------------|----------|---------------|---------------|
| A♠ | Pulquero | "Bulky Brute" | Agave americana var. | clean, green, funky |
| 6♠ | Mexicano | "Green Firework" | Agave rhodacantha | clean, herbal, spicy |
| 7♠ | Masparillo | "Crag Ripper" | Agave maximiliana | toasty, herbal, fruity |
| 8♠ | Papalote | "Copper Butterfly" | Agave cupreata | clean, herbal, fruity |
| 9♠ | Alto | "Soaring Monarch" | Agave inaequidens | clean, herbal, fruity |

## User Flow

1. User visits `scan.mezcalomano.com` on their mobile phone
2. Page requests camera access and opens a live viewfinder
3. User holds a card in front of the camera
4. The app identifies the card (displays the detected name briefly as confirmation)
5. User is redirected to `mezcalomano.com/directory/{slug}` (e.g., `mezcalomano.com/directory/alto`)

## Technical Architecture

### Stack

- **Frontend:** Single `index.html` file (HTML + JS + CSS inline), no framework
- **Recognition:** TensorFlow.js with a custom-trained image classification model (MobileNet transfer learning)
- **Hosting:** GitHub Pages or Cloudflare Pages (free tier), with `scan.mezcalomano.com` pointed via CNAME
- **Cost:** $0 ongoing — all inference runs client-side in the browser

### Model Training

- Use Google Teachable Machine (https://teachablemachine.withgoogle.com) or a custom TensorFlow.js training script
- Capture 15–30 photos of each card under varied lighting, angles, and backgrounds
- Export as a TensorFlow.js model (model.json + weight shard files)
- Model size target: under 5MB total for fast mobile loading

### Card-to-URL Mapping

A JS object maps each recognized class label to a destination URL:

```javascript
const CARD_ROUTES = {
  "pulquero":   "https://mezcalomano.com/directory/pulquero",
  "mexicano":   "https://mezcalomano.com/directory/mexicano",
  "masparillo": "https://mezcalomano.com/directory/masparillo",
  "papalote":   "https://mezcalomano.com/directory/papalote",
  "alto":       "https://mezcalomano.com/directory/alto",
  // ... all 40 cards
};
```

### Key Technical Considerations

- **Camera API:** Use `navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })` to default to rear camera
- **Frame capture:** Draw video frames to an offscreen canvas, run inference at ~2–4 fps (not every frame — save battery)
- **Confidence threshold:** Only trigger a match when confidence exceeds a defined threshold (e.g., 85%) to avoid false redirects
- **Debounce/confirmation:** Require consistent detection across multiple consecutive frames (e.g., same card detected 3 frames in a row) before redirecting
- **Loading state:** Show a loading indicator while the TF.js model downloads and initializes
- **HTTPS required:** Camera API requires a secure context — GitHub Pages and Cloudflare Pages both provide this

### File Structure

```
/
├── index.html          # Single-page app (all HTML/CSS/JS inline)
├── model/
│   ├── model.json      # TensorFlow.js model topology
│   └── weights.bin     # Model weights (may be multiple shards)
├── CNAME               # For GitHub Pages custom domain
└── README.md
```

## Design Requirements

- Clean, minimal UI — the camera viewfinder should dominate the screen
- Brand-aligned styling (use colors/fonts from mezcalomano.com)
- Brief confirmation overlay when a card is detected (show the mezcal name + agave species for ~1.5 seconds before redirect)
- Fallback message if camera access is denied
- Works on iOS Safari and Android Chrome (the two primary mobile browsers)

## Scope Boundaries

- **In scope:** Camera capture, on-device card recognition, redirect to existing URLs
- **Out of scope:** Building the destination pages on mezcalomano.com, card deck e-commerce, user accounts, analytics (can be added later with a free tier like Plausible or Umami)

## Deployment

1. Create a GitHub repo (or Cloudflare Pages project)
2. Add the built files
3. Configure custom domain: add CNAME record for `scan.mezcalomano.com` pointing to the hosting provider
4. SSL is automatic with both GitHub Pages and Cloudflare Pages

---

## Questions to Clarify Before Building

1. **URL structure:** Is `mezcalomano.com/directory/{mezcal-name}` the confirmed URL pattern? Do these pages already exist for all 40 cards, or do they need to be created?

2. **Card identification granularity:** Should the scanner identify each of the 40 individual cards (e.g., 9 of Spades = Alto), or just the 10 unique mezcal names across suits? In other words — do cards of different suits but the same number share the same agave, or does each of the 40 cards feature a different agave?

3. **Complete card list:** Can you provide the full mapping of all 40 cards (card value + suit → mezcal name → URL slug)? We need this to set up both the model training classes and the routing table.

4. **Redirect behavior:** Should the destination page open in the same tab (replacing the scanner), or open in a new tab so the user can scan another card without reloading?

5. **Branding assets:** Are there brand colors, fonts, or a logo for Mezcal Omano that should appear on the scanner page? Or should it be as minimal as possible — just the camera?

6. **Offline support:** Should the scanner work offline after the first load (service worker caching the model), or is requiring an internet connection acceptable?

7. **Hosting preference:** Do you have a preference between GitHub Pages and Cloudflare Pages? Cloudflare Pages offers slightly faster global CDN and easier DNS if your domain is already on Cloudflare.

8. **Training image capture:** Do you have access to all 40 physical cards to photograph them for model training? We'll need multiple photos of each card in different conditions.
