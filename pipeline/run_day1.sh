#!/bin/bash
# Exact recipe used for Day 1 (run from the project shop folder, Git Bash).
# Source clip: vidoes/DAY1/day1.mp4. Chosen take starts at 26.2 s (skip "Hi guys") and ends at 86.25 s.
set -e
cd "$(dirname "$0")/../vidoes/DAY1"
PY=../../pipeline/.venv/Scripts/python.exe
ffmpeg -y -ss 26.2 -to 86.25 -i day1.mp4 -c:v libx264 -crf 14 -preset fast -c:a aac -b:a 192k cut.mp4
$PY -I ../../pipeline/clean_cut.py cut.mp4 cut_clean.mp4
$PY -I ../../pipeline/build_reel.py cut_clean.mp4 day1_reel_v5.mp4 "ARE YOU A" "KTU STUDENT?" logo_outlined.png --no-end \
 --text "42.2|45.0|INDIA’S BEST PROJECT|76|white|1290" --text "42.2|45.0|ASSISTANCE COMPANY|78|orange|1380" \
 --text "56.4|59.9|WELCOME TO DAY 1|92|white|1230" --text "56.4|59.9|OF BUILDING THE BEST|76|orange|1335" \
 --text "56.4|59.9|PROJECT ASSISTANCE COMPANY|58|white|1425"
