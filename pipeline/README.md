# The Project Shop: Reel Pipeline

Turns a raw talking-head clip into an Instagram Reel (1080x1920): hook text from frame 1 (flash is opt-in via `--flash`), slow smooth push-in,
timed text overlays, soft pop sound effects, top progress bar, outlined logo, loop-friendly ending. No auto-captions
(Whisper mishears Manglish: never burn captions without human review).

## One-time setup (already done on this PC)
- FFmpeg on PATH. Python venv in `pipeline/.venv` (recreate: `uv venv --python 3.11 .venv` then
  `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`).
- Logos: `vidoes/DAY1/logo.png` (original), `logo_transparent.png` (white removed), `logo_outlined.png` (use this one:
  thin white outline keeps dark text readable on video). Copy them into each new day's folder.

## New day, step by step (replace DAYN, times in seconds)
1. Put the clip in `vidoes/DAYN/`. Find where the good take starts/ends (play it, or `reel.py transcribe` for rough timing).
2. Cut the take (re-encode, never stream-copy):
   `ffmpeg -ss START -to END -i dayN.mp4 -c:v libx264 -crf 14 -preset fast -c:a aac -b:a 192k cut.mp4`
3. Remove long silences (plain FFmpeg, no black frames): `python clean_cut.py cut.mp4 cut_clean.mp4 --map t1,t2`
   (`--map` prints where input times land in the output, so overlay times stay correct).
4. Build: `python build_reel.py cut_clean.mp4 dayN_reel.mp4 "HOOK LINE 1" "HOOK LINE 2" logo_outlined.png --no-end --text "start|end|TEXT|size|white-or-orange|y" ...`
   Options: `--punches 20-23` for an optional eased zoom, `--push 0.06` slow zoom, `--hook-end 3.0`, drop `--no-end` for a branded end card.
   See `run_day1.sh` for a complete example.
5. Check: no black frames (YAVG scan), play through once with sound, check text timing and the loop point.

Run Python as `.venv/Scripts/python.exe -I script.py ...`.

## Scripts
- `build_reel.py`: main builder (hook, zoom, text overlays, SFX, progress bar, logo, loop fade or end card).
- `clean_cut.py`: silence removal and time mapping.
- `reel.py transcribe <video> [--lang en]`: rough SRT/transcript (reference only). `words.py` gives word timestamps (large-v3).
- `run_day1.sh`: exact Day 1 recipe.

## Style rules learned on Day 1
- Few transitions: no zoom jumps, no whoosh on every cut (it felt dizzying). Text and soft pops only on key lines.
- Hook = one big question in the first 3 s, in sync with the spoken line. Keep text away from the face (hook at top, key text low).
- Auto-editor leaves single black frames at joins: do not use it for cutting.
- Loop: start and end on a similar pose, brief white fade at the end, no dead-stop end card.
- Music: add inside Instagram (business-account licensing). SFX are synthesized in code, so there are no licence issues.

## Shared assets
- pipeline/assets/ holds the logos (logo.png, logo_transparent.png, logo_outlined.png). Use them from any day folder instead of copying.
- Reels made from mixed Day 2/3 footage go in vidoes/reels/ (see vidoes/_analysis/ for per-clip notes).

## build_reel.py flags (updated 6 Nov 2026, matches 04_reel_production/REEL_SCRIPT_TEMPLATE.md)
- `--flash` opt-in white flash (default OFF: hook visible from frame 1)
- `--hook-y 300` hook line 1 position (line 2 at +160); warns if outside the safe zone (>270 px top, >670 px bottom)
- `--push 0` for continuous "hold" shots; `--punches s-e,...` + `--punch 0.15` for punch-ins
- `--end1/--end2/--end3` end-card text (defaults: The Project Shop / Learn it. Build it. Own it. / Follow for more), `--no-end` for loop reels
- Recommended: `build_reel.py <cut> <out> "<HOOK 1>" "<HOOK 2>" pipeline/assets/logo_transparent.png --hook-y 300 --push 0`

## reel_assemble.py: one-step renderer (YAML editor block + raw clips -> finished Reel)
`pipeline/.venv/Scripts/python.exe -I pipeline/reel_assemble.py <script.md|script.yaml> [--source-dir DIR] [--out OUT.mp4] [--preview] [--keep-work]`
- A `.md` script: the fenced ```yaml block containing `beats:` is used. `--preview` = fast 540x960 render.
- Output `<source_dir>/<id>_final.mp4` (H.264 1080x1920 30 fps, AAC, -14 LUFS / -1 dBTP), plus `<id>_qc.txt` (duration vs target, per-beat durations, warnings, loudness, frame brightness) and `<id>_qc_t0.0/t1.0/mid/end.jpg`. Temp files go to the system temp dir.
- Clips (Read Mode): `file` is a stem; picks `<stem>_KEEP.*`, else the highest `<stem>_t<N>.*`, else `<stem>.*` (mp4/mov/m4v). Portrait iPhone .MOV rotation is honoured; everything is cover-cropped to 1080x1920.
- `in/out: auto` trims leading/trailing silence (-35 dB, 0.15 s handles); numbers = seconds. Internal silences >0.6 s are jump-cut (0.15 s handles kept) unless `jumpcut: false`.
- All times in `text`, `punches`, `inserts` are seconds from the beat start, measured after jump cuts and speed.

```yaml
id: LAUNCH1
length_s: 45                # target; warns if the result differs by >2 s
source_dir: vidoes/2026-11-10/  # relative to the project root
beats:
  - id: B1
    clip: {file: LAUNCH1_B1, in: auto, out: auto, crop: 100, speed: 1.0, jumpcut: true}
    transition_in: TRN-CUT  # TRN-CUT|PUNCH|WHIP|ZOOMIN|FLASH|SPEED (JL/MATCH/NONE = cut); unknown -> warn + cut
    text: [{style: TXT-HOOK, words: "30 TEAMS. SAME 3 PROBLEMS.", in: 0.0, out: 3.0}]   # list or single dict
    overlays: [{type: OVL-PILL, words: "1/3 TOPIC"}]   # OVL-PILL, OVL-COUNT; others warn + skip
    punches: [[1.2, 2.0]]   # hard punch to punch_crop inside these windows
    punch_crop: 118
    sfx: SND-HIT            # SND-HIT|SND-WHOOSH|SND-POP|none (default: whoosh for WHIP/ZOOMIN, hit for FLASH)
    inserts: [{file: LAUNCH1_INS_board, at: 2.0, dur: 2.0}]  # B-roll over the picture, A-roll audio continues
