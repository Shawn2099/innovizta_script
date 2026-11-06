# competitor_reels: study data (do not repost)
Downloaded 6 Nov 2026 with yt-dlp, from public reels, for analysis only.

| Path | What |
|---|---|
| `idukki/`, `febtech/`, `flemin/`, `bbx/` | The reels (`<shortcode>.mp4`), plus rough transcripts `*_transcript.txt` / `.srt` from Whisper (base model, **unreliable for Malayalam**, only used to tell speech from music) |
| `manifest.csv` | account, shortcode, views (at download time), tier (top / mid / low) |
| `captions.txt` | account\|code\|views\|tier\|caption (first 400 chars) |
| `_breakdown/<account>_<code>/` | `hook.jpg` (first 3 s, 12 frames), `sheet.jpg` (12 frames across the reel), `metrics.json` |
| `_breakdown/summary.csv` | All metrics in one table (cuts = hard scene changes only; voiced_ratio = non-silent share, music included) |
| `_breakdown/*_visual.md` | Haiku agents' per-reel visual notes + patterns |
| `_breakdown/speech_lang.txt` | Detected language per reel (speech check) |

The conclusions are in `../REEL_FORMULA.md`.
