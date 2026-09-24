"""Remove the grey shading from Terra's artwork (face, shirt, motion smudges).

Low-saturation grey pixels are lifted to white; black outlines and the green cape
are left alone. Used to build docs/assets/img/terra-*.{png,webp}.
"""
import numpy as np
from PIL import Image

def clean(im: Image.Image) -> Image.Image:
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, alpha = a[..., :3], a[..., 3:4]
    lum = rgb.mean(axis=2, keepdims=True)
    sat = rgb.max(axis=2, keepdims=True) - rgb.min(axis=2, keepdims=True)
    grey = sat < 40                                  # cape teal has ~70+
    # 0 below 120 (outlines stay), ramps to 1 at 165 and above (shading -> white)
    t = np.clip((lum - 120) / 45, 0, 1) * grey
    out = rgb + (255 - rgb) * t
    # fully whitened pixels become opaque white so no grey shows through alpha edges
    alpha = np.where((t >= 1) & (alpha > 0), 255, alpha)
    return Image.fromarray(np.concatenate([out, alpha], axis=2).clip(0, 255).astype(np.uint8), "RGBA")

if __name__ == "__main__":
    import sys
    for src, dst in zip(sys.argv[1::2], sys.argv[2::2]):
        clean(Image.open(src)).save(dst)
        print("cleaned", dst)
