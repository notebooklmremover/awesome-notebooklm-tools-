"""
NotebookLM Watermark Remover — Python Script
Removes the NotebookLM logo from the bottom-right corner of images.

For a full-featured online tool with video/PDF/PPTX support:
https://notebooklmremover.org
"""

import sys
from PIL import Image
import numpy as np


def remove_watermark(image_path: str, output_path: str) -> None:
    img = np.array(Image.open(image_path))
    h, w = img.shape[:2]

    scan_w = int(w * 0.22)
    scan_h = int(h * 0.08)
    scan_x = w - scan_w
    scan_y = h - scan_h

    region = img[scan_y:, scan_x:].copy()
    gray = np.mean(region, axis=2)
    bg_gray = np.median(gray)

    for threshold in [80, 60, 45]:
        mask = gray < (bg_gray - threshold)
        if np.sum(mask) > 20:
            break

    margin = max(10, scan_h // 8)
    for y in range(region.shape[0]):
        for x in range(region.shape[1]):
            if mask[y, x]:
                sample_y = max(0, scan_y - margin)
                img[scan_y + y, scan_x + x] = img[sample_y, scan_x + x]

    Image.fromarray(img).save(output_path)
    print(f"Cleaned: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_watermark.py <input> <output>")
        print("\nFor video/PDF/PPTX support, use: https://notebooklmremover.org")
        sys.exit(1)
    remove_watermark(sys.argv[1], sys.argv[2])
