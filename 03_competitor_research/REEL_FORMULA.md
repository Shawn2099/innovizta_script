# The Reel Formula (cracked from 26 competitor reels)
6 Nov 2026 · data: `competitor_reels/` (videos, `manifest.csv`, `captions.txt`, `_breakdown/` contact sheets, metrics and Haiku notes per account)
Sample: Idukki (8), Febtech (7), Flemin (8), bbx (3). Each account's top and bottom reels were compared. **n = 26, so these are strong patterns, not laws. Test them with Trial Reels.**
*Limits:* these are 4 Kerala accounts (3 under 5K followers), not the biggest pages in the niche. A validation pass on 2–3 large proven pages is pending. Spoken hooks (e.g. Flemin's 109K) are taken from captions. `voiced_ratio` in the metrics = the non-silent share (music counts), not speech. The speech check (Whisper base) was **inconclusive**: it "detected" Malayalam even on mostly-music reels like the 250K printer fail, so it can't tell speech from music. None of the rules depend on it.

---

## The formula in one line
> **One real thing + one tension line in the first second → let the thing itself keep changing → pay it off → one clear ask.**

## The 9 rules (with evidence)

| # | Rule | Evidence |
|---|---|---|
| 1 | **The first frame shows one clear subject already doing something.** A face holding a prop, a machine moving, a hand triggering a result. No logo, no "hi guys", no scenery. | Idukki 250K: printer already failing in frame 1 · Idukki 68.5K: hand gesture lights a bulb at ~1 s · every Flemin top reel centres one physical object in second 1 · low tier: drifting clouds (4.6K), distant wide shot (451) |
| 2 | **A tension line of ≤8 words by 2 s**, as text and/or speech. The winning types: **sarcasm/fail, "not as simple as it looks", fear, curiosity question, recognisable name.** | "EXTRAORDINARY SKILLS TRYING TO PRINTING ON AIR" (250K) · "This design was not that simple as see…" (54K) · "AI IS GOING TO TAKE YOUR JOB" (80K) · "What if the internet just disappears?" (109K) · "SOLIDWORKS" name tag (38K) |
| 3 | **A plain title label is not a hook.** "PROJECT BIKE SAFETY SYSTEM" names the topic but creates no tension. | Idukki's cleanest, most polished reel with a title label got 6K, among his lowest |
| 4 | **Real phone footage beats polish.** Continuous, real shots of real devices outperformed CGI, motion graphics and event montages. | Febtech's top 4 are single phone shots, its bottom 2 are 3D/motion graphics · bbx's 43-cut event montage got 112 views · production level was 2–3/5 across all top reels |
| 5 | **Keep it visually changing, but the change can come from the action, not from editing.** Top build reels had 0–1 *hard scene changes* because the *process* keeps moving. Talking heads need text changes or punch-ins every 2–4 s instead. | Idukki and Febtech top reels: 0–1 hard scene changes (the detector misses jump cuts in the same framing, so talking-head counts are a lower bound) · bbx 80K: big kinetic text swapping every ~1–2 s |
| 6 | **Length follows how watchable it is.** Build/story reels of 57–90 s got the most views (we only have view counts, not retention). Explainers and talking heads ran 20–40 s. | Idukki top 57–90 s, Flemin top 57–85 s, Febtech top 19–27 s, bbx top 32 s |
| 7 | **Stay in your niche.** Off-topic content flops even on the same account. | Flemin music clips 203–451 vs career reels 20–109K · Febtech X-ray explainer 1.7K · bbx event PR 112 |
| 8 | **Story or emotion can carry a late payoff.** Without a hook, only a personal story holds people to the end. | "My first project in 2020" 125K (reveal at ~64 s) · "Will be back soon" (health) 61K |
| 9 | **Career/internship + comment keyword works.** Readable with the sound off, with an explicit ask at the end. | Flemin 57.7K "scouting interns… *Type CYBERSECURITY below*" (also another company's openings, which validates the Opportunity Drop) · bbx 80K ends on a "JOIN NOW" card · a no-text skit got 4K |

## Validation v2: 30 reels from 6 big face-cam pages (6 Nov)
Pages: @callmeshazzam (1.9M, Malayalam) · @techonemalayalam (636K, Malayalam) · @ankurwarikoo (4M) · @arshgoyalyt (473K) · @tanaypratap (120K) · @markrober (3M). Notes: `competitor_reels/bigpages/*_visual.md`.

| Rule | Verdict on big pages | Change |
|---|---|---|
| R1 real subject acting in frame 1 | **Holds** (28/30). The device/screen is in frame by 2 s on 10/10 Malayalam reels | Keep. Add: show the *object* by 2 s |
| R2 tension line ≤8 words by 2 s | **Holds** (all career reels pass the count) | Keep. The count is necessary, not sufficient |
| R3 plain title label isn't a hook | **Narrowed:** a plain topic label with no subject fails (5.1K), but **numbered promises** ("5 money rules" 3.7M) and **"X vs Y"** (2.2M) work as hooks | Allowed hook types now include NUMBERED-PROMISE and X-VS-Y |
| R4 real footage beats polish | Not testable (confounded by account) | Keep (no contradiction) |
| R5 change every 2–4 s | **Holds, reframed:** changes come from overlays, inserts or action. **Hard-cut count doesn't predict views** (0-cut reels from 53K to 5.9M) | Keep the "visual change" rule, don't chase cut counts |
| R6 length bands | **Contradicted:** talking reels of 43–84 s (Ankur 3.4–3.7M) and 141–169 s (Shaz 0.4–3.2M) went big | **Length is not a ceiling.** Start at 30–60 s; go longer only when each beat adds new value. Check watch-% in Insights |
| R7 stay in niche | **Holds, refined:** within an account, **lived access/proof** beats general opinion (Arsh's "at Intuit" 5.9M vs his AI-bubble take 1.6K). Celebrities (Rober) can stray, a new page can't | Keep. Prefer "what we saw/built" over "what I think" |
| R8 story carries a late payoff | Weakly holds | Keep |
| R9 readable on mute + explicit ask | **Ask contradicted:** top reels on the big pages show **no on-screen CTA**. The only keyword ask on the Malayalam pages was on the lowest reel | **Value reels: spoken or caption ask only, no CTA card. Keyword CTA cards only on lead reels (DROP, PIW)** |

**New patterns to add (seen on several big pages):**
1. **Numbered-promise pill** as the spine: a fixed "1/5, 2/5…" card per beat, every 8–15 s (Ankur)
2. **Access/proof in the first 2 s:** "We are here at…", "Microsoft invited me…". For us: "Ithaa njangalude workshop", a real build, a real price
3. **Evidence card within 10–15 s:** screenshot, price table, rate card, job-post count (Ankur, Tanay)
4. **Big money number as the stakes:** "₹500", "6000 AED" (Shaz, Tech One)
5. **Fixed series signature:** the same progress bar, pill style, one highlighted key word colour, and end card per series (Tanay, Ankur)
6. **"This is not X, it's Y"** over a prop (Rober) · **audience-answer hook** ("Who has coding in college?" → "Yes.") (Tanay)
7. **Top-down tripod insert with a visible timer/counter** for builds (Rober)

## Anti-patterns (seen in the bottom performers)
- Opening on scenery, a wide static shot or a logo
- Title-card hook with no tension ("PROJECT ___ SYSTEM")
- Motivational quotes and music/vibe clips (off-niche)
- Event recaps / PR montages with nobody talking to the viewer
- CGI or motion-graphic explainers with no real footage
- No on-screen text (unreadable when muted)

## What we do with it
| Our series | Formula applied |
|---|---|
| **Project Idea of the Week** | Frame 1 = the demo already working (result-first) + tension line ("₹900-nu ithu build cheyyam?"). Let the build *process* run (rule 5). 45–75 s |
| **Survival** | Shawn CU + a big kinetic text hook (fear/curiosity: "Activity points illenkil degree illa?"). Text or punch-in change every 2–3 s. 20–35 s |
| **Opportunity Drop** | Shawn holding the phone showing the listing + "₹15K stipend, ee aazhcha" + the INTERN keyword (rule 9). 45–60 s |
| **AI / build in public** | Screen + hands, "not as simple as it looks" tension. 25–40 s |
| **Human** | Single continuous shot of a real fail or a moment + one sarcastic line (the 250K pattern). 10–30 s |

The shot-by-shot version is `REEL_SCRIPT_TEMPLATE.md`.
