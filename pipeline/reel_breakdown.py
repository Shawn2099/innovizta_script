"""Reel breakdown: objective metrics + contact sheets for any folder of reels.

Usage:
  python pipeline/reel_breakdown.py <folder_with_mp4s> <out_folder>

For every .mp4 (searched recursively) writes into <out_folder>/<name>/:
  hook.jpg   - first 3 s at 4 fps (12 frames, 6x2 grid)  -> what the viewer sees before deciding
  sheet.jpg  - 12 frames spread across the whole reel (6x2 grid)
  metrics.json - duration, resolution, cut count, cuts/sec, first-cut time,
                 voiced_ratio = NON-SILENT share (music counts too; not speech), loudness
                 cuts = hard scene changes only (jump cuts in the same framing are missed)
And <out_folder>/summary.csv with one row per reel.
Needs ffmpeg/ffprobe on PATH. Reusable for our own reels too.
"""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="ignore")


def probe(p):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height:format=duration", "-of", "json", str(p)]).stdout
    j = json.loads(out or "{}")
    st = (j.get("streams") or [{}])[0]
    return float(j.get("format", {}).get("duration", 0) or 0), st.get("width"), st.get("height")


def cuts(p, thr=0.30):
    err = run(["ffmpeg", "-hide_banner", "-i", str(p), "-vf",
               f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"]).stderr
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", err)]


def audio(p, dur):
    err = run(["ffmpeg", "-hide_banner", "-i", str(p), "-af",
               "silencedetect=n=-35dB:d=0.4,volumedetect", "-vn", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    silent = sum(e - s for s, e in zip(starts, ends))
    if len(starts) > len(ends):
        silent += max(0.0, dur - starts[-1])
    mean = re.search(r"mean_volume: (-?[\d.]+) dB", err)
    has_audio = "Audio:" in err
    return (round(1 - silent / dur, 2) if dur and has_audio else 0.0,
            float(mean.group(1)) if mean else None, has_audio)


def sheets(p, out, dur):
    out.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", "3", "-i", str(p), "-vf",
         "fps=4,scale=240:-2,tile=6x2", "-frames:v", "1", str(out / "hook.jpg")])
    fps = 12 / max(dur, 1)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-vf",
         f"fps={fps:.4f},scale=240:-2,tile=6x2", "-frames:v", "1", str(out / "sheet.jpg")])


def main(src, dst):
    src, dst = Path(src), Path(dst)
    rows = []
    for p in sorted(src.rglob("*.mp4")):
        name = f"{p.parent.name}_{p.stem}"
        dur, w, h = probe(p)
        c = cuts(p)
        voiced, mean_db, has_audio = audio(p, dur)
        sheets(p, dst / name, dur)
        m = {"name": name, "account": p.parent.name, "code": p.stem, "duration_s": round(dur, 1),
             "width": w, "height": h, "cuts": len(c), "cuts_per_10s": round(len(c) / dur * 10, 2) if dur else 0,
             "first_cut_s": round(c[0], 2) if c else None, "avg_shot_s": round(dur / (len(c) + 1), 2) if dur else 0,
             "voiced_ratio": voiced, "mean_db": mean_db, "has_audio": has_audio}
        (dst / name / "metrics.json").write_text(json.dumps(m, indent=1))
        rows.append(m)
        print(name, m["duration_s"], "s", m["cuts"], "cuts", "voiced", voiced)
    if rows:
        with open(dst / "summary.csv", "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
