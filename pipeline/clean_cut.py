"""Remove silent gaps with plain FFmpeg (re-encoded, no black frames) and map times.

python clean_cut.py <in.mp4> <out.mp4> [--map t1,t2,...]   (times are seconds in the INPUT; prints their time in the OUTPUT)
"""
import argparse, os, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--min-gap", type=float, default=0.40)
ap.add_argument("--pad", type=float, default=0.09)
ap.add_argument("--db", default="-35dB")
ap.add_argument("--map", default="")
a = ap.parse_args()
inp, out = os.path.abspath(a.inp), os.path.abspath(a.out)

log = subprocess.run(["ffmpeg", "-hide_banner", "-i", inp, "-af", f"silencedetect=n={a.db}:d={a.min_gap}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", inp]))

segs, cur = [], 0.0
for s, e in zip(starts, ends):
    if s - cur > 0.2:
        segs.append((max(0, cur - a.pad if segs else cur), min(total, s + a.pad)))
    cur = e
if total - cur > 0.2:
    segs.append((max(0, cur - a.pad), total))

parts, labels = [], ""
for i, (s, e) in enumerate(segs):
    parts.append(f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}]")
    parts.append(f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-s-0.02:.3f}:d=0.02[a{i}]")
    labels += f"[v{i}][a{i}]"
parts.append(f"{labels}concat=n={len(segs)}:v=1:a=1[vv][a];[vv]fps=30[v]")
fg = os.path.join(os.path.dirname(out), "_clean_filter.txt")
open(fg, "w").write(";\n".join(parts))
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", inp, "-/filter_complex", fg, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", out], check=True)
print("segments:", len(segs), "cuts:", len(segs) - 1, "kept", round(sum(e - s for s, e in segs), 2), "of", round(total, 2))

def new_time(t):
    acc = 0.0
    for s, e in segs:
        if s <= t <= e:
            return acc + t - s
        acc += e - s
    return None
if a.map:
    print("map:", {t: (None if new_time(float(t)) is None else round(new_time(float(t)), 2)) for t in a.map.split(",")})
