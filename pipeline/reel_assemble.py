"""reel_assemble.py: one-step Reel renderer. YAML editor block + raw clips -> finished 1080x1920 Instagram Reel.

    reel_assemble.py <script.md | script.yaml> [--source-dir DIR] [--out OUT.mp4] [--preview] [--keep-work]

Implements REEL_SCRIPT_TEMPLATE.md (B1-B10, D4b Read Mode, Part D YAML). See pipeline/README.md for the schema.
No auto-captions: only the hand-written `text:` entries are drawn.
Run with:  pipeline/.venv/Scripts/python.exe -I pipeline/reel_assemble.py script.md
"""
import argparse, math, os, re, shutil, subprocess, sys, tempfile, wave, json
import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_reel import whoosh, impact, pop, SR, ORANGE, FONT   # synthesized SFX, colours, font path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # project root
LOGO = os.path.join(HERE, "assets", "logo_transparent.png")
ZOOM_Y = 0.15   # zoom/punch vertical anchor: 0 = keep the top edge, 0.5 = centre. 0.15 keeps a waist-up subject's head in frame up to ~170 %
TTF = "C:/Windows/Fonts/arialbd.ttf"
W_, H_ = 1080, 1920
LOGO_BOX = (60, 275, 230, 445)       # x0,y0,x1,y1 of the top-left logo (170 px wide, ~170 tall)
FPS_DEFAULT = 30
SAFE_L, SAFE_R, SAFE_T, SAFE_B = 60, 920, 270, 1250     # text must stay inside x 60..920, y 270..1250
MAXW = 2 * (SAFE_R - W_ // 2)                          # centred text: right edge <= 920 -> max width 760
SIL_DB, SIL_MIN, HANDLE, JUMP_MIN = -35, 0.3, 0.15, 0.6
END_DUR = 2.0
TEXT_ENGINE = "ass"                  # "ass" (libass, default) | "drawtext" (legacy); set from CLI / export.text_engine
FONTS_DIR = os.path.join(HERE, "assets", "fonts")

WARN, NOTES = [], []


def warn(msg):
    WARN.append(msg); print("WARNING:", msg)


def run(cmd, cwd=None, quiet=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stderr[-3000:]); raise SystemExit(f"ffmpeg/ffprobe failed: {' '.join(cmd[:6])} ...")
    return r


def ff(args, cwd=None):
    return run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + args, cwd=cwd)


def probe(path):
    j = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
                        "-of", "json", path]).stdout)
    has_a = any(s.get("codec_type") == "audio" for s in j["streams"])
    return float(j["format"]["duration"]), has_a


# ------------------------------------------------------------------ clip resolution (Read Mode)
def resolve_clip(src, stem):
    files = [f for f in os.listdir(src) if os.path.splitext(f)[1].lower() in (".mp4", ".mov", ".m4v")]
    def match(rx):
        return [f for f in files if re.fullmatch(rx, os.path.splitext(f)[0], re.I)]
    keep = match(re.escape(stem) + r"_KEEP")
    if keep:
        return os.path.join(src, keep[0]), "KEEP"
    takes = [(int(re.search(r"_t(\d+)$", os.path.splitext(f)[0], re.I).group(1)), f) for f in match(re.escape(stem) + r"_t\d+")]
    if takes:
        takes.sort()
        return os.path.join(src, takes[-1][1]), f"last take t{takes[-1][0]} of {len(takes)}"
    plain = match(re.escape(stem))
    if plain:
        return os.path.join(src, plain[0]), "plain"
    raise SystemExit(f"clip not found for stem '{stem}' in {src}")


# ------------------------------------------------------------------ silence handling
def silences(path, D):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af", f"silencedetect=noise={SIL_DB}dB:d={SIL_MIN}",
             "-f", "null", "-"])
    out, cur = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: (-?[\d.e+-]+)", line)
        if m: cur = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end: ([\d.e+-]+)", line)
        if m and cur is not None:
            out.append((cur, float(m.group(1)))); cur = None
    if cur is not None:
        out.append((cur, D))
    return out


def keep_intervals(path, D, has_a, tin, tout, jumpcut, label):
    sil = silences(path, D) if has_a else []
    a, b = 0.0, D
    sound = [(0.0, D)]
    if sil:
        sound, p = [], 0.0
        for s, e in sil:
            if s > p + 1e-3: sound.append((p, s))
            p = e
        if p < D - 1e-3: sound.append((p, D))
    if tin == "auto":
        a = max(0.0, sound[0][0] - HANDLE) if sound else 0.0
    else:
        a = float(tin)
    if tout == "auto":
        b = min(D, sound[-1][1] + HANDLE) if sound else D
    else:
        b = min(D, float(tout))
    if not sound and has_a:
        warn(f"{label}: no sound detected, using the whole clip")
    iv = [(a, b)]
    if jumpcut and has_a:
        for s, e in sil:
            if e - s > JUMP_MIN and s > a and e < b:
                cs, ce = s + HANDLE, e - HANDLE
                new = []
                for x, y in iv:
                    if ce <= x or cs >= y: new.append((x, y)); continue
                    if cs - x > 0.05: new.append((x, cs))
                    if y - ce > 0.05: new.append((ce, y))
                iv = new
    return [(x, y) for x, y in iv if y - x > 0.05] or [(a, b)]


# ------------------------------------------------------------------ text
def font(size, ttf=None):
    return ImageFont.truetype(ttf or TTF, int(round(size)))


def twidth(s, size):
    return font(size).getlength(s)


def split_segments(words, style, hl=()):
    """-> list of (text, is_orange). Orange only when explicit: `highlight:` words, *stars*, or (TXT-CTA only) "quoted" keyword.
    No marker -> all white (no automatic last-word highlight)."""
    parts = re.split(r'(\*[^*]+\*|"[^"]+")', words)
    segs = []
    for p in parts:
        if not p: continue
        if p.startswith("*") and p.endswith("*") and len(p) > 2:
            segs.append((p[1:-1], True))
        elif p.startswith('"') and p.endswith('"') and len(p) > 2:
            segs.append((p, style == "TXT-CTA"))
        else:
            segs.append((p, False))
    if hl:
        rx = re.compile(r"(?<!\w)(" + "|".join(re.escape(h) for h in sorted(hl, key=len, reverse=True)) + r")(?!\w)", re.I)
        out = []
        for t, o in segs:
            if o: out.append((t, o)); continue
            for j, piece in enumerate(rx.split(t)):
                if piece: out.append((piece, j % 2 == 1))
        segs = out
    return segs


POS_Y = {"top": None, "upper": 1180, "mid": 900}   # `pos:` presets (top = style default y)
STYLES = {  # size, y, border, box
    "TXT-HOOK": dict(size=96, y=330, bw=8, box=False, caps=True),
    "TXT-KEY": dict(size=76, y=1000, bw=7, box=False, caps=False),
    "TXT-LABEL": dict(size=54, y=1150, bw=0, box=True, caps=False),
    "TXT-CTA": dict(size=88, y=1050, bw=8, box=False, caps=False),
}