music: {file: null, level_lufs: -26, duck_db: 4}   # file relative to source_dir/project root; looped, ducked under voice
end_card: {show: true, line1: "The Project Shop", line2: "Learn it. Build it. Own it.", line3: "Follow for more"}
export: {lufs: -14, fps: 30}
```
- Text styles (hand-written only): TXT-HOOK (96 px caps, y 330), TXT-KEY (76 px, y 1000), TXT-LABEL (54 px on dark box, y 1150), TXT-CTA (88 px, y 1050). Orange is explicit only: add `highlight: "WORD"` (or a list) to a text item, or wrap words in `*stars*`; with no marker HOOK/KEY are all white. TXT-CTA keeps the "quoted" keyword orange. `
` = two lines. Text auto-shrinks (then wraps, with a warning) to stay inside x 60..920 (centred, so max width 760 px) and y 270..1250. A hook shares the beat with OVL-PILL: it moves down 60 px.
- Text position (any style): `y: 1000` = top of the text block in px, or `pos: top|upper|mid` (top = style default, upper = 1180, mid = 900; presets are lifted to stay above y 1250). With neither, face avoidance runs: OpenCV Haar frontal-face detection on the beat's first frame (after crop/scale to 1080x1920); if the text box is within 40 px of the face it moves below the face (else to `upper`) and the QC notes say so. Needs `opencv-python-headless<5` in the venv (v5 dropped CascadeClassifier); skipped with a note if missing.
- Logo: stays top-left (x 60..230, y 275..445). It is hidden automatically only while an OVL-PILL or text item overlaps that box, so it never collides; the QC notes list the hidden windows.
- Transitions: WHIP = xfade slideleft 0.15 s, ZOOMIN = xfade zoomin 0.3 s (both overlap, so total is shorter), FLASH = 0.1 s white flash (ignored on beat 1, warns if used twice), PUNCH = whole beat at punch_crop, SPEED uses clip `speed`.
- Fixed elements: logo top-left (60 % opacity), orange progress bar, 2 s end card, synthesized SFX (build_reel.py).
- QC flags: beats >8 s with no punch/insert/text change (warning), >4 s (note), SFX closer than 3 s, word-count limits, missing clips.
- Limitations: no TRN-FREEZE, OVL-ARROW/CIRCLE/PIP/SPLIT/EVIDENCE/BLUR, TXT-CARD; ducking amount is approximate; fps fixed at 30.

### Text engine (libass, default since 6 Nov 2026)
- `export: {text_engine: ass|drawtext}` or CLI `--text-engine drawtext` (legacy Arial drawtext look, kept as fallback). Default `ass`.
- ASS look: Anton caps (HOOK 122 px, KEY 100, CTA 112), thick black outline (6-7 px) + soft shadow, 2-4 words per line (auto-wrap, balanced), word-by-word pop (115% -> 100% in 120 ms, 90-100 ms stagger, slide-up 26 px + fade in, 150 ms fade out). The hook's first word is visible at frame 1. TXT-LABEL = Montserrat ExtraBold caps, lower third, slides in from the left, no pop. OVL-PILL uses Montserrat ExtraBold.
- Emphasis: wrap words in `*stars*` inside `words:` (e.g. `"THE *HARD PART.*"`) -> black text on a rounded orange box (consecutive starred words share one box). `highlight:` lists and the TXT-CTA "quoted" keyword work the same way. In TXT-LABEL emphasised words turn orange instead of boxed.
- Safe zones, face avoidance, `pos:`/`y:`, logo hiding and QC notes behave as before. Times are beat-local (each beat is rendered as its own segment), so trims/speed/transitions need no offset maths.
- Implementation: per-beat `txt_<n>.ass` in the work dir + `ass=filename=...:fontsdir=fonts` (fonts from `assets/fonts` are copied into the work dir; relative paths avoid Windows drive-colon escaping). libass `s` is calibrated per font (`fsk` in `ASTYLES`).

## Zoom (clip `crop`, `punch_crop`)
- Zoom is cut from the **source resolution** (4K footage stays sharp up to ~170 %), anchored `ZOOM_Y = 0.15` from the top so a waist-up subject's head stays in frame.
- House values: MS 100 · MCU 125 · CU 150 · punch = base + 20. Set `punch_crop` explicitly on every `TRN-PUNCH` beat (the default 118 is below the MCU base, so no zoom would show).
