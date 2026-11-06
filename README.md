# The Project Shop: workspace map
Everything for The Project Shop's marketing (Instagram, YouTube, Google, outreach) lives here. **Start with `00_PLAN_INDEX.md`.**

| Folder / file | What it is | Rule |
|---|---|---|
| `AGENTS.md` (+ `CLAUDE.md` → imports it) | **Agent context + the "today's content" routine.** Every session reads this first | Keep §6 "current state" updated |
| `00_PLAN_INDEX.md` | Master index: goal, decisions, 15 workstreams, open questions | Update the workstream status after every session |
| `01_strategy/` | The plans: 6-month global plan (master), social media strategy, original company notes | `6_MONTH_PLAN.md` wins any conflict |
| `02_growth_and_visibility/` | How students find us and how we reach them: local growth, Google/IG/YouTube visibility, direct reach | |
| `03_competitor_research/` | Competitor analysis, the cracked reel formula, and the downloaded competitor reels + breakdowns | Competitor videos are for **study only**, never reposted |
| `04_reel_production/` | Script playbook, global script template, **content calendar (dated plan + status)**, series formats, filled-in reel scripts | Every reel script = a copy of the template's Part D |
| `05_founder_inputs/` | Founders' handwritten notes and other raw inputs | Read-only reference |
| `instagram/` | Brand voice file for the OpenCode `ig-*` skills | **Don't move or rename.** The skills point at this path |
| `pipeline/` | Reel editing and analysis tools (`build_reel.py`, `reel_breakdown.py`, …) | **Don't move.** Global CLAUDE.md points here |
| `vidoes/` | Our own raw footage and Day 1–3 edits | Name kept (rename was blocked by Windows). New shoots go in `vidoes/<shoot date YYYY-MM-DD>/` |
| `.claude/`, `.opencode/` | Tool settings | Don't edit by hand |

Naming conventions:
- Reel name (also the tracking code and the clip prefix): `<SERIES WORD><n>`, e.g. `LAUNCH1`, `SURVIVAL2`, `DROP1`, `IDEA1`. Series words: LAUNCH (launch/story, code STO) · SURVIVAL (SRV) · DROP · IDEA (Project Idea of the Week, PIW) · BUILD (AI/build in public, AIB) · FUN (HUM)
- Scripts: `04_reel_production/scripts/<post date YYYY-MM-DD>_<REEL NAME>_<topic>.md`, e.g. `2026-11-16_LAUNCH1_why-we-started.md` (sorted = posting order; if the post date moves, rename the file, the reel name stays)
- Footage: `vidoes/<shoot date YYYY-MM-DD>/<REEL NAME>_<beat>_t<n>.mp4`, e.g. `vidoes/2026-11-10/LAUNCH1_B1_t2.mp4`; best take `…_KEEP.mp4`. Shoot-day sheets: `04_reel_production/shoot_days/<shoot date>_SHOOT-DAY.md`
