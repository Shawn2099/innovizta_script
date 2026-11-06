"""Reel cover (1080x1920) from a frame of a portrait 4K clip, laid out for the Instagram 3:4 grid crop.

Usage:
  pipeline\.venv\Scripts\python.exe -I pipeline\make_cover.py <clip> <time_s> <out.jpg> "LINE 1" ["LINE 2"] [--y 1060]

Layout: head-to-waist photo (top 3/4 of the frame) fills the grid crop (y 240-1680), blurred bands above/below,
<=4 words in Anton white caps with a black outline + orange underline (STO series style), on the chest.
Wide shots: --zoom 1.8 --cx 0.56 --top 0.22 crops in on the face (cx/top are fractions of the frame).
Pick the frame first (eyes open, smiling): grab a few with ffmpeg -ss and look.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = Path(__file__).parent / "assets" / "fonts" / "Anton-Regular.ttf"
ORANGE = "#F7931E"


BLACK_FONT = Path(__file__).parent / "assets" / "fonts" / "Montserrat-Black.ttf"
YELLOW = "#FFD400"


def _shadowed(layer, offset=(10, 14), blur=10, alpha=150):
    """Paste a soft drop shadow under an RGBA layer and return the combined layer."""
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    mask = layer.split()[3].point(lambda v: alpha if v else 0)
    sh.paste((0, 0, 0, 255), offset, mask)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    sh.alpha_composite(layer)
    return sh


def fun_text(bg, a):
    """Sticker-style title: white outlined lines, last line black-on-orange box, all tilted; optional badge."""
    W = bg.size[0]
    f = ImageFont.truetype(str(FONT), a.size)
    layer = Image.new("RGBA", (W + 400, a.size * (len(a.lines) + 1) + 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, y = layer.size[0] / 2, 60
    for i, t in enumerate(a.lines):
        w = d.textlength(t, font=f)
        if i == len(a.lines) - 1:                      # punch line on an orange box
            pad = 34
            box = (cx - w / 2 - pad, y + 6, cx + w / 2 + pad, y + a.size * 1.18)
            d.rounded_rectangle(box, radius=26, fill=ORANGE, outline="black", width=8)
            d.text((cx - w / 2, y), t, font=f, fill="black")
        else:
            d.text((cx - w / 2, y), t, font=f, fill="white", stroke_width=12, stroke_fill="black")
        y += int(a.size * 1.12)
    layer = _shadowed(layer).rotate(-a.tilt * -1, resample=Image.BICUBIC, expand=True)
    bg.paste(layer, (int((W - layer.size[0]) / 2), a.y - 120), layer)
    if a.badge:
        bf = ImageFont.truetype(str(BLACK_FONT), 64)
        r = 115
        b = Image.new("RGBA", (2 * r + 40, 2 * r + 40), (0, 0, 0, 0))
        bd = ImageDraw.Draw(b)
        bd.ellipse((20, 20, 20 + 2 * r, 20 + 2 * r), fill=YELLOW, outline="black", width=8)
        tw = bd.textlength(a.badge, font=bf)
        bd.text((20 + r - tw / 2, 20 + r - 40), a.badge, font=bf, fill="black")
        b = _shadowed(b, offset=(6, 8), blur=6).rotate(14, resample=Image.BICUBIC, expand=True)
        bg.paste(b, (W - b.size[0] - 30, a.y - 230), b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("time", type=float); ap.add_argument("out")
    ap.add_argument("lines", nargs="+")
    ap.add_argument("--y", type=int, default=1060, help="top of the first text line")
    ap.add_argument("--size", type=int, default=190)
    ap.add_argument("--zoom", type=float, default=1.0, help="zoom in for wide shots (e.g. 1.8)")
    ap.add_argument("--cx", type=float, default=0.5, help="horizontal centre of the zoom, 0-1 of the frame")
    ap.add_argument("--top", type=float, default=0.0, help="top of the zoomed photo, 0-1 of the frame height")
    ap.add_argument("--style", choices=["fun", "plain"], default="fun",
                    help="fun = tilted sticker text, last line on an orange box, optional badge; plain = v1 look")
    ap.add_argument("--badge", default="", help="short word for a yellow tilted badge, e.g. FREE (fun style)")
    ap.add_argument("--tilt", type=float, default=-5.0, help="text tilt in degrees (fun style)")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "f.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.time), "-i", a.clip, "-frames:v", "1", str(png)],
                       check=True)
        im = Image.open(png).convert("RGB")
    W, H = 1080, 1920
    sw, sh = im.size
    bg = im.resize((W, H)).filter(ImageFilter.GaussianBlur(40))
    cw = sw / a.zoom
    x0 = min(max(a.cx * sw - cw / 2, 0), sw - cw)
    y0 = min(a.top * sh, sh - cw * 4 / 3)
    photo = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + cw * 4 / 3))).resize((W, 1440), Image.LANCZOS)
    bg.paste(photo, (0, 240))
    if a.style == "fun":
        fun_text(bg, a)
    else:
        d = ImageDraw.Draw(bg)
        f = ImageFont.truetype(str(FONT), a.size)
        y = a.y
        for t in a.lines:
            w = d.textlength(t, font=f)
            d.text(((W - w) / 2, y), t, font=f, fill="white", stroke_width=10, stroke_fill="black")
            y += int(a.size * 1.05)
        uw = d.textlength(a.lines[-1], font=f)
        d.rectangle(((W - uw) / 2, y + 20, (W + uw) / 2, y + 44), fill=ORANGE)
    bg.convert("RGB").save(a.out, quality=95)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
