# PROGRESS: session handover log
**Next session: read `AGENTS.md`, then this file, then continue the "IN PROGRESS / NEXT" items.**
Update this file at the end of every work block (newest entry on top).

---

## Session 2026-11-06 (part 2: text engine + next scripts)

### Done
- **Animated text engine (libass/ASS) built, now the default** in `pipeline/reel_assemble.py`: Anton/Montserrat, word-by-word pop, `*emphasis*` = orange box with black text, slide-up/fade. Old look via `export: {text_engine: drawtext}`. Backup: `pipeline/reel_assemble.py.bak_v2`. Render: `vidoes/DAY1/day1_test_pipeline_v3.mp4`, compare strip `vidoes/DAY1/v2_vs_v3_compare.jpg`. Known nits: TXT-LABEL box nearly invisible on bright walls; slight offset of the orange box during the 120 ms pop.
- **Scripts:** `scripts/2026-11-18_SURVIVAL1_activity-points.md` (activity points, shoot 10 Nov with LAUNCH1) · `scripts/2026-11-23_LAUNCH2_free-consult.md` (free consult; steps F2–F5 are guesses for Shawn to confirm; no prices in public).
- **Research:** `04_reel_production/research/SURVIVAL1_activity_points_facts.md` (2019 scheme: 100 pts / 75 LE, "mandatory for the degree"; per-activity caps + deadlines unverified, keep off screen) · `research/DROP1_listings.md` (thin: most programs closed; needs a browser check).

### Added later (6 Nov)
- **DROP1 written** (`scripts/2026-11-20_DROP1_internships.md`): KSUM AIP · Amazon SDE intern (2027 grads) · Science Academies SRFP 2027 (2nd/3rd yr, closes 30 Nov), browser-verified 6 Nov. Shot 10 Nov with LAUNCH1 + SURVIVAL1; screen recordings + re-check 19 Nov; re-check 20 Nov; DM bonus decided 20 Nov.
- All scripts now have SETUP AT A GLANCE + SHOT LIST (frame per shot, B-roll), written for our real gear (iPhone, 2nd-phone teleprompter, wireless mic, 1 tripod, tube lights). Framing guide: template A3b.
- **Run sheet for 10 Nov:** `04_reel_production/shoot_days/2026-11-10_SHOOT-DAY.md` (all 3 reels, ~2 h 45 min, take log in recording order).

### NEXT
1. Shawn: watch v3 (text look verdict), approve LAUNCH1 + SURVIVAL1 + LAUNCH2, tick the fact sheets (LAUNCH1 F2, SURVIVAL1 F4, LAUNCH2 F2–F5).
2. Before 17 Nov: open IGNITE / Technopark / Infopark / Internshala in a browser, pick 3 + bonus → write DROP1 (shoot 17 Nov, post 20 Nov).
3. Write SURVIVAL2 (Phase II prep), DROP2, LAUNCH3.
4. Setup week 9–14 Nov (IG account, ManyChat PROJECT + booking link: LAUNCH2 depends on it).
5. Optional polish: label box opacity/outline in the ASS engine.

---

## Session 2026-11-06 (long planning + build session)

### Done
- Research: competitors (26 reels) + 6 big face-cam pages (30 reels) → `03_competitor_research/REEL_FORMULA.md` (+ Validation v2). Books/skills/audience/trends/comments/fonts/editing-tools research in `03_competitor_research/research/`.
- Strategy: `01_strategy/6_MONTH_PLAN.md` v2 (KTU-calendar aligned), local growth + visibility plans in `02_growth_and_visibility/`.
- Production system: `04_reel_production/SCRIPT_PLAYBOOK.md` (15 laws, hook score, gates), `REEL_SCRIPT_TEMPLATE.md` (D0 plain-English section, codes, Read Mode, shoot card, publishing pack, YAML), `CONTENT_CALENDAR.md`.
- First script: `04_reel_production/scripts/2026-11-16_LAUNCH1_why-we-started.md` (launch reel 1). **Shawn's feedback:** the Manglish was bad and the acting unclear → plain-English D0 section added (rule now permanent).
- Tools: `pipeline/build_reel.py` fixed (no flash, safe-zone hook). `pipeline/reel_assemble.py` built (YAML → final reel), fixed on real footage (no-music crash, xfade timebase), face-avoiding text, logo/text collision fix, explicit orange highlight. `pipeline/reel_breakdown.py` (contact sheets).
- Day 1 validation renders: `vidoes/DAY1/day1_test_pipeline_v1.mp4` (text over the face) and `…_v2.mp4` (layout fixed). The test YAML is in the scratchpad (`day1_val/day1_test.yaml`; copy kept at `pipeline/tests/day1_test.yaml`).
- Folder reorganisation (01–05 folders, READMEs), `AGENTS.md` + `CLAUDE.md`, memory files.

### Shawn's feedback still open
- **v2 still looks plain:** Arial + simple fades. Wants the premium look (bold fonts, animated text).

### IN PROGRESS (6 Nov, end of session)
1. ✅ **Fonts downloaded:** `pipeline/assets/fonts/` = Anton-Regular, Montserrat-ExtraBold, Montserrat-Black + OFL licences.
1b. ✅ **HyperFrames plugin INSTALLED** (6 Nov, scope: user). Next: `/reload-plugins` or a new session, then check its skills load and that the HyperFrames CLI is reachable (kinocut `hyperframes_doctor` said "CLI not found" before the install, so it may need `npx hyperframes`). Then test a transparent overlay layer (emoji pop, arrow, progress bar) composited onto v3. Install log: (`claude plugin marketplace add heygen-com/hyperframes`, then `claude plugin install hyperframes@hyperframes`). Check `/plugin` that it's installed, then run kinocut `hyperframes_doctor`.
2. **Animated text engine (step 1):** subagent is adding libass/ASS styled text to `reel_assemble.py`: Anton/Montserrat, word-by-word pop (110→100 %), orange highlight box with black text, thick outline + shadow, slide/fade, 2–4 words per line. Then re-render Day 1 → `vidoes/DAY1/day1_test_pipeline_v3.mp4`.
   - Check: does v3 exist? Is `pipeline/README.md` updated with the new text options?

### NEXT (in order)
1. Show Shawn v1 vs v2 vs v3 (frame strips). Get his verdict on the text look.
2. Step 2 (optional, premium motion graphics): **user runs** `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes` (Node v26 is installed). Then test HyperFrames for emoji pops / animated arrows / progress bars as a transparent overlay layer.
3. Shawn re-reads LAUNCH1 (the English D0 section), ticks the 4-item fact sheet, and does a **30-s test shoot** with the real setup (chest-up, ~1 m, teleprompter) → render with `reel_assemble.py`.
4. Write the remaining launch scripts: SURVIVAL1, DROP1, LAUNCH2, SURVIVAL2, DROP2, LAUNCH3 (calendar). D0 English-first format.
5. Setup week (9–14 Nov): Instagram account, website v1, Google Business Profile + 5 reviews, ManyChat, YouTube.
6. Content-creation extras: brand kit + cover templates, topic backlog, carousel/story templates, Manglish spelling list, consent template, music list, YouTube long-form template, Insights log.

### Open questions for the user
Instagram handle · student tool roadmap · website platform/builder · first demo build · office town (location tag) · confirm the LAUNCH1 3 problems (topic/build/viva).
