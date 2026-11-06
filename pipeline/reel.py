"""The Project Shop reel pipeline.

Usage (from anywhere):
  pipeline\.venv\Scripts\python.exe pipeline\reel.py transcribe <video> [--lang en|ml|hi] [--model small]
  pipeline\.venv\Scripts\python.exe pipeline\reel.py render <video> [--start S --end S] [--logo logo.png] [--no-captions]

transcribe -> writes <video>_transcript.txt and <video>.srt next to the video (edit the .srt to fix words).
render     -> writes <video>_reel.mp4: 1080x1920, loudness-normalised, burned-in captions, optional logo.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"


def transcribe(video, lang, model_name):
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segs, info = model.transcribe(str(video), language=lang, vad_filter=True)
    print(f"language={info.language} p={info.language_probability:.2f}")
    srt, txt = [], []
    for i, s in enumerate(segs, 1):
        srt.append(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n")
        txt.append(f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}")
    video.with_suffix(".srt").write_text("\n".join(srt), encoding="utf-8")
    Path(str(video.with_suffix("")) + "_transcript.txt").write_text("\n".join(txt), encoding="utf-8")
    print("\n".join(txt))


def render(video, start, end, logo, captions):
    out = video.with_name(video.stem + "_reel.mp4")
    srt = video.with_suffix(".srt")
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    if end is not None:
        cmd += ["-to", str(end)]
    cmd += ["-i", video.name]
    if logo:
        shutil.copy(logo, video.parent / "_logo.png")
        cmd += ["-i", "_logo.png"]
    if captions and srt.exists():
        vf += (",subtitles=" + srt.name + ":force_style='FontName=Arial,Bold=1,FontSize=14,"
               "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Alignment=2,MarginV=260'")
    if logo:
        fc = f"[0:v]{vf}[v];[1:v]scale=220:-1[l];[v][l]overlay=W-w-40:60[o]"
        cmd += ["-filter_complex", fc, "-map", "[o]", "-map", "0:a"]
    else:
        cmd += ["-vf", vf]
    cmd += ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-preset", "medium",
            "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart", out.name]
    subprocess.run(cmd, check=True, cwd=video.parent)
    if logo:
        (video.parent / "_logo.png").unlink(missing_ok=True)
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["transcribe", "render"])
    ap.add_argument("video")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--model", default="small")
    ap.add_argument("--start", type=float)
    ap.add_argument("--end", type=float)
    ap.add_argument("--logo")
    ap.add_argument("--no-captions", action="store_true")
    a = ap.parse_args()
    v = Path(a.video).resolve()
    if a.cmd == "transcribe":
        transcribe(v, a.lang, a.model)
    else:
        render(v, a.start, a.end, a.logo, not a.no_captions)
