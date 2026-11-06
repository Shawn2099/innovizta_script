"""Rough Whisper pass over every clip in a folder; ROUGH LOCATOR ONLY (Malayalam is mis-heard).

Usage:
  pipeline\.venv\Scripts\python.exe -I pipeline\whisper_clips.py <clips_dir> [--model large-v3]

For each clipNN.mp4 writes <clips_dir>/whisper/clipNN.json with:
  ml  : Malayalam/Manglish transcription (language forced to ml)
  en  : Whisper's own English translation (gist only)
Then rewrites CLIPS.md, adding 'Whisper (rough, ml)' and 'Whisper English gist' columns before the
last (user story) column. Existing user text is preserved. Safe to re-run; done clips are skipped.
"""
import argparse
import json
import re
from pathlib import Path

PROMPT = ("Casual Malayalam-English (Manglish) talk by an engineering startup founder about B.Tech "
          "final year projects, viva, project assistance company in India.")


def run(model, path, task):
    segs, _ = model.transcribe(str(path), language="ml", task=task, vad_filter=True, beam_size=5,
                               condition_on_previous_text=False, initial_prompt=PROMPT if task == "transcribe" else None)
    return " ".join(s.text.strip() for s in segs).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips_dir")
    ap.add_argument("--model", default="large-v3")
    a = ap.parse_args()
    d = Path(a.clips_dir)
    w = d / "whisper"
    w.mkdir(exist_ok=True)
    from faster_whisper import WhisperModel
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    for clip in sorted(d.glob("clip*.mp4")):
        out = w / f"{clip.stem}.json"
        if out.exists():
            continue
        res = {"ml": run(model, clip, "transcribe"), "en": run(model, clip, "translate")}
        out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(clip.stem, "done", flush=True)
    update_md(d, w)


def esc(t):
    return t.replace("|", "/").replace("\n", " ")


def update_md(d, w):
    md = d / "CLIPS.md"
    lines = md.read_text(encoding="utf-8").splitlines()
    out = []
    for ln in lines:
        if not ln.startswith("|"):
            out.append(ln)
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        # old layout: 6 cells; new layout: 8 cells
        if cells[0] == "Clip":
            if len(cells) == 6:
                cells = cells[:5] + ["Whisper (rough, ml)", "Whisper English gist"] + cells[5:]
        elif set(cells[0]) <= {"-"}:
            if len(cells) == 6:
                cells = cells[:5] + ["---", "---"] + cells[5:]
        elif re.fullmatch(r"clip\d+", cells[0]):
            f = w / f"{cells[0]}.json"
            if f.exists() and len(cells) == 6:
                r = json.loads(f.read_text(encoding="utf-8"))
                cells = cells[:5] + [esc(r["ml"]), esc(r["en"])] + cells[5:]
        out.append("| " + " | ".join(cells) + " |")
    md.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("CLIPS.md updated")


if __name__ == "__main__":
    main()
