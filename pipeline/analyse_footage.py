"""Analyse a shoot folder once and cache everything next to the footage (no re-runs, no tokens).

Usage:
  pipeline\.venv\Scripts\python.exe -I -X utf8 pipeline\analyse_footage.py vidoes\<shoot date> [--model large-v3] [--no-whisper] [--force]

For every video (mp4/mov/m4v) in the folder it writes to <folder>/_analysis/:
  <stem>.jpg   contact sheet (1 frame/s, rotation honoured, up to 10 frames)
  <stem>.json  duration, resolution, rotation, rough Whisper: ml transcript + English gist, with segment times
  FOOTAGE.md   index table of all clips (rebuilt every run; cached clips are not re-processed)

Script-first rule: if the folder has a non-empty improv_script.md (Shawn's own words, "clip N: ..."),
Whisper is SKIPPED (the script is the truth) and its lines go into FOOTAGE.md. With no script, Whisper
runs automatically. --whisper forces it anyway (e.g. to cross-check the script).

Whisper output is a ROUGH LOCATOR ONLY: Manglish is misheard. Never burn it as captions; the user's
"As said" notes in the script (D4c) are the truth. Runs locally on CPU: no API cost.
"""
import argparse
import json
import subprocess
from pathlib import Path

EXTS = {".mp4", ".mov", ".m4v"}
PROMPT = ("Casual Malayalam-English (Manglish) talk by an engineering startup founder about B.Tech "
          "final year projects, KTU, project mentoring, The Project Shop.")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "format=duration:stream=width,height:stream_side_data=rotation", "-of", "json",
                          str(path)], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    st = j["streams"][0]
    rot = 0
    for sd in st.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    w, h = st["width"], st["height"]
    if abs(rot) == 90:
        w, h = h, w
    return {"duration": round(float(j["format"]["duration"]), 2), "width": w, "height": h, "rotation": rot}


def contact_sheet(path, out_jpg):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf",
                    "fps=1,scale=360:-1,tile=5x2", "-frames:v", "1", str(out_jpg)], check=True)


def whisper(model, path):
    res = {}
    for task, key in (("transcribe", "ml"), ("translate", "en")):
        segs, _ = model.transcribe(str(path), language="ml", task=task, beam_size=5, vad_filter=False,
                                   condition_on_previous_text=False,
                                   initial_prompt=PROMPT if task == "transcribe" else None)
        res[key] = [{"start": round(s.start, 1), "end": round(s.end, 1), "text": s.text.strip()} for s in segs]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--no-whisper", action="store_true")
    ap.add_argument("--whisper", action="store_true", help="run Whisper even when improv_script.md exists")
    ap.add_argument("--force", action="store_true", help="re-process clips that are already cached")
    a = ap.parse_args()
    d = Path(a.folder)
    out = d / "_analysis"
    out.mkdir(exist_ok=True)
    clips = sorted(p for p in d.iterdir() if p.suffix.lower() in EXTS and not p.stem.endswith("_final"))
    script = d / "improv_script.md"
    lines = {}
    if script.exists() and script.read_text(encoding="utf-8").strip():
        import re
        for m in re.finditer(r"clip\s*(\d+)\s*:\s*(.+?)(?=\n\s*\**\s*clip\s*\d+\s*:|\Z)",
                             script.read_text(encoding="utf-8"), re.I | re.S):
            lines[int(m.group(1))] = " ".join(m.group(2).replace("*", "").split())
        if not a.whisper:
            a.no_whisper = True
            print(f"improv_script.md found ({len(lines)} clips): Whisper skipped")
    model = None
    for clip in clips:
        js = out / f"{clip.stem}.json"
        info = json.loads(js.read_text(encoding="utf-8")) if js.exists() and not a.force else {}
        if not info:
            info = {"file": clip.name, **probe(clip)}
        jpg = out / f"{clip.stem}.jpg"
        if a.force or not jpg.exists():
            contact_sheet(clip, jpg)
        if not a.no_whisper and "whisper" not in info:
            if model is None:
                from faster_whisper import WhisperModel
                model = WhisperModel(a.model, device="cpu", compute_type="int8")
            info["whisper"] = whisper(model, clip)
        js.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"done {clip.name}", flush=True)

    rows = ["# Footage index (auto, rough)", "",
            "Whisper is a rough locator only (Manglish is misheard). Fill the real words in the script's D4c.", "",
            "| # | Clip | Dur (s) | Size | Improv script (truth) | Whisper ml (rough) | English gist (rough) | Sheet |",
            "|---|---|---|---|---|---|---|---|"]
    for n, clip in enumerate(clips, 1):
        info = json.loads((out / f"{clip.stem}.json").read_text(encoding="utf-8"))
        w = info.get("whisper", {})
        ml = " / ".join(s["text"] for s in w.get("ml", [])).replace("|", "/")
        en = " / ".join(s["text"] for s in w.get("en", [])).replace("|", "/")
        rows.append(f"| {n} | {clip.name} | {info['duration']} | {info['width']}x{info['height']} | {lines.get(n, '')} | {ml} | {en} | "
                    f"[sheet]({clip.stem}.jpg) |")
    (out / "FOOTAGE.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"index: {out / 'FOOTAGE.md'}")


if __name__ == "__main__":
    main()
