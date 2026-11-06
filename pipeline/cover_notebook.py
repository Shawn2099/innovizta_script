"""Full-screen "engineering notebook" reel cover (1080x1920), no face. Hand-made look, not glossy AI.

Graph paper, a handwritten kicker, a huge Anton hero line on a rough highlighter stroke, a tilted sticky note
with a hand-ticked checklist, small logo. Everything important sits inside the 3:4 grid crop (y 240-1680).

Usage:
  pipeline\.venv\Scripts\python.exe -I pipeline\cover_notebook.py <out.jpg> --kicker "what really happens in" \
      --hero "1 HOUR?" --note "topic" "career fit" "real problem" "parts + plan" [--tape "project consult"] [--seed 7]
"""
import argparse
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
ANTON = HERE / "assets" / "fonts" / "Anton-Regular.ttf"
LOGO = HERE / "assets" / "logo_transparent.png"
HAND = Path(r"C:\Windows\Fonts\Inkfree.ttf")          # handwriting (Windows 11)
PAPER, GRID, GRID_MAJOR = (247, 242, 232), (196, 214, 232), (160, 190, 222)
ORANGE, INK, NOTE = (247, 147, 30), (22, 22, 22), (255, 226, 92)
W, H = 1080, 1920


def jitter_line(d, pts, width, fill, rnd, j=3):
    """Polyline with small random wobble, drawn twice, so it reads like a marker stroke."""
    for _ in range(2):
        q = [(x + rnd.uniform(-j, j), y + rnd.uniform(-j, j)) for x, y in pts]
        d.line(q, fill=fill, width=width, joint="curve")


def paper():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=GRID_MAJOR if x % 200 == 0 else GRID, width=2 if x % 200 == 0 else 1)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=GRID_MAJOR if y % 200 == 0 else GRID, width=2 if y % 200 == 0 else 1)
    noise = Image.effect_noise((W, H), 18).convert("RGB")
    return Image.blend(im, noise, 0.05)


def highlighter(size, rnd):
    """Rough translucent orange stroke (uneven edges, slight taper) on its own layer."""
    w, h = size
    lay = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    top = [(40 + i * (w / 12), 40 + rnd.uniform(-10, 12)) for i in range(13)]
    bot = [(40 + i * (w / 12), 40 + h + rnd.uniform(-12, 10)) for i in reversed(range(13))]
    d.polygon(top + bot, fill=ORANGE + (215,))
    return lay.filter(ImageFilter.GaussianBlur(1.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--kicker", default="what really happens in")
    ap.add_argument("--hero", default="1 HOUR?")
    ap.add_argument("--note", nargs="*", default=[])
    ap.add_argument("--tape", default="", help="handwritten label on the sticky note's tape strip")
    ap.add_argument("--mark", choices=["tick", "num"], default="tick",
                    help="tick = ticked boxes (things we do); num = circled 1,2,3 (problems / options)")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    im = paper().convert("RGBA")

    # handwritten kicker, slightly tilted
    kf = ImageFont.truetype(str(HAND), 92)
    k = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    kd = ImageDraw.Draw(k)
    kw = kd.textlength(a.kicker, font=kf)
    kd.text(((W - kw) / 2, 40), a.kicker, font=kf, fill=INK)
    k = k.rotate(3, resample=Image.BICUBIC)
    im.alpha_composite(k, (0, 300))

    # hero: huge Anton on a highlighter stroke, tilted the other way
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    hs = 300                                            # shrink long hero lines to fit 940 px
    while tmp.textlength(a.hero, font=ImageFont.truetype(str(ANTON), hs)) > 940 and hs > 120:
        hs -= 10
    hf = ImageFont.truetype(str(ANTON), hs)
    hw = tmp.textlength(a.hero, font=hf)
    hero = Image.new("RGBA", (int(hw) + 200, 460), (0, 0, 0, 0))
    hl = highlighter((int(hw) + 40, int(150 * hs / 300)), rnd)
    hero.alpha_composite(hl, (40, int(175 * hs / 300)))
    ImageDraw.Draw(hero).text((100, 10), a.hero, font=hf, fill=INK)
    hero = hero.rotate(-3, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(hero, ((W - hero.size[0]) // 2, 440))

    # sticky note with a hand-ticked checklist
    if a.note:
        nf = ImageFont.truetype(str(HAND), 66)
        nw, nh = 640, 120 + 96 * len(a.note)
        note = Image.new("RGBA", (nw + 60, nh + 60), (0, 0, 0, 0))
        sh = Image.new("RGBA", note.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((38, 44, 38 + nw, 44 + nh), fill=(0, 0, 0, 90))
        note.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
        nd = ImageDraw.Draw(note)
        nd.rectangle((24, 24, 24 + nw, 24 + nh), fill=NOTE)
        tf = ImageFont.truetype(str(HAND), 50)
        tw = nd.textlength(a.tape, font=tf) if a.tape else 140
        nd.rectangle((24 + nw / 2 - tw / 2 - 30, 0, 24 + nw / 2 + tw / 2 + 30, 62), fill=(238, 232, 212, 235))  # tape
        if a.tape:
            nd.text((24 + nw / 2 - tw / 2, 2), a.tape, font=tf, fill=(200, 40, 30))
        y = 90
        for n, item in enumerate(a.note, 1):
            bx, by = 80, y + 12
            if a.mark == "num":
                import math
                pts = [(bx + 22 + 34 * math.cos(math.radians(d)) + rnd.uniform(-2, 2),
                        by + 22 + 32 * math.sin(math.radians(d)) + rnd.uniform(-2, 2)) for d in range(-60, 330, 15)]
                nd.line(pts, fill=(200, 40, 30), width=5, joint="curve")
                nd.text((bx + 8, by - 22), str(n), font=nf, fill=(200, 40, 30))
            else:
                jitter_line(nd, [(bx, by), (bx + 44, by), (bx + 44, by + 44), (bx, by + 44), (bx, by)], 4, INK, rnd, 2)
                jitter_line(nd, [(bx + 6, by + 22), (bx + 20, by + 40), (bx + 58, by - 14)], 7, (200, 40, 30), rnd, 2)
            nd.text((bx + 80, y), item, font=nf, fill=INK)
            y += 96
        note = note.rotate(4, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(note, ((W - note.size[0]) // 2 + 30, 900))

        # hand-drawn arrow from the hero down to the note
        d = ImageDraw.Draw(im)
        jitter_line(d, [(170, 820), (150, 900), (165, 980), (215, 1040)], 7, INK, rnd, 2)
        jitter_line(d, [(215, 1040), (170, 1030)], 7, INK, rnd, 2)
        jitter_line(d, [(215, 1040), (205, 995)], 7, INK, rnd, 2)

    # small logo at the bottom of the grid-safe area
    if LOGO.exists():
        lg = Image.open(LOGO).convert("RGBA")
        lg = lg.resize((300, int(300 * lg.size[1] / lg.size[0])), Image.LANCZOS)
        im.alpha_composite(lg, ((W - 300) // 2, 1560 - lg.size[1] // 2))
    im.convert("RGB").save(a.out, quality=95)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
