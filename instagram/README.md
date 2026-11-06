# Instagram config (project-local)

This folder holds the data the `ig-*` skills read and write. It stays inside
this project instead of `~/.claude/instagram/`.

| File | Written by | Purpose |
|---|---|---|
| `voice.md` | you (human) | Brand voice, audience, positions, proof, CTAs. Read by every writing skill. **Keep it current.** |
| `swipe.md` | `/ig-viral` | Ranked swipe file from accounts in the niche. |
| `plan.md` | `/ig-plan` | The weekly content plan. |
| `log.md` | `/ig-reel`, `/ig-comment` | What has been posted/commented and when. |

## How to use

In OpenCode:

- `/ig-reel <idea>` or just ask "make a reel about X"
- `/ig-caption` after a reel or carousel is drafted
- `/ig-plan` once a week
- `/ig-human` on any draft before it goes out
- `@ig-reel` also loads the skill directly

The skills write; they never post. You copy the output and post it yourself.

## Windows notes

The upstream repo assumes `python3` and `pbpaste`. This install uses:

- `python` (Python 3.11 is on PATH; `python3` is a dead Microsoft Store alias)
- UTF-8 stdout and BOM-safe input reads, so the box-drawing output works in
  PowerShell
- `Get-Clipboard |` instead of `pbpaste |` in examples

## Source

`Jakeschincariol/instagram-agent-skill` (MIT). Skills live in
`.opencode/skills/ig-*`, slash commands in `.opencode/commands/ig-*.md`.
Local changes: config paths point here, Python commands use `python`, and the
scripts have the Windows encoding patch.
