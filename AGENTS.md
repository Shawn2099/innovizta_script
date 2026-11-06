# AGENTS.md: The Project Shop marketing workspace
**Read this first, every session.** It gives any agent (Claude Code, OpenCode, others) the full context and tells you what to do.
Last updated: 6 Nov 2026.

## 1. Who / what
- **The Project Shop** (theprojectshop.online): Kerala company giving **final-year project mentoring** to KTU B.Tech/M.Tech teams (CS, EC, EEE, robotics; software, IoT, hardware + simulation; no civil/heavy mechanical). Also kits, components, **3D printing at cost (PLA ₹5/g, PETG ₹8/g)**, PCB, and student tools in development (diagram/report automation).
- **Offer:** free 1-hour Google Meet consult per team → project from ₹15K (typically ~₹25K) incl. circuit diagram, data points and a class teaching the team their project → internship on their own project (small fee). **Referral:** internship free + ₹1K off per referred team.
- **People:** founders are KTU B.Tech grads, now M.Tech students. **Shawn is the only one on camera.** Sister brands: Clueless Engineer (Shawn's BTS/vlog page, ~100 followers, collab only on relevant reels) · Innovizta Technologies (separate B2B; its builds may appear as "projects our interns work on").
- **Situation (Nov 2026):** 80 student teams helped last season (word of mouth, now exhausted; corrected from 30 by the user, 6 Nov), 0 this season so far (5 this calendar year). Instagram account **not yet created**. Website is a "coming soon" page. Capacity 10–30 teams/month. Promotion budget ≤ ₹3K/month.
- **Goal:** best project-mentoring company in India → **own KTU/Kerala first in Manglish** (Kottayam, Ernakulam, Karunagappally/Kollam), English/national from ~Sep 2027. Finish line 30 Apr 2027: ~16 paid teams, 20+ Google reviews, a July waitlist.

## 2. Hard rules (never break)
1. **Positioning:** "Engineering projects: learn it, build it, own it." Project help = **mentoring, we build it WITH you**. Never "readymade", "we do your project", "submit-ready". (College clubs treat "project assistance" as taboo, and Meta bans ads that enable cheating.)
2. **Honesty:** no fake clients, reviews, numbers, urgency or testimonials. Demo builds are labelled as demos. Client work is shown only with written permission. Every factual claim in a script goes in its fact sheet.
3. **No auto-captions / subtitles.** Manglish breaks Whisper. Use hand-typed hook and key-line text only. Transcripts are rough reference, never truth.
4. **Original content only.** Never repost competitor footage (the downloaded reels are for study only). No Malayalam film clips or film audio. Licensed or our own audio only.
5. **Max 5 hashtags.** Keyword-rich caption line 1. Location tag.
6. **Avoid:** caste, religion, party politics, naming colleges/teachers/competitors, sexist slang.
7. **No IEDC/IEEE/club route** (they refuse). Reach students directly (own events, free tools, individual ambassadors/creators, paid student pages, careful ads, search visibility).
8. **Model split for subagents:** Haiku for small/mechanical work (classifying footage, extraction), Sonnet for research and code, Opus/main session for strategy, synthesis and scripts. Use subagents when asked and run them in parallel.
9. **Scripts start in plain English (template D0):** the meaning + simple acting notes per beat. Manglish lines are suggestions only; Shawn says it in his own natural Manglish (AI-written Malayalam reads unnaturally). Every script opens with **SETUP AT A GLANCE** (where Shawn stands/sits, camera, top-view sketch, props + the beat each is used in, close-ups at the end). Shawn is framed head-to-waist in 4K and never moves; close-ups are editor zoom.
10. Don't install third-party skills/repos yourself: give the user the command. Ask before code changes beyond the requested scope. **Posting is manual**: the user watches and posts.

## 3. Where everything is
| Path | What |
|---|---|
| `00_PLAN_INDEX.md` | Master index: decisions, 15 workstreams (status / to-do / to-research), open questions |
| `README.md` | Folder map + naming conventions |
| `01_strategy/6_MONTH_PLAN.md` | **Master plan** (wins any conflict): finish line, flywheel, KTU calendar, monthly targets + exit checks |
| `01_strategy/SOCIAL_MEDIA_MASTER_PLAN.md` · `THE_PROJECT_SHOP_PLAN.md` | Strategy · original founder notes |
| `02_growth_and_visibility/` | Local growth (realism, colleges, ambassadors, ads) · visibility (Google profile, website, IG search, direct reach) |
| `03_competitor_research/REEL_FORMULA.md` | Cracked formula: 9 rules + validation v2 on big pages + new patterns |
| `03_competitor_research/research/` | Books/frameworks, skills playbook, India/Kerala audience, trends, comment language bank |
| `03_competitor_research/competitor_reels/` | Study data (videos, captions, breakdowns). **Study only** |
| `04_reel_production/SCRIPT_PLAYBOOK.md` | **How to write a reel:** 15 laws, 8-step procedure, hook templates + 12-point hook score, QA/ethics gates |
| `04_reel_production/REEL_SCRIPT_TEMPLATE.md` | **The script sheet + all production codes** (sets, camera, posture, text, transitions, clip durations, overlays, cover, Read Mode, shoot card, publishing pack, YAML) |
| `04_reel_production/CONTENT_CALENDAR.md` | **Dated plan + status: the source of truth for "today"** |
| `04_reel_production/scripts/` | One file per reel (`<post date>_<REEL NAME>_<topic>.md`, e.g. `2026-11-16_LAUNCH1_why-we-started.md`) |
| `04_reel_production/series/` | Series details (Opportunity Drop) |
| `pipeline/` | Tools: `build_reel.py` (single-clip reel builder), `reel_assemble.py` (YAML → final reel, one step), `reel_breakdown.py` (contact sheets + metrics), `analyse_footage.py` (run once per shoot folder: cached sheets + rough transcript in `<folder>/_analysis/`), `reel.py`, `clean_cut.py` … Run with `pipeline/.venv/Scripts/python.exe` |
| `vidoes/` | Our raw footage (typo'd name kept). New shoots: `vidoes/<shoot date YYYY-MM-DD>/` |
| `instagram/` | Brand voice for the OpenCode `ig-*` skills (don't move) |
| `05_founder_inputs/` | Handwritten founder notes |

## 4. "What's today's content?": do this
1. Get today's date. Open `04_reel_production/CONTENT_CALENDAR.md` and find today's row and this week's rows.
2. Check `01_strategy/6_MONTH_PLAN.md` for the **month theme, main CTA and KTU moment** (e.g. Phase II starts ~1 Dec, Review 1 ~18–23 Jan, final evaluation 17–26 Mar, viva ~20 Apr).
3. Check status:
   - **Post day:** is the script in `scripts/` edited and QC'd? If yes, give the user the publishing pack (caption, hashtags, pinned comment, story plan, prepared replies). If not, say what's missing.
   - **Shoot day:** give Shawn the shoot card + Read Mode lines for every reel being shot, plus the props/setup checklist.
   - **Script missing:** write it now. Follow `SCRIPT_PLAYBOOK.md` §3 (brief → format → 8 hooks scored → beats → length → read-mode lines → gates) and fill **every** block of `REEL_SCRIPT_TEMPLATE.md` Part D. Save to `scripts/<post date>_<REEL NAME>_<topic>.md` and update the calendar status.
   - **Edit day:** if raw files are in `vidoes/<shoot date>/`, run `reel_assemble.py` on the script, read the QC report + frames, fix and re-render, then hand over for the user to watch.
   - **Setup/admin day:** list the open tasks for the current month from `6_MONTH_PLAN.md` and `00_PLAN_INDEX.md`.
4. Also remind the user of daily habits: 2–3 stories, reply to comments in the first hour, log leads (source = tracking code) in the lead sheet.
5. After any change: update `CONTENT_CALENDAR.md` status, and the relevant workstream in `00_PLAN_INDEX.md`.

## 5. Workflow for one reel (end to end)
Script (playbook + template) → Shawn approves and ticks the fact sheet → **shoot in Read Mode** (teleprompter under the lens, one file per beat: `<REEL NAME>_<beat>_t<n>.mp4`, e.g. `LAUNCH1_B1_t2.mp4`, best take renamed `_KEEP`) → copy to `vidoes/<shoot date YYYY-MM-DD>/` → **footage intake** (below) → **fill D4c "As said"** → `reel_assemble.py scripts/<script file>.md` → QC (template Part G + QC frames) → the user watches and posts manually → fill in D6 results after 48 h → Sunday review.

**Footage intake (every new shoot folder):**
1. If Shawn improvised, he saves `improv_script.md` in the shoot folder (`clip 1: …`, `clip 2: …`; clip N = Nth file in phone-time order).
2. Run `pipeline/.venv/Scripts/python.exe -I -X utf8 pipeline/analyse_footage.py vidoes/<shoot date>`. **Script present → Whisper is skipped** (the script is the truth). **No script → rough Whisper runs automatically** (ml + English gist). Results are cached in `<folder>/_analysis/` (contact sheets, per-clip JSON, `FOOTAGE.md`); never re-run, read the cache.
3. A **Haiku subagent** (`model: "haiku"`) reads `FOOTAGE.md` + contact sheets and returns: clip → beat mapping, English meaning per clip, usable speech in/out times, problems (fluffs, cut-off words, framing/lighting, claims that need the fact sheet or break a hard rule). The main session checks it, asks the user about anything unclear, then renames clips `<REEL>_B<n>_KEEP.mp4` (originals to `originals_phone_names/`) and fills D4c.
4. Without a script, the Whisper text is a draft: the user confirms what was said before D4c is final.

**Edit style:** follow template Part B0 (approved by the user on LAUNCH2, 6 Nov): no punch-zooms, no mid-sentence jump cuts, TRN-FADE between clips, text low on the chest, no progress bar, end card v2. Watch every cut frame by frame before handing it over.

## 6. Current state / next actions (update this list)
- ✅ Research done: competitors, formula (validated on 6 big pages), playbook, template, KTU calendar, visibility plan.
- ✅ `build_reel.py` fixed (no flash by default, safe-zone hook).
- ✅ `reel_assemble.py` (YAML → final reel) built and tested on synthetic clips: take selection, silence trim/jump cuts, portrait .MOV, punches, inserts, TXT-HOOK/KEY/LABEL/CTA, OVL-PILL/COUNT, TRN-CUT/PUNCH/WHIP/ZOOMIN/FLASH/SPEED, SFX, ducked music, -14 LUFS, logo, progress bar, end card, QC report + frames, `--preview`. **Not yet supported:** TRN-FREEZE, OVL-ARROW/CIRCLE/PIP/SPLIT/EVIDENCE/BLUR, TXT-CARD (warns and skips). Not yet tested on real phone footage. Do the test shoot first.
- ✅ LAUNCH1 shot early (6 Nov, improv, seated, 7 clips in `vidoes/2026-11-10/`, words in `improv_script.md`). 3 problems are now forced topic / too heavy / no expertise → "built with you, interview ready". Edit v2 `LAUNCH1_final.mp4` (30 s, LAUNCH2 style) **approved by the user 6 Nov**; publishing pack v2 + cover `cover_LAUNCH1.jpg` done. Shawn ticks F2–F4, then post 16 Nov. F1 = 80 teams (confirmed).
- ☐ Setup week (9–14 Nov): Instagram account, website v1, Google Business Profile + 5 reviews, ManyChat, YouTube.
- ✅ Animated ASS text engine is the default in `reel_assemble.py` (Anton, word pop, `*emphasis*` orange box). v3 render waiting for Shawn's verdict.
- ✅ Launch week scripted: LAUNCH1, SURVIVAL1, DROP1 (shoot all 3 on 10 Nov, run sheet `04_reel_production/shoot_days/2026-11-10_SHOOT-DAY.md`) + LAUNCH2. All wait for Shawn's approval + fact ticks.
- ✅ Week 2 scripted: LAUNCH2, SURVIVAL2, LAUNCH3 + run sheet `shoot_days/2026-11-17_SHOOT-DAY.md`. Manglish guide: `04_reel_production/MANGLISH_GUIDE.md`.
- ✅ **Naming changed 6 Nov:** scripts are `scripts/<post date>_<REEL NAME>_<topic>.md` (LAUNCH1, SURVIVAL1, DROP1 …), footage `vidoes/<shoot date YYYY-MM-DD>/`. Old TPS-YYMMDD-… IDs are gone.
- ⚠ LAUNCH2 (free consult) was shot early on 6 Nov, freestyle (sitting, own words, no props): 5 clips in `vidoes/2026-11-06/` (`Day 4/` = identical copy). Script v2 rebuilt from the footage, **edit approved by the user (6 Nov)**; end-card tagline stays "Learn It. Build It. Own It." (confirmed 6 Nov). Cut (`vidoes/2026-11-06/LAUNCH2_final.mp4`, 47 s: no punch-zooms, soft fades, no progress bar, lower text, CTA + free-consultation line, end card v2). Waiting for Shawn to watch + tick F3–F5. Its 4 B-roll shots are on the 17 Nov sheet.
- ☐ DROP2: research + script ~14–15 Nov. ☐ Thu carousels (19, 26 Nov) from SURVIVAL1/SURVIVAL2 facts.
- Open questions for the user: Instagram handle choice · student tool roadmap · website builder/platform · first demo build.