def layout_text(t, label, y_shift=0, face=None):
    """Return list of lines; each line = (size, y, [(text, orange, x)]). Auto-shrinks/wraps to the safe zone."""
    st = STYLES[t["style"]]
    words = str(t["words"]).replace("\\n", "\n")
    if st["caps"]: words = words.upper()
    size = float(t.get("size", st["size"]))
    explicit = ("y" in t) or ("pos" in t)
    pos = str(t.get("pos", "")).lower()
    if pos and pos not in POS_Y:
        warn(f"{label}: unknown pos '{pos}' (use top|upper|mid), using style default"); pos = ""
    if "y" in t: y0 = int(t["y"])
    elif pos: y0 = POS_Y[pos] or st["y"]
    else: y0 = st["y"] + y_shift
    hl = t.get("highlight") or []
    if isinstance(hl, str): hl = [hl]
    hl = [str(h).upper() if st["caps"] else str(h) for h in hl]
    raw_lines = [l for l in words.split("\n") if l.strip()]

    def fit(lines, sz):
        w = max(twidth(re.sub(r'\*', '', l), sz) for l in lines)
        return w
    def shrink(lines):
        w = fit(lines, size)
        return size if w <= MAXW else size * MAXW / w
    sz = shrink(raw_lines)
    if sz < 0.72 * size and len(raw_lines) == 1 and " " in raw_lines[0]:      # too long: wrap onto two lines
        ws = raw_lines[0].split(" ")
        best = min(range(1, len(ws)), key=lambda i: abs(twidth(" ".join(ws[:i]), size) - twidth(" ".join(ws[i:]), size)))
        raw_lines = [" ".join(ws[:best]), " ".join(ws[best:])]
        sz = shrink(raw_lines)
        warn(f"{label}: text '{words[:40]}' wrapped onto 2 lines (too wide for the safe zone)")
    if sz < size - 0.5:
        NOTES.append(f"{label}: text shrunk {size:g} -> {sz:.0f} px to fit the safe zone")
    sz = int(sz)
    lh = int(sz * 1.18)
    out = []
    for i, l in enumerate(raw_lines):
        segs = split_segments(l, t["style"], hl)
        total = sum(twidth(s, sz) for s, _ in segs)
        x = W_ / 2 - total / 2
        placed = []
        for s, o in segs:
            placed.append((s, o, int(round(x)))); x += twidth(s, sz)
        out.append((sz, y0 + i * lh, placed))
    def block_x():
        xs = [pl[0][2] for _, _, pl in out]
        ws = [sum(twidth(s_, sz) for s_, _, _ in pl) for _, _, pl in out]
        return min(xs), max(x0 + w for x0, w in zip(xs, ws))
    bottom = y0 + len(out) * lh
    if face and not explicit:
        bx0, bx1 = block_x(); fx, fy, fw, fh = face
        m = 40
        def hit(top, bot):
            return not (bx1 < fx - m or bx0 > fx + fw + m or bot < fy - m or top > fy + fh + m)
        if hit(y0, bottom):
            h = len(out) * lh
            placed_note = None
            for nm, ny in (("below the face", fy + fh + m + 2), ("upper", POS_Y["upper"])):
                ny = min(ny, SAFE_B - 10 - h)             # keep inside the bottom safe zone
                if ny > SAFE_T and not hit(ny, ny + h):
                    y0, placed_note = ny, nm; break
            if placed_note is None:
                y0 = min(POS_Y["upper"], SAFE_B - 10 - h); placed_note = "upper (no clear spot)"
                warn(f"{label}: could not find a face-free spot for '{words[:30]}', put at y {y0}")
            NOTES.append(f"{label}: text '{words[:30]}' overlapped the face {tuple(face)}, auto-moved {placed_note} (y {y0}); set y/pos to override")
            out = [(a, y0 + n * lh, c) for n, (a, _, c) in enumerate(out)]
            bottom = y0 + len(out) * lh
    elif pos in ("upper", "mid") and "y" not in t and bottom > SAFE_B - 10:
        y0 = SAFE_B - 10 - len(out) * lh
        out = [(a, y0 + n * lh, c) for n, (a, _, c) in enumerate(out)]
        bottom = y0 + len(out) * lh
        NOTES.append(f"{label}: pos '{pos}' raised to y {y0} to stay above the bottom unsafe zone")
    if y0 <= SAFE_T or bottom >= SAFE_B:
        warn(f"{label}: text '{words[:40]}' spans y {y0}-{bottom}, outside the safe zone (>{SAFE_T}, <{SAFE_B})")
    return out


# ------------------------------------------------------------------ libass text engine
_FM = {}


def fmet(ttf):
    """(PIL font at 1000 px, ascent+descent, cap height) in 1/1000 em."""
    if ttf not in _FM:
        f = ImageFont.truetype(os.path.join(FONTS_DIR, ttf), 1000)
        a, d = f.getmetrics(); bb = f.getbbox("H")
        _FM[ttf] = (f, a + d, bb[3] - bb[1])
    return _FM[ttf]


def aw(ttf, s, E, sp=0.0):
    return fmet(ttf)[0].getlength(s) * E / 1000.0 + sp * len(s)


#  E = em px, bw = outline px, stagger = s between words, lhk = line height / E
ASTYLES = {
    "TXT-HOOK":  dict(ttf="Anton-Regular.ttf", fsk=1.757, dy=0.106, E=122, y=330, bw=7, sp=1.0, stagger=0.09, caps=True, lhk=1.20),
    "TXT-KEY":   dict(ttf="Anton-Regular.ttf", fsk=1.757, dy=0.106, E=100, y=1000, bw=6, sp=1.0, stagger=0.10, caps=True, lhk=1.20),
    "TXT-LABEL": dict(ttf="Montserrat-ExtraBold.ttf", fsk=1.593, dy=-0.03, E=44, y=1150, bw=0, sp=2.0, stagger=0.0, caps=True, lhk=1.5),
    "TXT-CTA":   dict(ttf="Anton-Regular.ttf", fsk=1.757, dy=0.106, E=112, y=1050, bw=7, sp=1.0, stagger=0.10, caps=True, lhk=1.20),
}


def _tokens(raw, style, hl, caps):
    """Words of one line as [(word, emphasised)]. Emphasis = *stars*, `highlight:` list, TXT-CTA "quoted" (split_segments)."""
    toks, prev_space = [], True
    for s_, o in split_segments(raw, style, hl):
        for w in re.split(r"(\s+)", s_):
            if not w: continue
            if w.isspace(): prev_space = True; continue
            if caps: w = w.upper()
            if not prev_space and toks:                      # glued punctuation stays with the previous word
                toks[-1] = (toks[-1][0] + w, toks[-1][1] or o)
            else:
                toks.append((w, o))
            prev_space = False
        if s_ and s_[-1].isspace(): prev_space = True
    return toks


def _line_w(ttf, toks, E, sp):
    gap = 0.26 * E; padx = 0.16 * E; w = 0.0
    for i, (t, o) in enumerate(toks):
        w += aw(ttf, t, E, sp)
        if i: w += gap + (padx * 0.8 if toks[i - 1][1] != o else 0)
    return w


