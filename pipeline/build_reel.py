"""Energetic Reel builder (no captions). Reusable for every day.

python build_reel.py <cut.mp4> <out.mp4> "<HOOK LINE 1>" "<HOOK LINE 2>" <logo_transparent.png> [options]

Features: 9:16 crop, optional punch-in zooms, synthesized SFX (no licensing issues), big pop-in hook text
(visible from t=0.0), top progress bar, transparent logo, branded end card, loudness normalised.

Template-aligned options (REEL_SCRIPT_TEMPLATE.md B0/B1/B10):
  --flash       opt-in white-flash open (0.18 s). DEFAULT is no flash: frame 1 shows subject + hook text.
  --hook-y N    y of hook line 1 (default 300; line 2 sits at N+160). Safe zone on 1080x1920: >270 px from
                top, >670 px from bottom (text bottom <= 1250), >60 px left, >160 px right (text right <= 920).
                Built-in text is placed inside it; --text y values are left alone but a WARNING is printed.
  --push 0      disable the slow push-in; use it for CUT-HOLD (continuous shot) formats. Default stays 0.06.
  --end1/2/3    end-card lines (default: "The Project Shop" / "Learn it. Build it. Own it." / "Follow for more").
  --no-end      no end card, fade to white so the Reel loops.

Recommended for our template (no flash, hook-y 300, no push for hold formats):
  python build_reel.py cut.mp4 out.mp4 "HOOK 1" "HOOK 2" logo_transparent.png --no-end --hook-y 300 --push 0
"""
import argparse, subprocess, wave, subprocess, tempfile, os
import numpy as np

SR = 48000
ORANGE = "0xFF8A00"
FONT = "C\\:/Windows/Fonts/arialbd.ttf"


def dur(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def whoosh(length=0.45, vol=0.35):
    n = int(SR * length)
    t = np.linspace(0, 1, n)
    noise = np.random.default_rng(1).standard_normal(n)
    # sweeping one-pole lowpass: dark -> bright
    a = 0.05 + 0.85 * t
    y = np.zeros(n)
    prev = 0.0
    for i in range(n):
        prev += a[i] * (noise[i] - prev)
        y[i] = prev
    env = np.sin(np.pi * t) ** 1.5
    y = y * env
    return y / np.max(np.abs(y)) * vol


def impact(length=0.5, vol=0.55):
    n = int(SR * length)
    t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (140 * np.exp(-t * 9) + 45) * t) * np.exp(-t * 7)
    click = np.random.default_rng(2).standard_normal(n) * np.exp(-t * 60) * 0.4
    y = thump + click
    return y / np.max(np.abs(y)) * vol


def pop(length=0.14, vol=0.22):
    n = int(SR * length)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 620 * t) * np.exp(-t * 28) * vol


