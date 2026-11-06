# Fonts and on-screen text styles for short-form reels (research, 2026-11-06)

Scope: free-for-commercial-use fonts, premium text patterns, and one recommended pairing for The Project Shop (1080x1920). Sources are listed at the end. Items marked UNVERIFIED were not confirmed by a primary source in this session.

## 1. Fonts: license and use

| Font | License | Where | Best use | Weight |
|---|---|---|---|---|
| Anton | SIL OFL 1.1 (confirmed from OFL.txt: "Copyright 2020 The Anton Project Authors") | https://fonts.google.com/specimen/Anton | Hook, big key lines. Condensed, very loud. Used by Hormozi-style captions (third-party guides) | Regular (single weight) |
| Montserrat | SIL OFL 1.1 (copyright notice confirmed in secondary sources) | https://fonts.google.com/specimen/Montserrat | Body lines, Manglish lines, labels. Wide, clean Latin | ExtraBold 800 or Black 900 |
| Poppins | SIL OFL 1.1 (secondary source only) | https://fonts.google.com/specimen/Poppins | Alternative to Montserrat for body | Black 900 / ExtraBold 800 |
| Bebas Neue | SIL OFL 1.1 (Font Squirrel licence text) | https://fonts.google.com/specimen/Bebas+Neue | Labels, all-caps tags, section cards | Regular only |
| Archivo Black | OFL (folder contains OFL.txt, confirmed on GitHub; text not read) | https://fonts.google.com/specimen/Archivo+Black | Alternative hook font, heavy | Regular only |
| Oswald | OFL (from knowledge, not re-checked) | https://fonts.google.com/specimen/Oswald | Condensed alternative to Anton | 600-700 |
| Inter | OFL (from knowledge, not re-checked) | https://fonts.google.com/specimen/Inter | UI-style text; less punchy than Montserrat | Black 900 |
| League Spartan | OFL (from knowledge, not re-checked) | https://fonts.google.com/specimen/League+Spartan | Alternative geometric sans | Black 900 |
| Komika Axis | Not verified. Google Fonts folder fetch returned 404 | UNVERIFIED | Comic style, not for a serious brand | n/a |
| The Bold Font | Commercial (paid licence per most sources; UNVERIFIED) | Paid | Not recommended on cost grounds | n/a |
| Proxima Nova, Gilroy | Paid commercial licence | Paid | Not needed; Montserrat covers the same role for free | n/a |

Malayalam script (only needed if on-screen text is written in Malayalam script, not Manglish):
- Noto Sans Malayalam: OFL 1.1. https://fonts.google.com/noto/specimen/Noto+Sans+Malayalam
- Baloo Chettan 2: OFL 1.1 (Fontsource and online-fonts.com). https://fonts.google.com/specimen/Baloo+Chettan+2
- Manjari: Google Fonts folder lists OFL.txt, and files Manjari-Regular/Bold/Thin.ttf. Licence text not read in this session. https://fonts.google.com/specimen/Manjari
- Caveat: a Google Android metadata file flags Noto Sans Malayalam packaging as needing review. That applies to the Android packaging, not the font files, but check if reusing it in a product.

Manglish is written in Latin script, so Montserrat or Anton covers the on-screen text. The Malayalam fonts are only needed for native-script text.

Hormozi font: sources disagree. Most guides name "The Bold Font" (older) and Anton (newer), with Montserrat Black as the free stand-in. No primary source from Hormozi or his editors was found, so treat this as unverified.

## 2. Premium text style patterns (specs for 1080x1920)

Vendor blogs and creator-analysis guides agree on the broad patterns. The numeric specs below are starting points, not measured from competitor files.

1. **White text, thick black outline, soft drop shadow.** Stroke 3-4 px at 1080 width per vendor guides. For a 110 px font, use a stroke of 12-14 px. Shadow: 0 6px 0 rgba(0,0,0,0.35) or a soft 0 8px 16px blur. Use this on busy footage.
2. **Highlight box behind one key word.** Solid box in brand orange #FF8A00 (or yellow/green for variety) with black text inside. Padding 12-18 px horizontal, 6-10 px vertical, corner radius about 12 px. Only one word per line gets the box. Not white text on orange: contrast is about 2.3:1, so use black text on the orange box.
3. **Word-by-word pop.** Each word appears on its beat. Scale 110% to 100% over about 6 frames (200 ms at 30 fps), with a 1-2 frame fade-in. Keep the motion subtle for older audiences (vendor advice).
4. **Line length.** 2-4 words per line, max 2 lines on screen at once. Vendor guides say 2-3 words for fast-paced reels.
5. **Placement.** Keep text out of the top about 250 px (username and menu) and the bottom about 300-450 px (caption, audio ticker, action buttons). Sources disagree on the exact bottom value (250 to 670 px depending on the guide), so use a conservative lower-middle block around y = 900-1300 for body lines, and y = 300-600 for hook text. Preview on a phone before posting. Meta's own safe-zone diagram was not found in this session.
6. **Emoji accents.** Single emoji beside the highlight word, not after every line. Scale it to about 1.2x the text size.
7. **Highlight colour rule.** Vendor guides say highlight one word per beat, the word that changes the meaning. Orange, yellow, or green are the common choices.

