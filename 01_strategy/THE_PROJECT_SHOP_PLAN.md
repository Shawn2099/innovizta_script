# The Project Shop: Company Notes and Instagram Plan

Last updated: 2026-11-04. Living document: update it as answers and results come in.

## 1. Company facts (from the founders)
- **Brand:** The Project Shop (new). Sister company: Innovizta Technologies.
- **Founders:** KTU B.Tech grads, now doing M.Tech. Also running Innovizta Technologies.
- **Vision:** Become the best project-assistance company in India.
- **Origin:** Founders identified bottlenecks students face, fine-tuned an approach, and are now building tools for students.
- **Tools planned:** diagrams, datapoints, research paper presentation and writing, documentation.

### Offer / student journey
1. **Free consultation** (free initially).
2. Discuss the student's idea, give inputs, shape it into a better project/product, and link it to their career path so it is more relevant.
3. Start the project with the student and **teach them what was done**.
4. **Internship opportunity** on their own project, or on active projects at The Project Shop or Innovizta Technologies.

### Services and pricing
| Service | Price |
|---|---|
| Consultation | Free (initially) |
| PCB for all circuits | Free |
| 3D printing | At cost |
| Diagrams, table data, datasets, circuit diagrams | Provided (pricing TBD) |

### Current assets
- Many students already served, **but no testimonials yet** (top priority to collect).
- Office with a Creality 3D printer (good B-roll for Reels).
- Can film as many Reels as needed, **provided there is a script**.
- First clip: `DAY1/day1.mp4` (90 s, portrait, founder to camera, quiet audio).

## 2. Audience and goals
- **Audience:** B.Tech final years and M.Tech students.
- **3-month goals (all):** leads/clients, followers and brand, promoting student tools, trust and credibility.
- **Style:** founders face to camera.
- **Language:** Manglish / mixed.

## 3. Positioning and ethics (our moat)
- Line: **"We teach, guide and build with you. You own your work."**
- State plainly in bio and pinned post: no ghostwriting, no readymade submissions, no plagiarism, no fabricated data.
- Keep wording in Reels as "build together, we teach you", not "we do your project for you". This protects against college complaints, spam reports and reputation harm.
- Verify before promoting: that "free PCB for all circuits" and the internship offer have clear limits, terms and capacity.

## 4. Instagram plan
Evidence is from marketing blogs, so treat numbers as hypotheses and verify in Insights.