def ass_layout(t, label, y_shift=0, face=None):
    """-> dict(lines=[[(word, emph, cx, w)]], E, lh, y0, bottom). Wraps to 2-4 words/line, shrinks to the safe zone, and
    mirrors the drawtext layout's y/pos/face-avoidance rules (y0 = top of the text block)."""
    sty = t["style"]; st = ASTYLES[sty]; ttf, sp = st["ttf"], st["sp"]
    words = str(t["words"]).replace("\\n", "\n")
    E = float(t.get("size", st["E"]))
    explicit = ("y" in t) or ("pos" in t)
    pos = str(t.get("pos", "")).lower()
    if pos and pos not in POS_Y:
        warn(f"{label}: unknown pos '{pos}' (use top|upper|mid), using style default"); pos = ""
    if "y" in t: y0 = int(t["y"])
    elif pos: y0 = POS_Y[pos] or st["y"]
    else: y0 = st["y"] + y_shift
    hl = t.get("highlight") or []
    if isinstance(hl, str): hl = [hl]
    hl = [str(h) for h in hl]
    lines_t = []
    for raw in words.split("\n"):
        if not raw.strip(): continue
        toks = _tokens(raw, sty, hl, st["caps"])
        n = len(toks)
        if not n: continue
        k = math.ceil(n / 4)
        while True:                                          # balanced split: <=4 words and <=MAXW per line
            base, rem = divmod(n, k); parts, i = [], 0
            for j in range(k):
                c = base + (1 if j < rem else 0); parts.append(toks[i:i + c]); i += c
            if max(_line_w(ttf, p, E, sp) for p in parts) <= MAXW or k >= n: break
            k += 1
        if k > math.ceil(n / 4):
            NOTES.append(f"{label}: '{raw[:30]}' wrapped onto {k} lines to fit the safe zone")
        lines_t += parts
    wmax = max(_line_w(ttf, p, E, sp) for p in lines_t)
    E0 = E
    if wmax > MAXW: E = E * MAXW / wmax
    if E < E0 - 0.5: NOTES.append(f"{label}: text shrunk {E0:g} -> {E:.0f} px to fit the safe zone")
    lh = int(E * st["lhk"]); gap = 0.26 * E; padx = 0.16 * E
    lines = []
    for p in lines_t:
        lw = _line_w(ttf, p, E, sp); x = W_ / 2 - lw / 2; out = []
        for i, (w_, o) in enumerate(p):
            if i: x += gap + (padx * 0.8 if p[i - 1][1] != o else 0)
            ww = aw(ttf, w_, E, sp); out.append((w_, o, x + ww / 2, ww)); x += ww
        lines.append(out)
    h = len(lines) * lh; bottom = y0 + h
    bx0 = min(l[0][2] - l[0][3] / 2 for l in lines); bx1 = max(l[-1][2] + l[-1][3] / 2 for l in lines)
    if face and not explicit:
        fx, fy, fw, fh = face; m = 40
        def hit(top, bot):
            return not (bx1 < fx - m or bx0 > fx + fw + m or bot < fy - m or top > fy + fh + m)
        if hit(y0, bottom):
            placed_note = None
            for nm, ny in (("below the face", fy + fh + m + 2), ("upper", POS_Y["upper"])):
                ny = min(ny, SAFE_B - 10 - h)
                if ny > SAFE_T and not hit(ny, ny + h):
                    y0, placed_note = ny, nm; break
            if placed_note is None:
                y0 = min(POS_Y["upper"], SAFE_B - 10 - h); placed_note = "upper (no clear spot)"
                warn(f"{label}: could not find a face-free spot for '{words[:30]}', put at y {y0}")
            NOTES.append(f"{label}: text '{words[:30]}' overlapped the face {tuple(face)}, auto-moved {placed_note} (y {y0}); set y/pos to override")
            bottom = y0 + h
    elif pos in ("upper", "mid") and "y" not in t and bottom > SAFE_B - 10:
        y0 = SAFE_B - 10 - h; bottom = y0 + h
        NOTES.append(f"{label}: pos '{pos}' raised to y {y0} to stay above the bottom unsafe zone")
    if y0 <= SAFE_T or bottom >= SAFE_B:
        warn(f"{label}: text '{words[:40]}' spans y {y0}-{bottom}, outside the safe zone (>{SAFE_T}, <{SAFE_B})")
    return dict(lines=lines, E=E, lh=lh, y0=y0, bottom=bottom)


def _ts(x):
    cs = int(round(max(0.0, x) * 100)); h, r = divmod(cs, 360000); m, r = divmod(r, 6000); s, c = divmod(r, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def _rrect(w, h, r):
    k = 0.5523 * r
    def f(v): return f"{v:.1f}"
    return (f"m {f(r)} 0 l {f(w-r)} 0 b {f(w-r+k)} 0 {f(w)} {f(r-k)} {f(w)} {f(r)} l {f(w)} {f(h-r)} "
            f"b {f(w)} {f(h-r+k)} {f(w-r+k)} {f(h)} {f(w-r)} {f(h)} l {f(r)} {f(h)} "
            f"b {f(r-k)} {f(h)} 0 {f(h-r+k)} 0 {f(h-r)} l 0 {f(r)} b 0 {f(r-k)} {f(r-k)} 0 {f(r)} 0")


ASS_ORANGE = "&H008AFF&"          # ORANGE 0xFF8A00 as ASS BGR


def ass_header():
    sty = []
    for nm, fam, bs, bord, shad in (("Hook", "Anton", 1, 7, 4), ("Label", "Montserrat ExtraBold", 3, 16, 0)):
        prim = "&H00FFFFFF"; outl = "&H00000000" if bs == 1 else "&H88000000"
        sty.append(f"Style: {nm},{fam},60,{prim},{prim},{outl},&H78000000,0,0,0,0,100,100,0,0,{bs},{bord},{shad},5,0,0,0,1")
    return ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,"
            "StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
            + "\n".join(sty) + "\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")


def _pop(cx, cy):
    return f"\\move({cx:.1f},{cy+26:.1f},{cx:.1f},{cy:.1f},0,200)\\fscx115\\fscy115\\t(0,120,\\fscx100\\fscy100)"