## 3. Recommended pairing for The Project Shop

Brand: orange #FF8A00, black, white. Audience: Kerala engineering students, Manglish in Latin script.

- **Display (hooks, key lines): Anton Regular.** Condensed, high impact, OFL.
- **Body and Manglish lines: Montserrat ExtraBold 800.** Clean Latin, OFL, easy to read on a phone.

Sizes at 1080x1920:
- Hook (top, 1-3 s): Anton 130-150 px, uppercase, line-height 1.0, tracking 0, white with 14 px black stroke, orange highlight box on the key word.
- Key line (mid-reel): Anton 110-120 px, uppercase, same stroke.
- Body / Manglish line: Montserrat ExtraBold 800, 72-84 px, sentence case, white with 10 px black stroke.
- Label or tag: Montserrat ExtraBold 800, 48-54 px, black text on orange box.

Keep max 3 words per line for Anton at 130 px. Max 2 lines on screen.

Per CLAUDE.md for this project: no auto-generated captions burned in. Use short hand-written hooks and key lines only, and judge text from the footage and timestamps the user confirms.

## 4. Sources

- Hormozi font, third-party guides: https://www.kapwing.com/explore/hormozi-style-captions-template , https://www.submagic.co/blog/how-to-make-alex-hormozi-captions , https://www.thumbmagic.co/blog/how-to-make-alex-hormozi-captions
- Montserrat licence: https://en.wikipedia.org/wiki/Montserrat_(typeface)
- Poppins OFL list: https://www.fontsquirrel.com/fonts/Bebas-Neue (Bebas Neue licence text); general OFL/Google Fonts overview: https://typewolf.com/google-fonts
- Bebas Neue OFL: https://www.fontsquirrel.com/fonts/Bebas-Neue
- Anton licence text (fetched): https://github.com/google/fonts/blob/main/ofl/anton/OFL.txt
- Archivo Black folder (fetched, OFL.txt present): https://github.com/google/fonts/tree/main/ofl/archivoblack
- Manjari folder (fetched): https://github.com/google/fonts/tree/main/ofl/manjari
- Baloo Chettan 2 licence: https://fontsource.org/fonts/baloo-chettan-2 (via npm @fontsource/baloo-chettan-2) and https://online-fonts.com/fonts/baloo-chettan-2
- Noto Sans Malayalam: https://fontsource.org/fonts/noto-sans-malayalam/about
- Caption style and weight guidance (vendor blogs, unverified numbers): https://www.opus.pro/blog/instagram-reels-caption-subtitle-best-practices , https://blitzcutai.com/blog/best-caption-style-instagram-reels-2026 , https://blitzcutai.com/blog/best-caption-fonts-reels-2026 , https://www.kapwing.com/resources/social-media-captions-styles-a-complete-guide/
- Safe zones (vendor guides; values disagree): https://www.hopperhq.com/blog/instagram-reel-size/ , https://www.trymypost.com/blog/instagram-reels-safe-zones-text-placement-2026 , https://www.krumzi.com/blog/add-captions-to-instagram-reels
- Meta India fonts (Devanagari and Bengali-Assamese only, no Malayalam found): https://about.fb.com/news/2025/11/instagram-empowers-creators-to-go-global-with-local-voice-translations-and-fonts/

## 5. Open items

- Komika Axis licence not verified (folder fetch returned 404).
- Inter, Oswald, League Spartan licences stated from knowledge, not re-checked.
- Competitor-specific font identities (Hormozi, Ali Abdaal, MrBeast, Warikoo, Tanay Pratap, Malayalam creators) were not confirmed from primary footage. Recommend a visual check of 3-5 reels per creator with a frame grab.
- Safe-zone pixel values need a phone preview or Meta's official diagram.