- **Timing:** Nov-Dec: review/synopsis survival. Feb-Apr: report and PPT. Apr-May: viva prep. Jun-Aug: topic selection.
- **Cadence:** 4-5 Reels/week, 1 carousel/week, 2-3 Stories/day.
- **Length:** 15-30 s relatable/teaser, 30-60 s tutorials. Hook in first 1.5 s, burned-in captions.
- **Test posting slots:** morning (7-9), lunch (12-1:30), night (9 pm) for 2 weeks. Compare watch time, shares, saves.
- **SEO:** name field e.g. "The Project Shop | Engineering Project Help". Keywords in bio, captions, on-screen text and speech. Few precise hashtags (#finalyearproject #ktu #ieeepaper #engineeringstudents) plus one branded tag.
- **Bio structure:** what we do, for whom, proof, call to action. Link to WhatsApp or Linktree.
- **Highlights:** Start Here, Services, Results/Reviews, Free Tools, FAQs, Viva Prep.
- **Lead funnel:** "Comment KEYWORD for the free checklist" (official Instagram tools only), WhatsApp Business with quick replies and labels, free consult then project. Track leads by Reel in a Google Sheet.

### Content pillars
Project mentoring, research writing, diagrams and data, viva and presentation, student tools, behind the scenes (founders and lab).

### Reel ideas (first batch)
1. Founder story: KTU B.Tech grads, now M.Tech, and why we started The Project Shop.
2. "Free PCB for your circuit": show the process (strong, concrete offer).
3. 3D printing at cost: print timelapse on the Creality.
4. Messy block diagram turned into a clean one (before and after).
5. "3 red flags in your abstract."
6. How we shape a project idea to fit your career path.
7. Viva questions in 30 s quick-fire.
8. How a student got an internship on their own project (needs permission).
9. Dataset to graph, step by step.
10. PPT makeover: boring slide versus slide that sells.

## 5. Tooling status
- **Installed:** marketingskills plugin (`marketing-skills@marketingskills`): hooks, captions, social copy.
- **FFmpeg:** installed locally, used for editing.
- **KinoCut MCP:** installed (user scope, pinned `kinocut==1.16.5`). Takes effect in a new session.
- **Instagram agent skill:** installed project-locally from `Jakeschincariol/instagram-agent-skill` (MIT). 13 skills in `.opencode/skills/ig-*` and matching `/ig-*` commands in `.opencode/commands/`. Brand config in `instagram/voice.md` (prefilled from this plan; handle, keyword CTA and link still TODO). It only drafts; it never posts. Python tools patched for Windows (`python` not `python3`, UTF-8 output, BOM-safe input); all six smoke-tested.
- **Reusable reel pipeline:** `The project shop/pipeline/` with `reel.py` and a venv containing faster-whisper.
  - `pipeline\.venv\Scripts\python.exe pipeline\reel.py transcribe <video> [--lang en|ml|hi]` writes `.srt` and a transcript. Edit the `.srt` to fix words.
  - `pipeline\.venv\Scripts\python.exe pipeline\reel.py render <video> [--start S --end S] [--logo logo.png]` writes `<video>_reel.mp4` (1080x1920, loudness normalised, burned-in captions, optional logo).
  - Whisper "small" mis-hears Manglish: always review the `.srt` before rendering.
- **Avoid:** MomoFadaly/video-edit, kush36agrawal/video_editor_mcp, any skill asking for an API token pasted in the terminal.
- **Maybe later:** tenfoldmarc/video-edit-skill for talking-head reels, only after reading its scripts.

## 6. Open items
- [ ] Instagram handle, logo, brand colours
- [ ] Fill the remaining `instagram/voice.md` TODOs (handle, keyword CTA, link, pace) and add two more reference reels
- [ ] Transcript or script of `day1.mp4` (what is said, what the hook is)
- [ ] Collect testimonials from past students (with permission)
- [ ] Define limits and terms for free PCB, internship and pricing for diagrams/datasets
- [ ] Which tool to build and launch first
- [ ] Names and roles of founders on camera
- [ ] Edit Reel 1 from `day1.mp4`

## 7. Engagement research (2026-11-04; blog-based, test in Insights)
**Checklist:** hook in 1 s (face plus same line as big text, no "Hi guys"); 20-35 s for most Reels (45-60 s only for stories/tutorials); visual change every 2-3 s (punch-in 110-125%, B-roll, text pop); big 2-4 word Manglish captions in English letters with key word highlighted; low music plus whoosh/ding SFX; re-hook at ~40%; last line loops to first; one CTA (send/comment); check retention curve after each post.

**Formats:** (1) Free offer "PCB for Rs 0" (2) 3D print timelapse (3) Student mistakes (4) Day N of building (series, recurring title card) (5) Soldering close-up + voiceover (6) Myth vs reality (7) Project idea drop (8) Student question answered.

**Tips:** film twice from two angles and alternate for free cuts; same title card on every Reel; post 3-4/week; test Manglish vs English hook text.

## 8. Audio and assets (verify licences yourself)
- Business accounts: use Meta Sound Collection inside the Instagram app, or audio you hold a licence for. Volume does not make unlicensed music safe.
- SFX/music sources: Pixabay, Mixkit (commercial OK, no credit); Freesound CC0 only. Do not use YouTube Audio Library on Instagram unless checked. Save each licence page.
- Fonts: Google Fonts (Montserrat, Poppins, Anton, Bebas Neue). Footage: Pexels, Pixabay, Mixkit.

## 9. Candidate tooling (not yet installed; check licence/commits first)
auto-editor (silence cut), faster-whisper (installed) + pysubs2 ASS animated captions or pycaps, FFmpeg for zooms/SFX mix/progress bar, MoviePy (MIT), HyperFrames (Apache-2.0, needs Node, read code first). Do not use tenfoldmarc/video-edit-skill (no licence) or give any tool an Apify/API token.

## 10. Reel pipeline v2 (no captions)
- Installed in `pipeline/.venv`: faster-whisper, auto-editor, pysubs2, pillow, numpy. Whisper large-v3 transcribes Manglish better but still mishears and loops: do NOT burn auto-captions without human review.
- `pipeline/build_reel.py <cut.mp4> <out.mp4> "HOOK 1" "HOOK 2" <logo>`: punch-in zoom every 3 s, synthesized whoosh/impact SFX (no licensing issues), white-flash open, pop-in hook text, top progress bar, logo, end card, loudness normalisation.
- Logos: `logo_transparent.png` (white removed), `logo_outlined.png` (thin white outline so dark text stays readable on video).
- Day 1 output: `day1_reel_v3.mp4` (hook "ARE YOU A KTU STUDENT?"). Music is added in the Instagram app (business-account licensing).

## 11. Pipeline saved (2026-11-04)
Full instructions: `The project shop/pipeline/README.md`. Day 1 final: `day1_reel_v5.mp4` (recipe in `pipeline/run_day1.sh`).
Style rules: few transitions, no whoosh per cut, hook text top / key text low, loop-friendly ending, music added in Instagram.