def write_sfx(path, total, punches=None):
    track = np.zeros(int(SR * (total + 1)))
    def place(sig, at):
        i = int(at * SR)
        track[i:i + len(sig)] += sig[: len(track) - i]
    place(impact(vol=0.4), 0.0)
    for p in (punches or []):
        place(pop(), max(0.0, p - 0.03))
    pcm = (np.clip(track, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cut"); ap.add_argument("out"); ap.add_argument("h1"); ap.add_argument("h2"); ap.add_argument("logo")
    ap.add_argument("--punches", default="", help="comma list of start-end seconds, e.g. 20-24,50-53")
    ap.add_argument("--push", type=float, default=0.06, help="slow push-in over the whole video; use 0 for CUT-HOLD (continuous shot) formats")
    ap.add_argument("--punch", type=float, default=0.10, help="extra zoom during a punch window")
    ap.add_argument("--hook-end", type=float, default=3.0)
    ap.add_argument("--end1", default="The Project Shop")
    ap.add_argument("--end2", default="Learn it. Build it. Own it.")
    ap.add_argument("--end3", default="Follow for more")
    ap.add_argument("--flash", action="store_true", help="opt-in white-flash open (default: no flash, hook visible at t=0)")
    ap.add_argument("--hook-y", type=int, default=300, help="y of hook line 1 (line 2 = +160); safe zone is y>270 and text bottom<=1250")
    ap.add_argument("--text", action="append", default=[], help="start|end|text|size|color|y[|slam]  (repeatable; slam = zoom-in pop)")
    ap.add_argument("--box", action="append", default=[], help="start|end|x|y|w|h|color@alpha e.g. 0|3|0|150|1080|300|black@0.6 (repeatable; drawn under texts)")
    ap.add_argument("--fade-v", type=float, default=0.15, help="no-end mode: fade-to-white length at the end")
    ap.add_argument("--fade-a", type=float, default=0.08, help="no-end mode: audio fade-out length at the end")
    ap.add_argument("--no-end", action="store_true", help="no end card; fade to white so the Reel loops")
    a = ap.parse_args()

    cut = os.path.abspath(a.cut); out = os.path.abspath(a.out); logo = os.path.abspath(a.logo)
    D = dur(cut)
    work = os.path.dirname(out)
    sfx = os.path.join(work, "_sfx.wav")
    wins = [tuple(float(x) for x in p.split("-")) for p in a.punches.split(",") if p.strip()]
    texts = [t.split("|") for t in a.text]
    write_sfx(sfx, D, [w[0] for w in wins] + [float(t[0]) for t in texts])
    he = a.hook_end
    for parts in texts:  # warn (never change) user-provided --text positions outside the safe zone
        try:
            ty, tsz = float(parts[5]), float(parts[3])
        except (ValueError, IndexError):
            continue
        if ty <= 270 or ty + tsz >= 1250:
            print(f"WARNING: --text '{parts[2]}' y={ty:g} size={tsz:g} is outside the safe zone (need y>270 and y+size<1250)")
    if a.hook_y <= 270 or a.hook_y + 160 + 118 >= 1250:
        print(f"WARNING: --hook-y {a.hook_y} puts hook text outside the safe zone (need >270 top, <1250 bottom)")
    flash = "fade=t=in:st=0:d=0.18:color=white,\n" if a.flash else ""
    y1, y2 = a.hook_y, a.hook_y + 160
    extra = ""
    for b in a.box:
        bs, be, bx, by, bw, bh, bc = b.split("|")
        bc = bc.replace("orange", ORANGE)
        extra += f",\ndrawbox=x={bx}:y={by}:w={bw}:h={bh}:color={bc}:t=fill:enable='between(t,{bs},{be})'"
    for parts in texts:
        s, e, txt, size, color, y = parts[:6]
        slam = len(parts) > 6 and parts[6] == "slam"
        col = ORANGE if color == "orange" else color
        fsz = f"'if(lt(t-{s}\\,0.18)\\,{size}*(1.7-3.9*(t-{s}))\\,{size})'" if slam else size
        extra += (f",\ndrawtext=fontfile='{FONT}':text='{txt}':fontsize={fsz}:fontcolor={col}:borderw=7:bordercolor=black:"
                  f"x=(w-text_w)/2:y={y}:alpha='min(1\\,max(0\\,(t-{s})/0.2))*min(1\\,max(0\\,({e}-t)/0.2))':"
                  f"enable='between(t,{s},{e})'")
    # smooth zoom: slow push-in + eased punch windows (0.3 s in / 0.3 s out)
    zexpr = f"1+{a.push}*t/{D}" + "".join(
        f"+{a.punch}*min(1\\,max(0\\,(t-{s})/0.3))*min(1\\,max(0\\,({e}-t)/0.3))" for s, e in wins)
    ft = f"fontfile='{FONT}'"
    pop1 = "if(lt(t\\,0.22)\\,100+t*55\\,112)"
    pop2 = "if(lt(t\\,0.30)\\,104+t*47\\,118)"
    fg = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,
scale=w='1080*({zexpr})':h=-2:eval=frame,crop=1080:1920:(iw-1080)/2:(ih-1920)/5,
{flash}drawtext={ft}:text='{a.h1}':fontsize='{pop1}':fontcolor=white:borderw=9:bordercolor=black:x=(w-text_w)/2:y={y1}:enable='between(t,0,{he})',
drawtext={ft}:text='{a.h2}':fontsize='{pop2}':fontcolor={ORANGE}:borderw=9:bordercolor=black:x=(w-text_w)/2:y={y2}:enable='between(t,0,{he})'{extra}[b0];
color=c={ORANGE}:s=1080x14:r=30:d={D}[bar];
[b0][bar]overlay=x='-W+W*t/{D}':y=0[b1];
[1:v]scale=340:-1,format=rgba[lg];
[b1][lg]overlay=W-w-24:50:enable='gte(t,{he})'[main];
color=c=white:s=1080x1920:d=3.2:r=30,setsar=1[bg];
[1:v]scale=700:-1,format=rgba[lgbig];
[bg][lgbig]overlay=(W-w)/2:360,
drawtext={ft}:text='{a.end1}':fontsize=58:fontcolor=black:x=(w-text_w)/2:y=800,
drawtext={ft}:text='{a.end2}':fontsize=58:fontcolor={ORANGE}:x=(w-text_w)/2:y=880,
drawtext={ft}:text='{a.end3}':fontsize=70:fontcolor=black:x=(w-text_w)/2:y=1040[end];
[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo[v0];
[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55[s0];
[v0][s0]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={D-0.4}:d=0.4[ma];
anullsrc=r=48000:cl=stereo:d=3.2[ea];
[main][ma][end][ea]concat=n=2:v=1:a=1[v][a]
""".strip()
    if a.no_end:
        head = fg.split("color=c=white:s=1080x1920:d=3.2")[0]
        head += (f"[main]fade=t=out:st={D-a.fade_v}:d={a.fade_v}:color=white[v];\n"
                 "[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo[v0];\n"
                 "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55[s0];\n"
                 f"[v0][s0]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={D-a.fade_a}:d={a.fade_a}[a]")
        fg = head
    fgp = os.path.join(work, "_filter.txt")
    open(fgp, "w", encoding="utf-8").write(fg)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", cut, "-i", logo, "-i", sfx,
                    "-/filter_complex", fgp, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
                   check=True, cwd=work)
    print("wrote", out, "duration", dur(out))
