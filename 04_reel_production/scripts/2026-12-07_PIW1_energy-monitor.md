# PIW1: Project Idea of the Week #1 "An ESP32 energy monitor that warns you before the bill shock"
*(Posts Mon 7 Dec. Shoot 10 Nov or 17 Nov, seated set. No demo build yet: parts only, said honestly. When Demo Build #1 exists, re-shoot as F1 result-first.)*

## SETUP AT A GLANCE
**Where:** the lab, **seated**, same chair and frame as LAUNCH1. **Plain T-shirt.**
**Frame:** head to waist, hands visible. The editor zooms in for the parts.
**Camera / light / mic:** as LAUNCH1.
**How you talk:** improv, your words. One file per piece.
**Props (used in B3):** an **ESP32 board** · a **PZEM-004T energy module with its CT clamp coil** (if we have one; otherwise any CT clamp, and say "a module like this") · your **phone** (screen off is fine). Tape over any shop labels.

```
TOP VIEW (same as LAUNCH1)
        [ lab shelves ]
              [chair]  <- YOU, parts in your lap until B3
              ~1.1 m
         [ iPhone on tripod ]
```

### SHOT LIST
| # | Shot | What happens | Length | Used in | File | Need? |
|---|---|---|---|---|---|---|
| A1 | Talking pieces B1–B5 | you say each piece | each | B1–B5 | phone names + `improv_script.md` | MUST |
| BR1 | Parts close-up | hands only, top-down 40 cm: ESP32 next to the PZEM + clamp | 4 s | B3a | PIW1_INS_parts | MUST |
| BR2 | Clamp on a wire | hands only: the CT clamp closes around **one insulated wire of an unplugged extension cord** (nothing live) | 3 s | B3a | PIW1_INS_clamp | NICE |

**Safety (say it, show it):** nothing is connected to mains on camera. Mains wiring is done only with a mentor.

---

## D0. READ THIS FIRST (plain English)
**What this reel is about:** "Project idea: an ESP32 energy monitor. It measures your home's power use live, shows the units on your phone, and warns you before the bill jumps. Level it up with an overload cut-off or a bill prediction."
**Why we're making it:** Project Idea of the Week is our main lead series (keyword PROJECT). This idea fits EEE, EC and CS (IoT + data), it solves a real problem everyone in Kerala knows (the bill shock), and it scales from basic to strong.
**Your role:** the senior who just found a great project idea and wants to give it to you.
**Length:** about 40 s. 6 pieces.

| # | Time | What you SAY (meaning in English) | How to ACT | What the viewer SEES |
|---|---|---|---|---|
| **B1** | 0–3 s | "Electricity bill shock every two months? Make that your final year project." | Eyebrows up, half smile | Hook: **BILL SHOCK = *PROJECT IDEA*** |
| **B2** | 3–7 s | "Project idea of the week: an ESP32 energy monitor. Here's how it works, and how to level it up." | Small "listen" gesture | **PROJECT IDEA OF THE WEEK** label + **ESP32 *ENERGY MONITOR*** |
| **B3a** | 7–15 s | "An energy module like this measures voltage, current, power and units. The ESP32 reads it and sends it over Wi-Fi." | Hold up the module, then the ESP32 | Pill **HOW IT WORKS** + parts close-up |
| **B3b** | 15–21 s | "On your phone you see live usage, and it warns you when this month's units cross a limit you set." | Hold up the phone | Pill **ON YOUR PHONE** + **LIVE UNITS + *ALERT*** |
| **B3c** | 21–30 s | "Level up: add a relay to cut off an overloaded socket. Or for CS teams, predict the next bill from the data." | 1 finger, then 2 | Pill **LEVEL UP** + **OVERLOAD CUT-OFF · *BILL PREDICTION*** |
| **B4** | 30–35 s | "A real problem, real data, and you can explain every block in your viva." | Calm, sure | **REAL PROBLEM. *REAL DATA.*** |
| **B5** | 35–39 s | "Want this idea for your team? Comment PROJECT." | Point down (comments) | CTA **COMMENT "PROJECT"** |
| End | 39–41 s | — | — | Logo · Learn It. Build It. Own It. · We Build It WITH Your Team · Comment PROJECT |

**Careful:** don't show anything plugged into mains. Don't say a price. Don't say "we'll make it for you": say "we'll guide your team to build it".

---

## D1. Header
```
REEL ID:       PIW1
SERIES:        PIW (Project Idea of the Week #1)     FORMAT: F2 talking + parts inserts (F1 once Demo Build #1 exists)
TARGET LENGTH: 41 s        SET: lab, seated (LAUNCH1 set), improv
HOOK TYPE:     PROBLEM-FIRST + NAME (ESP32)
KTU MOMENT:    Phase II just started: teams still finalising / upgrading topics     MONTH CTA (Dec): PROJECT keyword → consult
ONE ASK:       Comment "PROJECT" (ManyChat sends the idea sheet + consult link)
SEND TEST:     "An EEE/EC student sends this to the group: 'nammude topic ithu aakkiyalo?'"
HOOKS:         8 written · best = 11/12 · Trial variant = 10/12
GATES:         Script QA 90/100 · Ethics gate [x]
GOAL METRIC:   PROJECT comments + saves
COVER:         notebook cover "BILL SHOCK?" (D3)
CAPTION L1:    "Final year project idea: ESP32 energy monitor (EEE, EC, CS)"
HASHTAGS (≤5): #finalyearproject #esp32 #iotproject #ktu #eeeprojects
LOCATION TAG:  [office town]
```

## D1b. Control, facts and readiness
```
STATUS:        draft v1 → waiting for Shawn's approval + fact ticks       AUTHOR: Claude (Opus)
VALID UNTIL:   evergreen
TRACKING CODE: PIW1
DEPENDS ON:    ManyChat PROJECT flow live (same as LAUNCH2) + a one-page idea sheet to send (block diagram + parts list + 3 levels)
PERMISSIONS:   [x] parts only, no client project · nothing on mains on camera
```
**Fact sheet**
| # | Claim | Proof / source | OK? |
|---|---|---|---|
| F1 | KSEB bills most homes every two months | KSEB domestic bi-monthly billing. **VERIFY** (true for most domestic LT connections) | [ ] |
| F2 | A PZEM-004T-type module measures voltage, current, power and energy (units) | PZEM-004T v3 datasheet (also frequency + power factor) | [ ] |
| F3 | The ESP32 has Wi-Fi and can read the module (UART) and send data to a phone | ESP32 datasheet; common PZEM + ESP32 libraries | [ ] |
| F4 | A relay can cut off an overloaded socket | Standard design; **mains switching only with a mentor and a rated relay/contactor** | [ ] |
| F5 | Bill prediction from usage data is a fit for CS teams | Our recommendation (simple regression/time-series on logged units) | [x] |
| F6 | "We guide your team to build it" | Offer: mentoring, build WITH you, class included | [x] |
**Don't say:** prices · "readymade" · "we'll do it for you" · that it's a finished/tested product (no build yet).

## D2. HOOK block
```
HOOK TYPE:      PROBLEM-FIRST + NAME
B1 VISUAL:      seated, eyebrows up, half smile, module in your lap
ON-SCREEN TEXT: "BILL SHOCK =\n*PROJECT IDEA*"   (TXT-HOOK, 0.0 s)
SPOKEN (idea):  "Current bill kandu shock aayo? Athu thanne aakkaam ninte final year project."
MUTE TEST:      [x] text + parts carry it
SCORE:          Gap 2 · Spec 2 · Truth 2 · Fit 2 · Voice 2 · Pull 1 = 11/12
TRIAL VARIANT:  text "ESP32 PROJECT FOR EEE + EC + CS" / spoken "EEE, EC, CS: moonnu branch-num pattunna oru ESP32 project." = 10/12
```
Other hooks considered: "Ee module kond ninte veedinte current bill predict cheyyaam" (10, claim stretches) · "Plant monitoring old aayi. Ithu try cheyyu" (9, negative flip, mild dig) · "Ninte project-il real data undo?" (9) · "₹__ parts-il oru IoT project" (rejected: no verified price) · "Viva-yil 'real application?' chodichaal…" (9) · "Final year IoT idea, 3 levels" (8).

## D3. THUMBNAIL / COVER block
```
COVER TYPE:     full-screen notebook graphic, no face
COVER TEXT:     kicker "project idea of the week" · hero "BILL SHOCK?" · sticky note "ESP32 energy monitor", ticked:
                units on phone / limit alert / overload cut-off / bill prediction
FILE:           vidoes/<shoot date>/cover_PIW1.jpg
COMMAND:        pipeline/.venv/Scripts/python.exe -I pipeline/cover_notebook.py vidoes/<shoot date>/cover_PIW1.jpg --kicker "project idea of the week" --hero "BILL SHOCK?" --note "units on phone" "limit alert" "overload cut-off" "bill prediction" --tape "ESP32 energy monitor"
```

## Shot table
| Beat | Dur | Text | Overlay / insert | TRN |
|---|---|---|---|---|
| B1 | 3 s | TXT-HOOK "BILL SHOCK = *PROJECT IDEA*" | — | cut |
| B2 | 4 s | TXT-LABEL "PROJECT IDEA OF THE WEEK #1" · TXT-KEY "ESP32 *ENERGY MONITOR*" | — | fade |
| B3a | 8 s | TXT-KEY "MEASURES *POWER + UNITS*" | PILL HOW IT WORKS · INS parts 2.0→4.0 · INS clamp 5.0→6.5 | fade |
| B3b | 6 s | TXT-KEY "LIVE UNITS + *ALERT*" | PILL ON YOUR PHONE | fade |
| B3c | 9 s | TXT-KEY "OVERLOAD CUT-OFF" → "*BILL PREDICTION* (CS)" | PILL LEVEL UP | fade |
| B4 | 5 s | TXT-KEY "REAL PROBLEM. *REAL DATA.*" | — | fade |
| B5 | 4 s | TXT-CTA "COMMENT \"PROJECT\"" | — | fade |
| End | 2 s | end card v2 | — | — |

## D4. SHOOT CARD (Shawn)
```
REEL:       PIW1 · F2 · ~40 s · 20 min incl. B-roll
PROPS:      [ ] ESP32  [ ] PZEM-004T + CT clamp (labels taped)  [ ] phone  [ ] unplugged extension cord (BR2)
ORDER:      B1 (5 takes) → B2 → B3a → B3b → B3c → B4 → B5 → BR1 → BR2
SAFETY:     nothing plugged in. Say "mains work only with a mentor" if it comes up naturally
AFTER:      improv_script.md (clip N: what you said)
```

## D4b. READ MODE (meaning cues)
```
B1   [eyebrows up]        bill shock every 2 months → make it your project
B2   [listen gesture]     idea of the week: ESP32 energy monitor, how + level up
B3a  [module, then ESP32] module measures V, I, power, units → ESP32 sends over Wi-Fi
B3b  [phone up]           live usage on phone, alert past your limit
B3c  [1 finger, 2]        level up: relay cut-off for overload · CS: predict the bill
B4   [calm]               real problem, real data, you can explain every block
B5   [point down]         want it for your team? comment PROJECT
```

## D4c. AS SAID (fill in after the shoot)
| Beat | Spoken (Shawn's Manglish) | Meaning |
|---|---|---|
| | | |

## D5. PUBLISHING PACK
```
CAPTION:
  Final year project idea: ESP32 energy monitor (EEE, EC, CS)
  Veettile current use live aayi phone-il. Limit cross cheythaal alert.
  How: energy module (voltage, current, power, units) → ESP32 → Wi-Fi → phone
  Level up: overload aaya socket relay vazhi cut-off · CS teams: data vechu next bill predict cheyyu
  Real problem, real data, viva-il oro block-um ninakku explain cheyyaam.
  Ee idea ninte team-nu venel "PROJECT" comment cheyyu 👇 (block diagram + parts list DM-il)
  #finalyearproject #esp32 #iotproject #ktu #eeeprojects
ALT TEXT:       "Shawn holding an ESP32 and an energy meter module, explaining a final year project idea"
COVER:          cover_PIW1.jpg
MANYCHAT:       keyword PROJECT → DM: idea sheet (block diagram, parts list, 3 levels) + "free 1-hr team consult" booking link
PINNED COMMENT: "Comment PROJECT, block diagram + parts list DM cheyyaam. Ethu branch aanu? 👇"
TRIAL REEL:     [x] yes, variant from D2
STORY PLAN:     +1 h: poll "Ee idea ninte team-nu?" Yes 🔥 / Need something else
POST SLOT:      Mon 7 Dec, 7–8 pm
PREPARED REPLIES:
  "price?"              → "Free 1-hr consult-il ninte scope nokki parayaam. DM cheyyu 🙌"
  "readymade kittumo?"  → "Illa bro, readymade illa. Ninte team-nte koode build cheyyum, ningal padikkum 🙌"
  "CS-kku pattumo?"     → "Pattum: bill prediction + dashboard part CS-kku perfect aanu"
  "mains safe aano?"    → "Mains part mentor-nte koode maathram. Module + clamp kond safe aayi measure cheyyaam"
REPURPOSE:      [ ] idea sheet = lead magnet PDF · [ ] F1 re-shoot when Demo Build #1 exists
```

## Editor block (for pipeline/reel_assemble.py)
```yaml
# Seated improv set, LAUNCH1 v2 style. After the shoot: rename PIW1_B1..B7_KEEP (B1,B2,B3a→B3,B3b→B4,B3c→B5,B4→B6,B5→B7).
id: PIW1
length_s: 41
source_dir: vidoes/2026-11-10/
progress_bar: false
beats:
  - id: B1
    clip: {file: PIW1_B1, in: auto, out: auto, crop: 115, jumpcut: false}
    transition_in: TRN-CUT
    text: [{style: TXT-HOOK, words: "BILL SHOCK =
*PROJECT IDEA*", in: 0.0, out: 3.0, y: 1000}]
    sfx: SND-HIT
  - id: B2
    clip: {file: PIW1_B2, in: auto, out: auto, crop: 115, jumpcut: false}
    transition_in: TRN-FADE
    text:
      - {style: TXT-LABEL, words: "PROJECT IDEA OF THE WEEK #1", in: 0.2, out: 4.0, y: 1050}
      - {style: TXT-KEY, words: "ESP32
*ENERGY MONITOR*", in: 0.8, out: 4.0, y: 1200}
  - id: B3
    clip: {file: PIW1_B3, in: auto, out: auto, crop: 115, jumpcut: false}
    transition_in: TRN-FADE
    overlays: [{type: OVL-PILL, words: "HOW IT WORKS"}]
    text: [{style: TXT-KEY, words: "MEASURES
*POWER + UNITS*", in: 0.8, out: 7.0, y: 1200}]
    inserts: [{file: PIW1_INS_parts, at: 2.0, dur: 2.0}, {file: PIW1_INS_clamp, at: 5.0, dur: 1.5}]
    sfx: SND-POP
  - id: B4
    clip: {file: PIW1_B4, in: auto, out: auto, crop: 115, jumpcut: false}
    transition_in: TRN-FADE
    overlays: [{type: OVL-PILL, words: "ON YOUR PHONE"}]
    text: [{style: TXT-KEY, words: "LIVE UNITS
+ *ALERT*", in: 0.8, out: 5.5, y: 1200}]
    sfx: SND-POP
  - id: B5
    clip: {file: PIW1_B5, in: auto, out: auto, crop: 115, jumpcut: false}
    transition_in: TRN-FADE
    overlays: [{type: OVL-PILL, words: "LEVEL UP"}]
    text:
      - {style: TXT-KEY, words: "OVERLOAD
*CUT-OFF*", in: 0.8, out: 4.3, y: 1200}
      - {style: TXT-KEY, words: "*BILL PREDICTION*
(CS TEAMS)", in: 4.6, out: 8.5, y: 1200}
    sfx: SND-POP
  - id: B6
    clip: {file: PIW1_B6, in: auto, out: auto, crop: 115, jumpcut: false}
    transition_in: TRN-FADE
    text: [{style: TXT-KEY, words: "REAL PROBLEM.
*REAL DATA.*", in: 0.3, out: 4.5, y: 1200}]
  - id: B7
    clip: {file: PIW1_B7, in: auto, out: auto, crop: 115, jumpcut: false}
    transition_in: TRN-FADE
    text: [{style: TXT-CTA, words: "COMMENT \"PROJECT\"", in: 0.5, out: 4.0, y: 1010}]
music: {file: null, level_lufs: -26, duck_db: 4}
end_card: {show: true, line2: "Learn It. Build It. Own It.", line3: "We Build It WITH Your Team", line4: "Comment PROJECT"}
export: {lufs: -14, fps: 30, safe_bottom: 1480}
```

## D6. Result log
```
Link: ____ · Views __ · 3-s hold __% · Avg watch __ s · Saves __ · Sends __ · PROJECT comments __ · DMs → consults __
```

## Script QA (90/100)
Truth 27/30 (F1–F4 to tick; no build yet, said honestly) · Voice 18/20 · Hook & structure 18/20 · Duration & clarity 13/15 (B3c is the longest) · Ask & caption 14/15
**Ethics gate:** [x] "readymade" only in the reply that says we don't do it · [x] no fake numbers/prices · [x] no client shown · [x] no film clips/audio · [x] no colleges/teachers/competitors named · [x] safety: nothing on mains on camera
