"""Cut candidate clips from long source videos using a manifest.

Usage:
  pipeline\.venv\Scripts\python.exe -I pipeline\extract_clips.py <vidoes_dir> [--out filtered] [--crf 16]

Reads <vidoes_dir>/<out>/manifest.csv (columns: clip,source,start,end,machine_note), writes
<vidoes_dir>/<out>/<clip>.mp4 (re-encoded, rotation applied, so portrait stays portrait).
Skips clips that already exist. Originals are never touched.
Creates <out>/CLIPS.md only if it does not exist (it is hand-edited afterwards).
"""
import argparse
import csv
import subprocess
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vidoes_dir")
    ap.add_argument("--out", default="filtered")
    ap.add_argument("--crf", default="16")
    a = ap.parse_args()
    root = Path(a.vidoes_dir)
    out = root / a.out
    rows = list(csv.DictReader((out / "manifest.csv").open(encoding="utf-8")))
    for r in rows:
        dst = out / f"{r['clip']}.mp4"
        if dst.exists():
            print("skip", dst.name)
            continue
        src = root / r["source"]
        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", r["start"], "-to", r["end"], "-i", str(src),
               "-c:v", "libx264", "-crf", a.crf, "-preset", "fast", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", str(dst)]
        subprocess.run(cmd, check=True)
        print("made", dst.name)

    md = out / "CLIPS.md"
    if not md.exists():
        lines = ["# Filtered clips tracker", "",
                 "Machine notes come from frames + audio levels only (no transcripts: Malayalam is mis-heard).",
                 "Fill the last column with what is actually said / the story. The story column is the source of truth.", "",
                 "| Clip | Source (original) | Time | Length | Machine-extracted content | Your story / content |",
                 "|---|---|---|---|---|---|"]
        for r in rows:
            s, e = float(r["start"]), float(r["end"])
            lines.append(f"| {r['clip']} | {r['source']} | {s:g}-{e:g}s | {e - s:.0f}s | {r['machine_note']} |  |")
        md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("wrote CLIPS.md")


if __name__ == "__main__":
    main()
