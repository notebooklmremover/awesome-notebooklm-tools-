# Awesome NotebookLM Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated collection of tools, scripts, and resources for Google NotebookLM — watermark removal, audio processing, prompt engineering, and more.

<p align="center">
  <a href="https://notebooklmremover.org">
    <img src="images/banner.png" alt="NotebookLM Tools" width="800">
  </a>
</p>

<p align="center">
  <strong>🌐 <a href="https://notebooklmremover.org">Try the Online Tool →</a></strong> — Free, browser-local, no upload needed
</p>

<p align="center">
  <a href="README_zh-CN.md">中文</a> · <a href="README_ja.md">日本語</a> · <a href="README_ko.md">한국어</a> · <a href="README_es.md">Español</a> · <a href="README_fr.md">Français</a> · <a href="README_de.md">Deutsch</a> · <a href="README_pt.md">Português</a> · <a href="README_ru.md">Русский</a>
</p>

---

## Why This Exists

Google NotebookLM is an incredible AI research tool that generates podcasts, slide decks, videos, and infographics from your documents. But the free tier adds visible watermarks to all exports — and the official removal option (NotebookLM Ultra) costs **$250/month**.

This repo collects **free, open-source, privacy-first** tools to solve this problem.

## Contents

- [Online Tools](#-online-tools)
- [CLI Tools](#-cli-tools)
- [Scripts](#-scripts)
- [Watermark Detection](#-watermark-detection)
- [Gemini Image Tools](#-gemini-image-tools)
- [Audio Processing](#-audio-processing)
- [Metadata & Privacy](#-metadata--privacy)
- [NotebookLM Prompts](#-notebooklm-prompts)
- [Resources](#-resources)

---

## 🌐 Online Tools

| Tool | Formats | Privacy | Free |
|------|---------|---------|------|
| **[NotebookLM Remover](https://notebooklmremover.org)** | Video, PDF, PPTX, Infographic, Gemini Image, Audio, Metadata | 100% browser-local | ✅ |
| [SlideClean](https://github.com/aaronyang-ai/slideclean) | PDF | Local Python | ✅ |
| [SlideDeckcleaner.com](https://slidedeckcleaner.com) | PDF | Server-side | ✅ |

> 💡 **[NotebookLM Remover](https://notebooklmremover.org)** is the most comprehensive option — it handles 8 format types and runs entirely in your browser using WebAssembly. Your files never leave your device.

## 🖥️ CLI Tools

### notebooklm-remover-cli

A Node.js command-line tool for batch watermark removal. Powered by the same engine as the [online tool](https://notebooklmremover.org).

```bash
# Install
npm install -g notebooklm-remover-cli

# Remove watermark from a single image
notebooklm-remover clean image input.png -o output.png

# Batch process a folder
notebooklm-remover clean image ./slides/ -o ./cleaned/

# Remove watermark from video
notebooklm-remover clean video input.mp4 -o output.mp4 --trim-ending
```

See [cli/README.md](cli/README.md) for full documentation.

## 📜 Scripts

### Python: Quick Watermark Removal

```python
# scripts/remove_watermark.py
# Removes NotebookLM watermark from images using connected component analysis

from PIL import Image
import numpy as np

def remove_watermark(image_path, output_path):
    """Remove NotebookLM logo from bottom-right corner."""
    img = np.array(Image.open(image_path))
    h, w = img.shape[:2]
    
    # Scan bottom-right region (22% width, 8% height)
    scan_x = int(w * 0.78)
    scan_y = int(h * 0.92)
    region = img[scan_y:, scan_x:]
    
    # Detect dark pixels (watermark)
    gray = np.mean(region, axis=2)
    bg_gray = np.median(gray)
    mask = gray < (bg_gray - 60)
    
    # Fill with gradient from surrounding pixels
    for y in range(region.shape[0]):
        for x in range(region.shape[1]):
            if mask[y, x]:
                # Sample from above the watermark region
                sample_y = max(0, scan_y - 10)
                img[scan_y + y, scan_x + x] = img[sample_y, scan_x + x]
    
    Image.fromarray(img).save(output_path)
    print(f"Cleaned: {output_path}")

# Usage
remove_watermark("slide_with_watermark.png", "slide_clean.png")
```

### Bash: Batch Process All PDFs

```bash
#!/bin/bash
# scripts/batch_process.sh
# Convert all PDFs in a folder, remove watermarks, rebuild

for pdf in ./input/*.pdf; do
    echo "Processing: $pdf"
    # Use the online tool API or local script
    python scripts/remove_watermark.py "$pdf" "./output/$(basename $pdf)"
done
```

## 🔍 Watermark Detection

NotebookLM watermarks are located at predictable positions:

| Format | Position | Size (1080p) |
|--------|----------|-------------|
| Video | Bottom-right | x=1104, y=656, w=770, h=62 |
| Video (720p) | Bottom-right | x=736, y=437, w=513, h=41 |
| PDF/PPTX | Bottom-right corner | ~350×80px scan area |
| Infographic | Bottom-right corner | Variable |
| Video ending | Last 2.5 seconds | "Made with Google" screen |

### Detection Algorithm

The [online tool](https://notebooklmremover.org) uses:
1. **Connected component analysis** on dark pixels in the scan area
2. **Adaptive threshold** (background median - 60/45/80 multi-pass)
3. **Smart filtering** by area, aspect ratio, and position
4. **Gradient fill** interpolation from surrounding pixels

## ✨ Gemini Image Tools

Gemini AI images embed a visible sparkle watermark. The removal is **mathematically lossless** using alpha channel reversal:

```
original_pixel = (watermarked_pixel - α × 255) / (1 - α)
```

This formula perfectly restores the original pixels — no AI inpainting, no quality loss.

| Image Size | Alpha Template |
|------------|---------------|
| ≤1024px | 48px margins |
| >1024px | 96px margins |
| Standard sizes | 1024×1024, 1536×1024, 2816×1536 |

**[Try Gemini Watermark Remover →](https://notebooklmremover.org/gemini-image)**

## 🎵 Audio Processing

NotebookLM Audio Overview podcasts include intro/outro segments. Tools to trim them:

- **[NotebookLM Podcast Trimmer](https://notebooklmremover.org/audio)** — Browser-based, supports MP3/M4A/WAV
- FFmpeg one-liner:
  ```bash
  # Trim first 15 seconds and last 20 seconds
  ffmpeg -i podcast.mp3 -ss 15 -to $(ffprobe -v error -show_entries format=duration -of csv=p=0 podcast.mp3 | awk '{print $1-20}') -c copy trimmed.mp3
  ```

## 🛡️ Metadata & Privacy

AI-generated images contain metadata that reveals their origin (C2PA, EXIF, XMP). To strip it:

- **[Image Metadata Cleaner](https://notebooklmremover.org/metadata)** — Browser-based, strips all readable metadata
- ExifTool: `exiftool -all= image.jpg`
- Python: `from PIL import Image; img = Image.open("in.jpg"); img.save("out.jpg")`

## 📝 NotebookLM Prompts

Effective prompts for NotebookLM content generation:

### Slide Generation
```
Create a professional 10-slide presentation about [topic].
Use clear headings, bullet points, and include data visualizations.
Target audience: [audience]. Tone: [formal/casual].
```

### Audio Overview
```
Generate a podcast-style discussion about [topic].
Make it conversational between two hosts.
Duration: approximately 10 minutes.
Include key takeaways at the end.
```

### Infographic
```
Create an infographic summarizing [topic].
Use a vertical layout with icons and statistics.
Color scheme: [colors]. Style: [modern/minimal/bold].
```

See [prompts/](prompts/) for the full prompt collection.

## 📚 Resources

### Official
- [NotebookLM](https://notebooklm.google/) — Google's AI notebook
- [NotebookLM Help](https://support.google.com/notebooklm)
- [NotebookLM Plans](https://notebooklm.google/plans)

### Community
- [r/notebooklm](https://reddit.com/r/notebooklm) — Reddit community
- [NotebookLM Remover](https://notebooklmremover.org) — Free online watermark remover (8 formats, 9 languages)

### Comparison: Free vs Ultra

| Feature | Free Tier | Ultra ($250/mo) | NotebookLM Remover |
|---------|-----------|-----------------|-------------------|
| Watermark on slides | ✅ Yes | ❌ No | ❌ Removed free |
| Watermark on video | ✅ Yes | ❌ No | ❌ Removed free |
| "Made with Google" ending | ✅ Yes | ❌ No | ❌ Trimmed free |
| Privacy | Server-side | Server-side | 100% browser-local |
| Cost | Free | $250/month | Free |

---

## Contributing

Contributions welcome! See [contributing.md](contributing.md).

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

This work is licensed under CC0 1.0 Universal.
