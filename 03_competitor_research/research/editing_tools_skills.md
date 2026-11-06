# Editing tools and skills for premium Reels (researched 2026-11-06)

Method: read-only `gh api` (repo metadata, READMEs, license files). Nothing cloned, installed or run. Stars and last-push dates are live as of today. Items marked UNVERIFIED are from my background knowledge and were not checked.

Constraint recap: hand-written text and timings per beat (YAML), no ASR/captions, Windows laptop, single editor (Claude), minimal new dependencies, existing Python + ffmpeg pipeline.

## Master table

| # | Tool | Stars | Last push | License (commercial?) | Runtime | Integration with Python+ffmpeg | Text animation quality | Render speed (Win laptop) | Paid keys? |
|---|------|-------|-----------|----------------------|---------|-------------------------------|------------------------|---------------------------|-----------|
| 1 | HyperFrames (github.com/heygen-com/hyperframes) | 79.5k | 2026-11-05 | Apache-2.0 (yes) | Node >=22, headless Chromium (bundled by CLI), ffmpeg | Good: CLI renders an HTML file to MP4. Python writes/templates the HTML from the YAML, then calls `npx hyperframes render`. Studio desktop app exists for Windows. | Very high: full CSS/GSAP-style seekable animation, so pop, bounce, highlight boxes, emoji, SVG arrows, progress bars. Deterministic. | Medium: Chromium frame capture, roughly real-time to a few x slower for 30-60s 1080x1920 (UNVERIFIED). | No for core. Studio Pro plan adds HeyGen AI models, optional. |
| 2 | Remotion (github.com/remotion-dev/remotion) | 71.0k | 2026-11-05 | Custom "Remotion License": free for individuals, for-profit orgs up to 3 employees, non-profits. Larger companies need a paid Company License. Check the team size. | Node + React + Chromium (downloaded by Remotion) + ffmpeg bundled | Medium: React project plus `npx remotion render comp out.mp4 --props=script.json`. A Python script can dump the YAML to JSON props. | Very high: spring(), interpolate(), `@remotion/transitions`, `@remotion/shapes`, `@remotion/google-fonts`, Lottie, noise. Best ecosystem. | Medium: Chromium per frame, multi-threaded, about 1-3x real-time on a laptop (UNVERIFIED). | No (Remotion Lambda is optional and paid). |
| 3 | Remotion Agent Skills (github.com/remotion-dev/skills) | 6.4k | 2026-11-05 | No license file shown on the repo (treat as use-as-intended with Remotion) | Agent Skills format, works with Claude Code | Easy install: `npx skills add remotion-dev/skills`. Skills: remotion-best-practices (umbrella), remotion-create, remotion-render, remotion-captions, remotion-multimedia, remotion-interactivity, remotion-docs, remotion-markup, remotion-maps, remotion-license | Teaches Claude correct Remotion animation idioms. Quality = Remotion's. Skip remotion-captions (it is Whisper-oriented). | n/a | No |
| 4 | HyperFrames skills (same repo, 9 skills) | (in #1) | 2026-11-05 | Apache-2.0 | Claude Code plugin or `npx skills` | Easy: `/hyperframes` (contract plus references for captions, overlays, motion, look), `/hyperframes-cli`, `/hyperframes-registry` (blocks catalog), `/media-use`, `/remotion-to-hyperframes`, `/reverse-any-video` (copy a reference reel's style), `/style-sampling`, `/slideshow`, `/figma` | Strong: also ships a catalog of ready-made animated blocks. | n/a | No for core |
| 5 | libass / ASS subtitles via ffmpeg `subtitles`/`ass` filter (github.com/libass/libass) | 1.2k | 2026-11-05 | ISC (yes) | Nothing new: libass is already inside standard ffmpeg builds (verify with `ffmpeg -filters` showing `ass`) | Excellent: generate a `.ass` file from the YAML in Python, add one filter to the existing command. Fonts via `fontsdir=`. | Good for text: `\t` transform animations (scale pop 120%->100%, color/alpha fades), `\move`, `\fad`, `\blur`, `\bord`, `\3c` outlines, `\p1` vector drawing (boxes, arrows, circles), `\k` karaoke wipe. Limits: no emoji color fonts (use PNG overlay), no easing curves beyond accel, no real bounce physics (fake with chained `\t`). | Fastest: same ffmpeg pass, no extra decode. | No |
| 6 | MoviePy (github.com/Zulko/moviepy) | 15.1k | 2026-08-26 | MIT (yes) | Python + ffmpeg + Pillow | Easy (pure Python) but would replace the current pipeline for composition. `TextClip` plus `resized(lambda t: ...)`/`with_position(lambda t: ...)` gives per-frame scale and position. | Medium: every effect is hand-coded per-frame lambdas, text rasterised by Pillow (no CSS, no emoji color without work). | Slow: Python per-frame compositing, 2-10x slower than ffmpeg filters. | No |
| 7 | pycaps (github.com/francozanardi/pycaps) | 230 | 2026-09-30 | MIT (yes) | Python 3.10-3.12, ffmpeg, Playwright/Chromium for CSS rendering | Medium: pip install. Accepts your own transcript via `--transcript transcript.json`, so Whisper is skipped; word timings would be hand-authored in that JSON. But Whisper is a core dependency and downloads a model on first use (alpha status). | Good: CSS-styled words, `.word-being-narrated` state, pop/fade/slide animations, emoji and sound-effect insertion. Built for word-by-word captions, not free-form overlays. | Medium (Chromium frames) | No (AI tagging is optional and uses an API) |
| 8 | Motion Canvas (github.com/motion-canvas/motion-canvas) | 19.7k | 2026-07-02 | MIT (yes) | Node, browser editor, ffmpeg render plugin | Poor fit: generator-function timeline, aimed at explainer diagrams, not overlays on live footage. | High for vector/kinetic typography | Medium | No |
| 9 | Revideo (github.com/midrender/revideo, formerly redotvideo) | 4.2k | 2026-07-15 | MIT (yes) | Node + headless browser + ffmpeg | Medium: Motion Canvas fork with an API (`renderVideo`) and video-in-scene support; callable from a script. Less community than Remotion/HyperFrames. | High | Medium-fast | No |
| 10 | captacity (github.com/unconv/captacity) | 141 | 2024-06-07 | MIT | Python + MoviePy + Whisper | Stale and Whisper-bound. Not recommended. | Basic | Slow | No |
| 11 | zhuyansen/awesome-claude-video-skills (awesome list) | 1.6k (UNVERIFIED count, from `gh api` stargazers = 1624) | not checked | not checked | n/a | Use as a discovery index only; `gh search` for "ffmpeg skill" returned nothing useful, so the dedicated skills above are the real finds. | n/a | n/a | n/a |
| 12 | Kinocut MCP (already connected in this environment) | n/a | n/a | n/a | MCP server | Already available: `video_add_texts`, `video_validate_text_layout`, `hyperframes_doctor`, `video_review_package`. It has a HyperFrames doctor, so it likely expects HyperFrames. Worth testing before installing anything. | Unknown, check | Unknown | Unknown |

Not checked (could not verify in time): ComposioHQ/awesome-claude-skills and travisvn/awesome-claude-skills contents; Kdenlive/MLT, Natron, After Effects scripting (excluded as heavy or paid); Lottie via `rlottie`/`lottie2gif` (UNVERIFIED, would give icon/emoji pops as overlays).

## Notes on key trade-offs

- Windows: HyperFrames and Remotion both need Node (>=22 for HyperFrames) and Chromium. That is one new runtime, not a Python library stack. libass needs nothing new.
- No-caption rule: neither HyperFrames nor Remotion transcribes anything by default. You give them text and frame/second timings. pycaps and captacity assume Whisper, so they fit the rule poorly.
- Licensing: HyperFrames (Apache-2.0) has no company-size condition. Remotion is free only for individuals / up to 3 employees / non-profits; confirm The Project Shop qualifies. Safer default: HyperFrames.
- Fonts: both browser renderers use Google Fonts or local TTF/WOFF via CSS, so bold modern fonts (Montserrat ExtraBold, Poppins, Anton, Bebas Neue, Inter Tight) are easy. Emoji work as native color emoji or Twemoji/Noto SVG.
- Sound-synced motion: in both, you pass your beat times from YAML (or analyse audio peaks in Python) and place animations at exact frames.
- Practical architecture for either browser option: render ONLY the text/graphics layer as a transparent (alpha) WebM/ProRes 4444 or PNG sequence, then composite onto the footage with the existing ffmpeg step. That keeps your cut/clean pipeline and uses the browser engine just for motion graphics. HyperFrames/Remotion both support transparent output (Remotion: `--codec=vp8/prores --pixel-format=yuva420p`; HyperFrames: check docs, UNVERIFIED).

## Ranking for "premium look, minimal new deps, Windows, single editor Claude"

1. HyperFrames + its Claude skills (Apache-2.0, 79k stars, active today, skills are first-class, HTML/CSS means Claude writes polished animation easily, catalog of ready blocks, `/reverse-any-video` to copy a reference reel's style, no license caveat, a Kinocut doctor tool is already connected).
2. libass / ASS via existing ffmpeg (zero new dependencies, fastest render, quick win for pop-in text, highlight boxes, karaoke color wipes; limited for emoji, bounce physics and complex graphics). Best as an immediate upgrade and fallback.
3. Remotion + remotion-dev/skills (best animation ecosystem and docs, official skills, but the custom license needs a team-size check, and the React project is heavier than HyperFrames' plain HTML).

## Install command for the #1 pick (USER runs it; not executed here)

Prerequisite: Node.js 22 or newer (`node -v`).

Claude Code plugin route (recommended):

```
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

Then in a project folder, ask Claude to use `/hyperframes:hyperframes`.

Alternative, skills only:

```
npx hyperframes skills update
```

(installs the core set: /hyperframes, /hyperframes-cli, /hyperframes-registry, /media-use). Add `/reverse-any-video` later with `npx hyperframes skills update reverse-any-video`.

First test: have Claude render a 5s transparent text-overlay with a pop-in word, a highlight box and an emoji, and composite it with the current ffmpeg step; measure render time on the laptop before committing.

## Sources
- https://github.com/heygen-com/hyperframes (README, repo metadata)
- https://github.com/remotion-dev/remotion (LICENSE.md, metadata)
- https://github.com/remotion-dev/skills (README, skills list)
- https://github.com/francozanardi/pycaps (README)
- https://github.com/libass/libass, Zulko/moviepy, motion-canvas/motion-canvas, midrender/revideo, unconv/captacity (metadata only)