def ass_events(t, lay, ts, te):
    """ASS Dialogue lines for one text item. Times are beat-local seconds: every beat is rendered as its own segment
    (silence trims / speed already baked in), so no timeline offset is needed and transitions blend the text with the clip."""
    sty = t["style"]; st = ASTYLES[sty]; E = lay["E"]; lh = lay["lh"]
    fs = E * st["fsk"]            # libass s per em px, calibrated by rendering (win metrics, not hhea)
    dy = st["dy"] * E             # libass n5 centres the line box; shift so the CAP centre lands on cy
    capH = fmet(st["ttf"])[2] * E / 1000.0
    ev = []
    if sty == "TXT-LABEL":                                   # lower third: slide in from the left, no pop
        l = lay["lines"][0]; cx = (l[0][2] - l[0][3] / 2 + l[-1][2] + l[-1][3] / 2) / 2; cy = lay["y0"] + lh / 2 - dy
        txt = " ".join(f"{{\\1c{ASS_ORANGE if o else '&HFFFFFF&'}}}{w_}" for w_, o, _, _ in l)
        for ln in lay["lines"][1:]:
            txt += "\\N" + " ".join(w for w, *_ in ln)
        tags = f"\\an5\\move({cx-80:.0f},{cy:.0f},{cx:.0f},{cy:.0f},0,260)\\fad(200,150)\\fs{fs:.1f}\\fsp{st['sp']}"
        return [f"Dialogue: 1,{_ts(ts)},{_ts(te)},Label,,0,0,0,,{{{tags}}}{txt}"]
    k = 0                                                    # running word index (stagger clock)
    for li, ln in enumerate(lay["lines"]):
        cy = lay["y0"] + lh * li + lh / 2
        i = 0
        while i < len(ln):
            # a run of consecutive emphasised words shares one orange box
            run = [ln[i]]
            if ln[i][1]:
                while i + len(run) < len(ln) and ln[i + len(run)][1]: run.append(ln[i + len(run)])
            if run[0][1]:
                a0 = min(ts + k * st["stagger"], max(ts, te - 0.3))
                first0 = (ts <= 0.001 and k == 0)
                bx0 = run[0][2] - run[0][3] / 2 - 0.16 * E; bx1 = run[-1][2] + run[-1][3] / 2 + 0.16 * E
                bw_, bh_ = bx1 - bx0, capH + 0.30 * E; bcx = (bx0 + bx1) / 2
                mv = f"\\pos({bcx:.1f},{cy:.1f})" if first0 else _pop(bcx, cy)
                ev.append(f"Dialogue: 0,{_ts(a0)},{_ts(te)},Hook,,0,0,0,,{{\\an5{mv}\\fad({0 if first0 else 100},150)"
                          f"\\bord0\\shad5\\4c&H000000&\\4a&H80&\\blur1\\1c{ASS_ORANGE}\\p1}}{_rrect(bw_, bh_, 0.10 * E)}{{\\p0}}")
            for (w_, o, cx, ww) in run:
                a = min(ts + k * st["stagger"], max(ts, te - 0.3))
                first = (ts <= 0.001 and k == 0)
                mv = f"\pos({cx:.1f},{cy-dy:.1f})" if first else _pop(cx, cy - dy)
                common = f"\\an5{mv}\\fad({0 if first else 100},150)\\fs{fs:.1f}\\fsp{st['sp']}"
                if o:
                    ev.append(f"Dialogue: 1,{_ts(a)},{_ts(te)},Hook,,0,0,0,,{{{common}\\bord0\\shad0\\1c&H000000&}}{w_}")
                else:
                    ev.append(f"Dialogue: 1,{_ts(a)},{_ts(te)},Hook,,0,0,0,,{{{common}\\bord{st['bw']}\\shad4\\blur1"
                              f"\\1c&HFFFFFF&\\3c&H000000&\\4c&H000000&\\4a&H70&}}{w_}")
                k += 1
            i += len(run)
    return ev


def pill_png(path, text, size=40):
    if TEXT_ENGINE == "ass":
        size = 34; text = text.upper()
        f = font(size, os.path.join(FONTS_DIR, "Montserrat-ExtraBold.ttf"))
    else:
        f = font(size)
    w = int(f.getlength(text)) + 56; h = size + 30
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(0, 0, 0, 170), outline=(255, 138, 0, 255), width=3)
    d.text((w / 2, h / 2 + 1), text, font=f, fill=(255, 255, 255, 255), anchor="mm")
    im.save(path)
    return w, h


# ------------------------------------------------------------------ face avoidance
_CASC = None


