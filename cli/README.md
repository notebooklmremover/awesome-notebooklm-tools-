# notebooklm-remover-cli

Command-line tool for batch NotebookLM watermark removal.

> **Prefer a visual interface?** Use the [online tool](https://notebooklmremover.org) — same engine, zero setup.

## Install

```bash
npm install -g notebooklm-remover-cli
```

## Usage

### Image Watermark Removal

```bash
# Single file
notebooklm-remover clean image input.png -o output.png

# Batch process folder
notebooklm-remover clean image ./slides/ -o ./cleaned/

# Specify output format
notebooklm-remover clean image input.png -o output.jpg --format jpg --quality 95
```

### Video Watermark Removal

```bash
# Remove watermark + trim ending
notebooklm-remover clean video input.mp4 -o output.mp4 --trim-ending

# Custom FPS
notebooklm-remover clean video input.mp4 -o output.mp4 --fps 30

# Keep original ending
notebooklm-remover clean video input.mp4 -o output.mp4 --no-trim
```

### Gemini Image (Lossless)

```bash
# Alpha reversal — zero quality loss
notebooklm-remover clean gemini input.png -o output.png
```

### Audio Trimming

```bash
# Trim intro (first 15s) and outro (last 20s)
notebooklm-remover trim audio input.mp3 -o output.mp3 --start 15 --end 20
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output path | `./cleaned/` |
| `--format` | Output format (png/jpg/webp) | Same as input |
| `--quality` | JPEG/WebP quality (1-100) | 95 |
| `--trim-ending` | Remove "Made with Google" ending | true |
| `--fps` | Output video FPS (0=original) | 0 |
| `--start` | Audio trim start (seconds) | 0 |
| `--end` | Audio trim end (seconds from end) | 0 |

## How It Works

This CLI uses the same detection and removal engine as [notebooklmremover.org](https://notebooklmremover.org):

1. **Detection**: Connected component analysis identifies watermark pixels
2. **Removal**: Gradient fill interpolation restores the background
3. **Gemini**: Mathematical alpha channel reversal (lossless)
4. **Video**: FFmpeg-based delogo filter + tail trim

## License

CC0 1.0 Universal