def detect_face(path, t0, zoom, work, label):
    """Largest frontal face (x, y, w, h) in the beat's first frame after scale/crop to 1080x1920 (+ static zoom); None if none/no cv2."""
    global _CASC
    try:
        import cv2
    except ImportError:
        NOTES.append(f"{label}: opencv not installed, face avoidance skipped"); return None
    if _CASC is None:
        _CASC = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
    jp = os.path.join(work, "face_probe.png")
    vf = f"scale={W_}:{H_}:force_original_aspect_ratio=increase,crop={W_}:{H_}"
    if zoom != 1.0:
        vf = (f"scale=2*trunc({W_}*{zoom}/2):2*trunc({H_}*{zoom}/2):force_original_aspect_ratio=increase,"
              f"crop=2*trunc({W_}*{zoom}/2):2*trunc({H_}*{zoom}/2),crop={W_}:{H_}:(iw-ow)/2:(ih-oh)*{ZOOM_Y}")
    ff(["-ss", f"{t0:.3f}", "-i", path, "-frames:v", "1", "-vf", vf, jp])
    g = cv2.imread(jp, cv2.IMREAD_GRAYSCALE)
    if g is None: return None
    fs = _CASC.detectMultiScale(g, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    if len(fs) == 0: return None
    f = max(fs, key=lambda r: r[2] * r[3])
    return tuple(int(v) for v in f)


def hits_logo(x0, y0, x1, y1, pad=20):
    return x0 < LOGO_BOX[2] + pad and x1 > LOGO_BOX[0] - pad and y0 < LOGO_BOX[3] + pad and y1 > LOGO_BOX[1] - pad


# ------------------------------------------------------------------ transitions
TRN_KNOWN = {"TRN-CUT", "TRN-PUNCH", "TRN-WHIP", "TRN-ZOOMIN", "TRN-FLASH", "TRN-SPEED"}
TRN_CUTLIKE = {"TRN-JL", "TRN-MATCH", "TRN-NONE", "NONE", "TRN-FREEZE"}


# ------------------------------------------------------------------ segment (one beat)
def build_beat(i, beat, src, work, preview, hook_shift_ok=True):
    bid = str(beat.get("id", f"B{i+1}"))
    lab = f"beat {bid}"
    clip = beat.get("clip") or {}
    path, how = resolve_clip(src, clip["file"])
    D, has_a = probe(path)
    jc = clip.get("jumpcut", True)
    iv = keep_intervals(path, D, has_a, clip.get("in", "auto"), clip.get("out", "auto"), jc, lab)
    trn = str(beat.get("transition_in", "TRN-CUT") or "TRN-CUT").upper()
    if trn == "NONE": trn = "TRN-NONE"
    speed = float(clip.get("speed", 1.0))
    if trn == "TRN-SPEED" and speed == 1.0:
        warn(f"{lab}: TRN-SPEED used but clip speed is 1.0")
    raw = sum(y - x for x, y in iv)
    dur = raw / speed
    nfr = max(1, round(dur * FPS_DEFAULT)); durf = nfr / FPS_DEFAULT

    base_z = float(clip.get("crop", 100)) / 100.0
    pc = float(beat.get("punch_crop", 118)) / 100.0
    if trn == "TRN-PUNCH":
        base_z = max(base_z, pc)
    punches = [(float(a), float(b)) for a, b in (beat.get("punches") or [])]
    if punches or trn == "TRN-PUNCH":
        pass
    if base_z != 1.0 or punches:
        cond = "+".join(f"between(t,{a},{b})" for a, b in punches)
        zexpr = f"if({cond},{max(pc, base_z)},{base_z})" if cond else f"{base_z}"
    else:
        zexpr = None

    inputs = ["-i", path]
    f = []
    K = len(iv)
    for k, (a, b) in enumerate(iv):
        f.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{k}]")
        if has_a:
            f.append(f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS[a{k}]")
    if has_a:
        f.append("".join(f"[v{k}][a{k}]" for k in range(K)) + f"concat=n={K}:v=1:a=1[cv][ca]")
    else:
        f.append("".join(f"[v{k}]" for k in range(K)) + f"concat=n={K}:v=1:a=0[cv]")
        f.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{raw:.3f}[ca]")
    # Zoom is taken from the SOURCE resolution (sharp from 4K): cover-scale to W*M x H*M (M = largest zoom in
    # this beat), then per frame scale to W*z and crop W x H, anchored ZOOM_Y from the top (keeps the head in frame).
    M = max(base_z, pc if punches else base_z, 1.0) if zexpr else 1.0
    WM, HM = 2 * int(W_ * M / 2), 2 * int(H_ * M / 2)
    vf = f"[cv]setpts=PTS/{speed},fps={FPS_DEFAULT},scale={WM}:{HM}:force_original_aspect_ratio=increase,crop={WM}:{HM},setsar=1"
    if zexpr:
        vf += (f",scale=w='2*trunc({W_}*({zexpr})/2)':h='2*trunc({H_}*({zexpr})/2)':eval=frame,"
               f"crop={W_}:{H_}:x='(iw-ow)/2':y='(ih-oh)*{ZOOM_Y}',setsar=1")
    vf += f",format=yuv420p,tpad=stop_mode=clone:stop_duration=2[base]"
    f.append(vf)
    af = "[ca]"
    if speed != 1.0:
        s, parts = speed, []
        while s > 2.0: parts.append("atempo=2.0"); s /= 2.0
        while s < 0.5: parts.append("atempo=0.5"); s /= 0.5
        parts.append(f"atempo={s}")
        af += ",".join(parts) + ","
    af += "aformat=sample_rates=48000:channel_layouts=stereo,apad[sa]"
    f.append(af)

    cur = "base"
    # inserts (B-roll over the A-roll picture; A-roll audio continues)
    changes = [0.0, durf] + [a for a, _ in punches] + [b for _, b in punches]
    for n, ins in enumerate(beat.get("inserts") or []):
        ipath, _ = resolve_clip(src, ins["file"])
        at, idur = float(ins.get("at", 0)), float(ins.get("dur", 2))
        if at + idur > durf + 0.05:
            warn(f"{lab}: insert {ins['file']} ({at}+{idur}) runs past the beat end ({durf:.2f}), clipped")
            idur = max(0.1, durf - at)
        inputs += ["-i", ipath]; idx = inputs.count("-i") - 1
        f.append(f"[{idx}:v]tpad=stop_mode=clone:stop_duration=60,trim=0:{idur},setpts=PTS-STARTPTS+{at}/TB,fps={FPS_DEFAULT},"
                 f"scale={W_}:{H_}:force_original_aspect_ratio=increase,crop={W_}:{H_},setsar=1,format=yuv420p[ins{n}]")
        f.append(f"[{cur}][ins{n}]overlay=enable='between(t,{at},{at+idur})':eof_action=pass[o{n}]")
        cur = f"o{n}"; changes += [at, at + idur]
        if idur > 4.0: warn(f"{lab}: insert longer than 4 s (B7)")

    # overlays
    overlays = beat.get("overlays") or []
    has_pill = any(str(o.get("type")).upper() == "OVL-PILL" for o in overlays)
    hides = []        # beat-local (t0, t1) windows where the logo is covered by a pill/text and gets hidden
    ft = f"fontfile='{FONT}'"
    step = 0
    for o in overlays:
        ty = str(o.get("type", "")).upper()
        if ty == "OVL-PILL":
            png = f"pill_{i}.png"
            w, h = pill_png(os.path.join(work, png), str(o["words"]))
            if w > 700: warn(f"{lab}: pill text is wide ({w}px), shorten it")
            if hits_logo((W_ - w) / 2, 292, (W_ + w) / 2, 292 + h): hides.append((0.0, durf))
            inputs += ["-framerate", "30", "-loop", "1", "-t", f"{durf:.3f}", "-i", png]
            idx = inputs.count("-i") - 1
            f.append(f"[{idx}:v]format=rgba[pl{step}]")
            f.append(f"[{cur}][pl{step}]overlay=x=(W-w)/2:y=292:format=auto[p{step}]")
            cur = f"p{step}"; step += 1
        elif ty == "OVL-COUNT":
            txt = str(o["words"]); fs = 46
            x = int(SAFE_R - twidth(txt, fs))
            open(os.path.join(work, f"cnt_{i}.txt"), "w", encoding="utf-8").write(txt)
            f.append(f"[{cur}]drawtext={ft}:textfile=cnt_{i}.txt:expansion=none:fontsize={fs}:fontcolor={ORANGE}:borderw=5:bordercolor=black:x={x}:y=292[c{step}]")
            cur = f"c{step}"; step += 1
        else:
            warn(f"{lab}: overlay type '{o.get('type')}' not supported, skipped")

    # text
    texts = beat.get("text") or []
    if isinstance(texts, dict): texts = [texts]
    face = None
    if texts and any(("y" not in t and "pos" not in t) for t in texts):
        face = detect_face(path, iv[0][0], base_z, work, lab)
        if face: NOTES.append(f"{lab}: face detected at x{face[0]} y{face[1]} {face[2]}x{face[3]} (1080x1920 frame)")
    ass_ev = []
    for k, t in enumerate(texts):
        sty = str(t.get("style", "")).upper(); t["style"] = sty
        if sty not in STYLES:
            warn(f"{lab}: text style '{sty}' not supported, skipped"); continue
        ts = float(t.get("in", 0.0))
        te = float(t.get("out", 3.0 if sty == "TXT-HOOK" else durf))
        te = min(te, durf)
        words_n = len(str(t["words"]).split())
        maxw = {"TXT-HOOK": 8, "TXT-KEY": 6, "TXT-LABEL": 4, "TXT-CTA": 5}[sty]
        if words_n > maxw: warn(f"{lab}: {sty} has {words_n} words (template max {maxw})")
        if te - ts < 1.0 and te < durf - 0.01: warn(f"{lab}: {sty} on screen only {te-ts:.1f}s (min 1 s)")
        changes += [ts, te]
        if TEXT_ENGINE == "ass":
            lay = ass_layout(t, f"{lab} {sty}", y_shift=(60 if (has_pill and sty == "TXT-HOOK") else 0), face=face)
            for li, ln in enumerate(lay["lines"]):
                ly = lay["y0"] + li * lay["lh"]
                if hits_logo(ln[0][2] - ln[0][3] / 2, ly, ln[-1][2] + ln[-1][3] / 2, ly + lay["lh"]):
                    hides.append((ts, te)); break
            ass_ev += ass_events(t, lay, ts, te)
            continue
        lines = layout_text(t, f"{lab} {sty}", y_shift=(60 if (has_pill and sty == "TXT-HOOK") else 0), face=face)
        for (lsz, ly, pl) in lines:
            if hits_logo(pl[0][2], ly, pl[-1][2] + twidth(pl[-1][0], lsz), ly + lsz * 1.18):
                hides.append((ts, te)); break
        fin = 0.0 if ts <= 0.001 else 0.15
        alpha = f"min(1,max(0,(t-{ts})/{fin if fin else 0.001}))*min(1,max(0,({te}-t)/0.15))" if fin else f"min(1,max(0,({te}-t)/0.15))"
        st = STYLES[sty]
        for li, (sz, y, segs) in enumerate(lines):
            for si, (s, o, x) in enumerate(segs):
                fn = f"t_{i}_{k}_{li}_{si}.txt"
                open(os.path.join(work, fn), "w", encoding="utf-8").write(s)
                col = ORANGE if o else "white"
                extra = f":borderw={st['bw']}:bordercolor=black" if st["bw"] else ""
                if st["box"]: extra += ":box=1:boxcolor=black@0.65:boxborderw=16"
                f.append(f"[{cur}]drawtext={ft}:textfile={fn}:expansion=none:fontsize={sz}:fontcolor={col}{extra}:x={x}:y={y}:"
                         f"alpha='{alpha}':enable='between(t,{ts},{te})'[x{k}_{li}_{si}]")
                cur = f"x{k}_{li}_{si}"
    if ass_ev:
        asf = f"txt_{i}.ass"
        open(os.path.join(work, asf), "w", encoding="utf-8").write(ass_header() + chr(10).join(ass_ev) + chr(10))
        f.append(f"[{cur}]ass=filename={asf}:fontsdir=fonts[xa]")      # relative paths (cwd=work): no Windows drive-colon escaping
        cur = "xa"
    f.append(f"[{cur}]null[vo]")

    fg = os.path.join(work, f"seg_{i}.txt")
    open(fg, "w", encoding="utf-8").write(";\n".join(f))
    outp = os.path.join(work, f"seg_{i}.mov")
    crf = "30" if preview else "12"
    ff(inputs + ["-/filter_complex", fg, "-map", "[vo]", "-map", "[sa]", "-t", f"{durf:.4f}", "-r", str(FPS_DEFAULT),
                 "-c:v", "libx264", "-preset", "ultrafast" if preview else "veryfast", "-crf", crf, "-pix_fmt", "yuv420p",
                 "-c:a", "pcm_s16le", "-ar", "48000", outp], cwd=work)

    # B7 checks: longest stretch with no visual change
    pts = sorted(set(min(max(c, 0), durf) for c in changes))
    gap = max((b - a for a, b in zip(pts, pts[1:])), default=durf)
    if durf > 8 and gap > 8:
        warn(f"{lab}: {durf:.1f}s with no punch/insert/text change (FLAG, B7 max ~4 s on a talking head)")
    elif gap > 4.0:
        NOTES.append(f"{lab}: {gap:.1f}s without a visual change (B7: talking head max 4 s, fine only for action/hold shots)")
    return dict(id=bid, seg=outp, dur=durf, trn=trn, file=os.path.basename(path), how=how, iv=iv, speed=speed,
                sfx=beat.get("sfx"), raw=D, hides=hides)


# ------------------------------------------------------------------ loudness helpers
def measure_loudnorm(path, I, TP):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", f"loudnorm=I={I}:TP={TP}:LRA=11:print_format=json",
             "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    return json.loads(m.group(0))


def loudnorm_file(src, dst, I, TP, cwd):
    m = measure_loudnorm(src, I, TP)
    flt = (f"loudnorm=I={I}:TP={TP}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
           f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
           f"aresample=48000")
    ff(["-i", src, "-af", flt, "-ar", "48000", "-c:a", "pcm_s16le", dst], cwd=cwd)


def sfx_signal(kind):
    return {"SND-HIT": impact(vol=0.4), "SND-WHOOSH": whoosh(), "SND-POP": pop()}[kind]


# ------------------------------------------------------------------ main
def load_script(p):
    txt = open(p, encoding="utf-8").read()
    if p.lower().endswith((".yaml", ".yml")):
        return yaml.safe_load(txt)
    for m in re.finditer(r"```ya?ml\s*\n(.*?)```", txt, re.S):
        if re.search(r"^beats:", m.group(1), re.M):
            return yaml.safe_load(m.group(1))
    raise SystemExit("no ```yaml block containing 'beats:' found in " + p)


def mean_luma(jpg):
    return float(np.asarray(Image.open(jpg).convert("L"), dtype=float).mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script"); ap.add_argument("--source-dir"); ap.add_argument("--out")
    ap.add_argument("--preview", action="store_true", help="fast 540x960 render")
    ap.add_argument("--keep-work", action="store_true")
    ap.add_argument("--text-engine", choices=["ass", "drawtext"], help="text renderer (default ass = libass; or export.text_engine)")
    a = ap.parse_args()
    global TEXT_ENGINE

    spec = load_script(a.script)
    rid = str(spec.get("id", "reel"))
    sd = a.source_dir or spec.get("source_dir") or "."
    src = sd if os.path.isabs(sd) else os.path.join(ROOT, sd)
    src = os.path.normpath(src)
    if not os.path.isdir(src): raise SystemExit(f"source_dir not found: {src}")
    out = os.path.abspath(a.out) if a.out else os.path.join(src, f"{rid}_final.mp4")
    outdir = os.path.dirname(out); os.makedirs(outdir, exist_ok=True)
    exp = spec.get("export") or {}
    lufs = float(exp.get("lufs", -14)); fps = int(exp.get("fps", FPS_DEFAULT))
    if fps != FPS_DEFAULT: warn(f"export.fps={fps} ignored, rendering at {FPS_DEFAULT}")
    TEXT_ENGINE = str(a.text_engine or exp.get("text_engine") or "ass").lower()
    if TEXT_ENGINE not in ("ass", "drawtext"):
        warn(f"unknown text_engine '{TEXT_ENGINE}', using ass"); TEXT_ENGINE = "ass"
    NOTES.append(f"text engine: {TEXT_ENGINE}")
    beats = spec["beats"]
    work = tempfile.mkdtemp(prefix="reelasm_")
    if TEXT_ENGINE == "ass":
        os.makedirs(os.path.join(work, "fonts"))
        for fn_ in os.listdir(FONTS_DIR):
            if fn_.lower().endswith(".ttf"): shutil.copy(os.path.join(FONTS_DIR, fn_), os.path.join(work, "fonts", fn_))
    print("work dir:", work, "| source:", src)
    try:
        segs = []
        for i, b in enumerate(beats):
            s = build_beat(i, b, src, work, a.preview)
            print(f"  {s['id']}: {s['file']} ({s['how']}), intervals={[(round(x,2),round(y,2)) for x,y in s['iv']]} -> {s['dur']:.2f}s")
            segs.append(s)

        # ---- timeline + transitions
        acc = segs[0]["dur"]; starts = [0.0]; kinds = [None]
        flashes = []
        flash_n = 0
        for i in range(1, len(segs)):
            trn = segs[i]["trn"]; s = segs[i]
            if trn not in TRN_KNOWN and trn not in TRN_CUTLIKE:
                warn(f"beat {s['id']}: unknown transition '{trn}', using cut"); trn = "TRN-CUT"
            if trn == "TRN-FREEZE":
                warn(f"beat {s['id']}: TRN-FREEZE not implemented, using cut")
            kind, d = "cut", 0.0
            if trn == "TRN-WHIP": kind, d, xf = "x", 0.15, "slideleft"
            elif trn == "TRN-ZOOMIN": kind, d, xf = "x", 0.3, "zoomin"
            if kind == "x" and (s["dur"] < d * 2 or segs[i-1]["dur"] < d * 2):
                warn(f"beat {s['id']}: too short for {trn}, using cut"); kind, d = "cut", 0.0
            if trn == "TRN-FLASH":
                flash_n += 1
                if flash_n > 1: warn("TRN-FLASH used more than once (template B6: max 1 per reel)")
            st = acc - d
            starts.append(st)
            kinds.append((kind, d, xf if kind == "x" else None))
            s["start"] = st
            acc = acc + s["dur"] - d
            if trn == "TRN-FLASH": flashes.append(st)
        main_dur = acc
        total = main_dur + (END_DUR if (spec.get("end_card") or {}).get("show", True) else 0.0)
        segs[0]["start"] = 0.0
        if segs[0]["trn"] == "TRN-FLASH":
            warn("TRN-FLASH on the first beat is not allowed (hook must be visible at 0.0 s), ignored")

        # ---- SFX track
        sfx_events = []
        for i, s in enumerate(segs):
            k = s["sfx"]
            k = str(k).upper() if k is not None else None
            if k in (None, "NONE", "NULL", "FALSE"):
                if s["sfx"] is None:                       # default from transition
                    k = {"TRN-WHIP": "SND-WHOOSH", "TRN-ZOOMIN": "SND-WHOOSH", "TRN-FLASH": "SND-HIT"}.get(s["trn"])
                    if i == 0 and s["trn"] == "TRN-FLASH": k = None
                else:
                    k = None
            if k and k not in ("SND-HIT", "SND-WHOOSH", "SND-POP"):
                warn(f"beat {s['id']}: unknown sfx '{k}', skipped"); k = None
            if k: sfx_events.append((s["start"], k, s["id"]))
        for (t0, _, b0), (t1, _, b1) in zip(sfx_events, sfx_events[1:]):
            if t1 - t0 < 3.0: warn(f"SFX at {b0} and {b1} only {t1-t0:.1f}s apart (B4: max 1 every 3-4 s)")
        track = np.zeros(int(SR * (total + 2)))
        for t0, k, _ in sfx_events:
            sig = sfx_signal(k) * 0.6; i0 = int(max(0, t0) * SR)
            track[i0:i0 + len(sig)] += sig[: len(track) - i0]
        sfxp = os.path.join(work, "sfx.wav")
        with wave.open(sfxp, "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
            wf.writeframes((np.clip(track[: int(SR * total)], -1, 1) * 32767).astype("<i2").tobytes())

        # ---- stage A: voice track (concat/acrossfade of segment audio)
        ins = []
        for s in segs: ins += ["-i", s["seg"]]
        af, acc_l = [], "[0:a]"
        for i in range(1, len(segs)):
            kd = kinds[i]
            nxt = f"[an{i}]"
            if kd[0] == "x":
                af.append(f"{acc_l}[{i}:a]acrossfade=d={kd[1]}:c1=tri:c2=tri{nxt}")
            else:
                af.append(f"{acc_l}[{i}:a]concat=n=2:v=0:a=1{nxt}")
            acc_l = nxt
        af.append(f"{acc_l}apad=whole_dur={total:.3f},atrim=0:{total:.3f},aformat=sample_rates=48000:channel_layouts=stereo[vo]")
        fgA = os.path.join(work, "audioA.txt"); open(fgA, "w").write(";\n".join(af))
        ff(ins + ["-/filter_complex", fgA, "-map", "[vo]", "-c:a", "pcm_s16le", "voice_raw.wav"], cwd=work)
        loudnorm_file(os.path.join(work, "voice_raw.wav"), "voice_n.wav", lufs, -1.5, work)

        # ---- stage B: mix voice + sfx + ducked music
        music = spec.get("music") or {}
        mix_in = ["-i", "voice_n.wav", "-i", "sfx.wav"]
        # voice is only split when music needs a sidechain (an unused split output breaks ffmpeg)
        mf = ["[0:a]anull[vm]", "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[sf]"]
        labels = "[vm][sf]"; n_in = 2
        mfile = music.get("file")
        if mfile:
            mp = mfile if os.path.isabs(mfile) else (os.path.join(src, mfile) if os.path.exists(os.path.join(src, mfile)) else os.path.join(ROOT, mfile))
            if not os.path.exists(mp):
                warn(f"music file not found: {mfile}, no music")
            else:
                lvl = float(music.get("level_lufs", -26)); duck = float(music.get("duck_db", 4))
                ff(["-stream_loop", "-1", "-i", mp, "-t", f"{total:.3f}", "-vn", "-af", "aformat=sample_rates=48000:channel_layouts=stereo",
                    "-c:a", "pcm_s16le", "music_raw.wav"], cwd=work)
                loudnorm_file(os.path.join(work, "music_raw.wav"), "music_n.wav", lvl, -3, work)
                mix_in += ["-i", "music_n.wav"]; n_in = 3
                mf[0] = "[0:a]asplit=2[vm][vsc]"
                ratio = min(20.0, max(1.1, 1.0 / max(0.05, 1 - duck / 20.0)))
                mf.append(f"[2:a]afade=t=in:d=0.5,afade=t=out:st={total-1.0:.2f}:d=1.0[mu]")
                mf.append(f"[mu][vsc]sidechaincompress=threshold=0.02:ratio={ratio:.2f}:attack=15:release=350:makeup=1[md]")
                labels = "[vm][sf][md]"
        mf.append(f"{labels}amix=inputs={labels.count('[')}:normalize=0:duration=longest,atrim=0:{total:.3f}[mixed]")
        mf_p = os.path.join(work, "audioB.txt"); open(mf_p, "w").write(";\n".join(mf))
        ff(mix_in + ["-/filter_complex", mf_p, "-map", "[mixed]", "-c:a", "pcm_s16le", "-ar", "48000", "mix_raw.wav"], cwd=work)
        loudnorm_file(os.path.join(work, "mix_raw.wav"), "final.wav", lufs, -1.0, work)

        # ---- stage C: video assembly
        vf, acc_l = [], "[0:v]"
        for i in range(len(segs)):
            vf.append(f"[{i}:v]settb=AVTB,setpts=PTS-STARTPTS,fps={FPS_DEFAULT},settb=1/{FPS_DEFAULT},setsar=1[sv{i}]")
        acc_l = "[sv0]"; accd = segs[0]["dur"]
        for i in range(1, len(segs)):
            kd = kinds[i]; nxt = f"[vc{i}]"
            if kd[0] == "x":
                vf.append(f"{acc_l}[sv{i}]xfade=transition={kd[2]}:duration={kd[1]}:offset={accd-kd[1]:.4f}{nxt}")
                accd += segs[i]["dur"] - kd[1]
            else:
                # concat resets the timebase; force 1/FPS so a later xfade sees matching inputs
                vf.append(f"{acc_l}[sv{i}]concat=n=2:v=1:a=0,settb=1/{FPS_DEFAULT}{nxt}")
                accd += segs[i]["dur"]
            acc_l = nxt
        cur = acc_l
        for n, t0 in enumerate(flashes):
            vf.append(f"{cur}drawbox=x=0:y=0:w=iw:h=ih:color=white@0.9:t=fill:enable='between(t,{t0:.3f},{t0+0.1:.3f})'[fl{n}]")
            cur = f"[fl{n}]"
        nseg = len(segs)
        logo_i, logo2_i = nseg, nseg + 1
        vf.append(f"color=c={ORANGE}:s={W_}x12:r={FPS_DEFAULT}:d={main_dur:.3f}[bar]")
        vf.append(f"{cur}[bar]overlay=x='-W+W*t/{main_dur:.3f}':y=0[bb]")
        vf.append(f"[{logo_i}:v]scale=170:-1,format=rgba,colorchannelmixer=aa=0.6[lg]")
        hid = [(s_["start"] + a_, s_["start"] + b_) for s_ in segs for a_, b_ in s_["hides"]]
        en = ("" if not hid else ":enable='not(" + "+".join(f"between(t,{a_:.3f},{b_:.3f})" for a_, b_ in hid) + ")'")
        if hid: NOTES.append("logo hidden while a pill/text overlaps it: " + ", ".join(f"{a_:.1f}-{b_:.1f}s" for a_, b_ in hid))
        vf.append(f"[bb][lg]overlay=60:275{en}[vmain]")
        ec = spec.get("end_card") or {}
        if ec.get("show", True):
            l1 = str(ec.get("line1", "The Project Shop")); l2 = str(ec.get("line2", "Learn it. Build it. Own it."))
            l3 = str(ec.get("line3", "Follow for more"))
            for n, (s_, sz) in enumerate(((l1, 58), (l2, 58), (l3, 70))):
                open(os.path.join(work, f"end{n}.txt"), "w", encoding="utf-8").write(s_)
            ft = f"fontfile='{FONT}'"
            vf.append(f"color=c=white:s={W_}x{H_}:r={FPS_DEFAULT}:d={END_DUR},setsar=1,format=yuv420p[ebg]")
            vf.append(f"[{logo2_i}:v]scale=700:-1,format=rgba[lgbig]")
            vf.append(f"[ebg][lgbig]overlay=(W-w)/2:360,"
                      f"drawtext={ft}:textfile=end0.txt:fontsize=58:fontcolor=black:x=(w-text_w)/2:y=800,"
                      f"drawtext={ft}:textfile=end1.txt:fontsize=58:fontcolor={ORANGE}:x=(w-text_w)/2:y=880,"
                      f"drawtext={ft}:textfile=end2.txt:fontsize=70:fontcolor=black:x=(w-text_w)/2:y=1040[end]")
            vf.append(f"[vmain]format=yuv420p[vm2]")
            vf.append(f"[vm2][end]concat=n=2:v=1:a=0[vall]")
        else:
            vf.append("[vmain]format=yuv420p[vall]")
        if a.preview:
            vf.append("[vall]scale=540:960[vfin]")
        else:
            vf.append("[vall]null[vfin]")
        fgC = os.path.join(work, "video.txt"); open(fgC, "w", encoding="utf-8").write(";\n".join(vf))
        vin = []
        for s in segs: vin += ["-i", s["seg"]]
        vin += ["-i", LOGO, "-i", LOGO, "-i", "final.wav"]
        ff(vin + ["-/filter_complex", fgC, "-map", "[vfin]", "-map", f"{nseg+2}:a", "-r", str(FPS_DEFAULT),
                  "-c:v", "libx264", "-preset", "ultrafast" if a.preview else "medium", "-crf", "30" if a.preview else "18",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], cwd=work)

        # ---- QC
        qc_lines = []
        fdur, _ = probe(out)
        info = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                               "stream=width,height,r_frame_rate,codec_name", "-of", "json", out]).stdout)["streams"][0]
        r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"])
        lm = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr); pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
        got_lufs = float(lm[-1]) if lm else float("nan"); got_tp = float(pk[-1]) if pk else float("nan")
        target = float(spec.get("length_s", 0) or 0)
        if target and abs(fdur - target) > 2.0:
            warn(f"total {fdur:.1f}s differs from target {target:g}s by more than 2 s")
        if abs(got_lufs - lufs) > 1.0: warn(f"loudness {got_lufs:.1f} LUFS vs target {lufs:g}")
        frames = {"t0.0": 0.0, "t1.0": 1.0, "mid": fdur / 2, "end": max(0.0, fdur - 0.1)}
        lumas = {}
        for k, t in frames.items():
            jp = os.path.join(outdir, f"{rid}_qc_{k}.jpg")
            ff(["-ss", f"{t:.3f}", "-i", out, "-frames:v", "1", "-q:v", "3", jp])
            lumas[k] = mean_luma(jp)
        if lumas["t0.0"] > 215: warn(f"frame at t=0 is very bright (luma {lumas['t0.0']:.0f}): flash at start?")
        qc_lines += [f"QC report: {rid}", f"output: {out}",
                     f"video: {info['codec_name']} {info['width']}x{info['height']} @ {info['r_frame_rate']}",
                     f"duration: {fdur:.2f}s (target {target:g}s, main {main_dur:.2f}s + end card {total-main_dur:.1f}s)",
                     f"loudness: {got_lufs:.1f} LUFS integrated (target {lufs:g}), true peak {got_tp:.1f} dBFS", "",
                     "beats:"]
        for s in segs:
            qc_lines.append(f"  {s['id']}: {s['dur']:.2f}s start {s['start']:.2f}s  {s['trn']}  {s['file']} [{s['how']}] "
                            f"intervals {len(s['iv'])} speed {s['speed']:g}")
        qc_lines += ["", "frame brightness (mean luma 0-255): " + ", ".join(f"{k}={v:.0f}" for k, v in lumas.items()), "",
                     f"warnings ({len(WARN)}):"] + [f"  - {w}" for w in WARN] + ["", "notes:"] + [f"  - {n}" for n in NOTES]
        qcp = os.path.join(outdir, f"{rid}_qc.txt")
        open(qcp, "w", encoding="utf-8").write("\n".join(qc_lines) + "\n")
        print("\n".join(qc_lines))
        print("wrote", out)
    finally:
        if a.keep_work: print("work kept:", work)
        else: shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
