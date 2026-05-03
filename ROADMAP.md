# Mighty Mussels Scorecard — Roadmap

**Current version:** v79 (`180e5d6`, 2026-05-02)
**Status as of:** 2026-05-02. **Season record: 2-3** (W vs Hot Rods, L vs Thunder, W vs Bulls, L vs Devil Rays mercy, L vs Hurricanes mercy). Two heavy game-day shake-downs (5/1 Devil Rays, 5/2 Hurricanes) drove ~14 versions covering: skip-batter purgatory + out-of-order insert (v67-68), pinch-runner with proper bi handling (v69), Firebase sync guards both directions (v70/v72/v73), pitch-rest off-by-one fix per LMLL Rule C.4 (v75), view-only mode for finalized games (v75), LMLL rules tab verbatim with search + accordion (v75), pitcher attribution + pc-as-authoritative (v76), BIP X always appended (v77), SB stat team filter (v78), opp picker full lineup view + insert/remove per row (v79). Next game: e10 Tin Caps May 7.

## Newly identified items from 5/1 + 5/2 game-day testing

| Priority | Item | Notes |
|---|---|---|
| 📋 | **Pitcher attribution UX during live game** — When a manager changes the active pitcher mid-game (without going through the pitcher switch modal), `fa[inn].P` doesn't always update. The plays-page banner can lag behind reality. v76 fixed the rendering side; the data-entry side still needs an audit. | Real example: e8 B4 had Hunter pitching the whole inning but `fa[4].P` stayed on Miles (the planned pitcher) until manually corrected. Investigate where the user's "switch pitcher" action should sync to `fa`. |
| 📋 | **Visual mismatch when `pitches.length < ab.pc`** — Plays page shows e.g. `B B (2)` but `ab.pc=3`. v76 added a `(Np)` fallback for empty `pitches`, but partial sequences (`pitches=['B','B']` + `pc=3`) still show the shorter count. Decide: prepend filler / show Math.max(pitches.length, ab.pc) / leave as-is. | Comes up whenever a retro patch bumps `pc` without adding to the sequence. |
| 📋 | **Live entry of opp ABs without alu** — When opp lineup is empty (e.g. after a wipe) and the user adds opp batters mid-game via the picker, the on-the-fly add path should match the v79 picker affordances (insert/remove). Currently the form just appends. | Verify after a sandbox run-through. |
| 📋 | **`pscored` should store `bi` not just `name`** — When opp lineup gets renamed (e.g. via the placeholder rename in v71), historical `pscored` entries on past ABs reference stale names. The plays-page sub-line displays the stored name regardless of current lineup. | Schema change: push `{bi, team, name}` objects so the renderer can resolve to the current name. Backward-compat: keep accepting strings. |
| 📋 | **CS records don't credit pitcher IP_outs in `recalcPitcherStats`** — Live `confirmCS` stamps `cs.pitcher` (v65 work), and the existing CS-handling block in `recalcPitcherStats` credits the pitcher's `ip_outs`. But the partial recalc paths in standalone patch scripts don't replicate this — Hunter B4 audit was off by 1 IP_out for this reason on Paxton's e9 phantom AB. Acceptable for now since opp-pitcher detail is low-priority. | Cosmetic; revisit only if opp pitcher box scores become important. |
| 🐞 | **Pinch-run swap-back display verification** — User reported in e8 that only one pinch-run line was visible in plays. Both records ARE in Firestore (T3 #25 Bodhi-for-Malcolm + T3 #26 Malcolm-for-Bodhi after fix). After v79 + cache refresh, both should render — but never confirmed visually on the user's phone. | Re-verify next time user opens e8 plays tab. |
| 💡 | **Auto-detect run cap (6-run rule)** — When a half-inning hits 6 runs, prompt "End half-inning? (run-limit cap)". Manager currently has to manually advance. | Came up in T2 + T3 of e9 where both halves hit 6 and ended via cap. |
| 💡 | **Force-out RBI awareness** — User wasn't sure when RBI is credited on a force play. Per LL Rule 9.04 (and per LMLL B), runs scoring on a single force out *do* credit RBI; only force-double-plays exclude RBI. Worth surfacing this in the post-AB result modal so the user knows whether to bump RBI. | Could be a tooltip on the RBI input. |
| 💡 | **Opp pitcher pitch-count display** — We track opp pitcher totals via `ab.pitcher` attribution (e9 Greg/Paxton/Gold), but there's no clear box-score view showing them per-pitcher per-game. | Side-tab on the Pitchers screen, similar to ours. |

## Status Key
- ✅ Done
- 🔄 In Progress / Needs Verification
- 📋 Planned (next release)
- 💡 Idea / Future
- 🐞 Known Bug

---

## 🏟 Game-day readiness

### ✅ All v40 must-haves and nice-to-haves shipped (v65)

| # | Item | Status |
|---|------|--------|
| **A1** | Edit-AB RBI doesn't rebuild G.runs / score | ✅ v65 — RBI delta applied to team total + inning total; A.gameResults synced |
| **B1** | Native `confirm()` / `prompt()` cleanup | ✅ v65 — `confirmModal` and `promptModal` helpers; in-game dialogs replaced |
| **B2** | Walk-off / end-of-last-inning PROMPT | ✅ v65 — both top-of-last and bottom-of-last walk-off paths covered |
| **B3** | Lineup tab — hide ✕ delete behind Edit toggle | ✅ v65 — opp lineup ✕ only shows when in edit mode |
| **B4** | "Saved roster — not in lineup yet" section | ✅ v65 — Lineup tab shows OPP_ROSTERS players not yet added with + Add |
| **B5** | Per-CS pitcher attribution | ✅ v65 — `cs.pitcher` stamped at log time |
| **A2** | End-to-end sandbox test before next game | 🔄 PENDING — needs to be run by user |

### Remaining: just the sandbox smoke test

The only thing left for game-day readiness is a full sandbox game run-through to verify no regressions from the recent refactors (Plays log 4-col, opp picker overhaul, font switch, ID collision fix, all the v65 modals).

Suggested test sequence:
1. Start test sandbox
2. Build lineup (should see new Saved-roster + Add option for known opponents)
3. Confirm opp lineup popup ("Pre-enter" / "Add live")
4. Log a few pitches → result → switch batter (modal: "Switch batter?")
5. Try out-of-order: mid-AB switch via selBat
6. Steal + CS, verify sub-lines on Plays log
7. Edit an AB (✎), change RBI by 1, confirm score updates
8. Swap two ABs (⇄)
9. Delete an AB
10. End an inning, switch sides
11. Mark a player DNP — should show modal
12. Call game from gear menu

If any step misbehaves, surface the issue.

### 💡 Cosmetic / future (parked)

| # | Issue | Why deferred |
|---|------|---|
| C1 | Pitchers tab — collapsible pitch-type breakdown | Big UX redesign; current works |
| C2 | Backfill pitcher stamps for e2 / e4 | Old games, plays log transitions are cosmetic |
| C3 | ⚠️ Yellow-! error indicator on Plays log | In-AB errors don't surface visually; standalone do as sub-lines |
| C4 | Per-fielder error count column on Box | Already shown per-error in Fielding Errors panel |
| C5 | Retro scorecard (parked as WIP) | See `RETRO_SCORECARD_TODO.md` for the 14-item list |

---

## v40 — Next Up (queued for next session)

User feedback from 2026-04-26 testing. All items below are confirmed for implementation.

### 🔥 High priority

| # | Issue | Notes |
|---|------|-------|
| **A** | **Edit-AB: RBI change must rebuild G.runs / G.hs / G.as** | Currently editing an AB's RBI doesn't update the team score or the `↳ Scored:` sub-line. Score quietly goes out of sync. Fix: when Edit-AB saves, do a full rebuild from `G.abs` (clear `G.runs`, walk every AB, re-derive score and inning totals). |
| **B** | **Per-CS pitcher attribution** | Stamp `cs.pitcher` and `cs.pitcherTeam` at `confirmCS` time. Update `recalcPitcherStats()` to use `cs.pitcher` directly instead of the heuristic of "last AB pitcher in the half." |
| **C** | **Backfill pitcher stamps for e2 (Hot Rods) and e4 (Thunder)** | Write a one-time eval that walks each game's ABs and stamps `ab.pitcher` based on the documented inning ranges (Brody/Ethan/Ezra for e2, Felix/Land/Gutmann/Stabert for e4). Cosmetic but completes the Plays log transition lines for those games. |
| **D** | **Pitchers tab redesign — collapsible pitch breakdown** | Each pitcher row: `#22 Brody Steinberg — 35` (jersey, name, dash, pitch count). Click row to expand a panel showing pitch-type breakdown: <ul><li>Strikes (total): swinging / looking / foul tip / foul ball (separate counts)</li><li>Ball in play</li><li>Balls</li><li>HBP</li></ul> Requires splitting the existing `p.fo` counter into `p.fo` (foul ball) and `p.ft` (foul tip). Update `pAdd()` and `recalcPitcherStats()` accordingly. |
| **E** | **Lineup tab cleanup — hide X delete behind Edit toggle** | Currently the ✕ delete button is always visible on each row. Should only appear when "Edit" is toggled on, for BOTH our team and opp team. Existing `_luEdit` state already controls reorder buttons; extend it to control X visibility too. |
| **F** | **Lineup tab — show "Saved roster — not in lineup yet" section for opp team** | Below the entered opp lineup, render a list of saved roster players (from OPP_ROSTERS) that aren't yet in alu. Each row gets a + button to add them to the lineup. Then user uses existing ↑/↓ arrows to position them. Replaces the v40-original "Pre-fill from saved roster" item but in a more useful, in-context form. |
| **G** | **Replace remaining native confirm() / prompt() dialogs** | Spots: `selBat()` "Switch? Pitches lost", `oppbatEndOrder()` confirm, `runnerM()` prompt for adding a runner, `markDNP()`, recalc stats confirm, addTaxi name prompt, addGB late-arrival prompts, Edit-AB / Swap-AB / Delete-AB confirms. Build a generic `confirmModal(title, body, onYes, onNo)` and `promptModal(title, label, onSubmit)` to replace them all. |

### 📋 Lower priority

| # | Issue | Notes |
|---|------|-------|
| H | **Walk-off / end-game PROMPT (not auto-end)** | When conditions look like the game should be over, pop up a confirm modal: "Home leads — call it now?" with Yes / Keep playing. Triggers: (a) top of last inning ends with home leading, (b) home takes the lead in bottom of last inning. User confirms or dismisses. NOT auto-end — too many ways game state can be temporarily wrong. |
| I | **⚠️ Yellow-! error indicator on Plays log AB rows** | Small ⚠️ icon next to the result badge when the AB had an error logged via m-play err-sec. Tap → popup with position, type, description. Extends standalone-error sub-lines to in-AB errors. |
| J | **Per-fielder error count column on Box** | Box "Fielding errors" panel already shows each error individually — a count column on the batting table would be cosmetic. Deferred unless requested. |

### ✅ Recently Completed

**v39 (today, 2026-04-26):** Plays log redesign + post-Lugnuts test fixes
- Plays log: 4-column layout (# | batter | pitches | result), no more overflow
- Plays log: indented sub-lines for steals, CS, runs scored
- Edit-AB modal (✎) — change batter, result, RBI, notation; or delete
- Swap-AB modal (⇄) — fix out-of-order batting after the fact
- Placeholder names: `(Leadoff)`/`(Cleanup)`/`(N-hole)` format, light red, propagate on edit
- Box score: jersey # ahead of name; new PA column
- "Call game" relocated to bottom of Rules tab (out of accidental-tap zone)
- PA counter in matchup bar and bat list
- Skip-this-batter for our team (bathroom kid scenario)
- Roster-as-menu opp picker (full hardcoded roster shown by default with jersey input per row)
- Opponent lineup choice popup ("Pre-enter" vs "Add live as they bat")
- Resume flow goes straight to scorecard (no more lineup re-confirm)

**v35-v38:**
- Pre-plan fielding spreadsheet/grid view (positions × innings, bench row)
- Pre-plan fielding by inning (Field tab inning selector)
- Standalone error tracking ("⚠️ Err" button + modal, plays log integration)
- Stolen base checkbox UI (multi-runner advances, no stealing home)
- Auto-out batter (LL Rule 4.04(h) — CBO mid-game removal)
- Per-AB pitcher stamp — mid-inning changes now tracked, plays log shows transitions
- Pitch threshold strict-equality bug fix (missed warnings on count jumps)
- Threshold modal queue (no more overwriting)
- Retroactive pitcher recalc + button

---

## v36+ — Feature Gaps

| # | Feature | Priority | Notes |
|---|---|---|---|
| 1 | **Retroactive game logging UI** — a "log a past game" mode that doesn't enforce live-game timing/Firebase sync. Should let you paste linescore, pick pitchers per inning, and step through ABs without alerts firing. | 💡 | Currently requires preview-eval scripting. A scorecard-style entry form would cut entry from 90+ minutes to ~10 minutes. |
| 2 | **Pitch reconstruction from result** — when no pitch sequence is known (paper scorebook entry), default to sensible pitch synthesis (e.g. K = 3 strikes, BB = 4 balls, BIP = 1 strike) so totals match without manual eval. | 💡 | Goes hand-in-hand with retroactive logging UI. |
| 3 | **Game data export / paper scorecard reprint** — print-friendly single-page summary so a parent or coach can reconstruct the game from the app. | 💡 | Would have prevented the e2 retroactive replay. |
| 4 | **Rest day calendar** — "Eligible again: Apr 26" per pitcher based on pitch count rules. | 💡 | |

---

## Core Scoring & At-Bat

| Feature | Status | Notes |
|---------|--------|-------|
| Ball/Strike/Out counter | ✅ | |
| Pitch sequence display (real-time) | ✅ | v15 — `renderCB` ID mismatch fix |
| Previous AB pitch sequence (faded) | ✅ | v14 — `G.lastABPitches` |
| All result buttons (1B/2B/3B/HR, outs, FC, DP, etc.) | ✅ | |
| FC base movement (runner picker + batter to 1B) | ✅ | v34 |
| Undo last pitch | ✅ | |
| Undo last AB | ✅ | |
| Runner advancement (SB, CS, WP, etc.) | ✅ | |
| Stolen base checkbox UI (multi-runner) | ✅ | v35 — checkboxes for 1st→2nd, 2nd→3rd; no stealing home |
| Auto-out batter (LL 4.04(h)) | ✅ | v35 — for player removed from CBO mid-game |
| CS credits `ip_outs` to pitcher | ✅ | v34 |
| Auto-advance to next batter | ✅ | |
| Multi-runner scoring on short hits | ✅ | v34 |
| AB flow tolerates `cbi=-1` with pitches in buffer | ✅ | v32 |

---

## Opponent Batter Management

| Feature | Status | Notes |
|---------|--------|-------|
| On-the-fly opponent batter picker | ✅ | v32, enhanced v34 |
| **Auto-open picker** for each opponent AB | ✅ | v34 — opens at game start, after each AB, and on tab return |
| Ghost slots (Leadoff Hole, Cleanup Hole, etc.) | ✅ | v34 |
| Skip batter (bathroom, late arrival) | ✅ | v34 — auto-clears on lineup wrap |
| End of order → cycle lineup | ✅ | v32 |
| Change / skip batter after lineup locked | ✅ | v34 |
| Substitute player into locked lineup | ✅ | v34 |
| Out-of-order batting (our team) | ✅ | v34 — selectable styling + instruction banner |

---

## Pitcher Tracking & Limits

| Feature | Status | Notes |
|---------|--------|-------|
| Pitch count per pitcher | ✅ | |
| Pitch type breakdown (SW/LK/FO/BA/BIP) | ✅ | |
| HBP counter per pitcher | ✅ | v10 |
| **21/36/40/51/65/66-pitch threshold popups** | ✅ | v15 fix |
| **75-pitch hard block (our pitcher)** | ✅ | v14/v15 |
| **75-pitch notify (opponent pitcher)** | ✅ | v14/v15 |
| **3-HBP forced removal (both teams)** | ✅ | v14 |
| Threshold checks on ALL AB outcomes | ✅ | v13/v14 |
| Override rule violation option | ✅ | v14 |
| 75-pitch "Finish Batter" flow | ✅ | v16 |
| RBI buttons capped to runners+1 | ✅ | v16 |
| LLHR result | ✅ | v16 |
| Catcher 4+ innings → cannot pitch warning | ✅ | v16 |
| Pitcher 41+ pitches → cannot catch warning | ✅ | v16 |
| Pitching change UI | ✅ | |
| Innings pitched tracking | ✅ | Includes CS outs as of v34 |
| Per-AB pitcher stamp | ✅ | v36 — `ab.pitcher` + `ab.pitcherTeam` set in `finAB` |
| Retroactive pitcher recalc | ✅ | v36 — `recalcPitcherStats()` + Pitchers tab button |

---

## Fielding & Lineup

| Feature | Status | Notes |
|---------|--------|-------|
| 9-player field positions | ✅ | |
| 10-player with RCF (was 4OF) | ✅ | v10/v11 |
| CF left of center / RCF right of center | ✅ | v11 |
| RCF counts in innings-per-player | ✅ | v10 |
| Innings per player tracking | ✅ | |
| Minimum play rule warnings | ✅ | Non-blocking modal as of v34 |
| Catcher pitch-count limit | ✅ | |
| DNP / availability tracking | ✅ | |
| "Remove" button (renamed from DNP) | ✅ | v16 |
| Pitching change → prompt fielder update | ✅ | v16 |
| Block pitch logging until pitcher assigned | ✅ | v16 |
| In-game lineup edit mode (reorder, late arrivals) | ✅ | v31 |
| Mid-inning pitcher tracking | ✅ | v36 — per-AB pitcher stamp + plays log transitions |

---

## Field Graphic

| Feature | Status | Notes |
|---------|--------|-------|
| Solid green wide-angle field | ✅ | v22+ restoration, Apr 10 |
| Position labels (P, C, 1B…) in dark boxes | ✅ | `6ccd8f9` |
| Labels turn gold + show first names when assigned | ✅ | `a403381` |
| Big gold runner circles centered on bases | ✅ | `180a1c3` |
| Visible dirt around bases + mound | ✅ | `6ccd8f9` |
| Home plate point faces down | ✅ | `a341125` |

---

## Matchup Bar

| Feature | Status | Notes |
|---------|--------|-------|
| Our pitcher name + pitch count | ✅ | |
| Opponent batter name | ✅ | |
| Opponent batter jersey number | ✅ | v10 |
| HBP count shown on pitcher | ✅ | v10 |
| Opponent batter on-the-fly add | ✅ | v32 — `m-oppbat` modal |

---

## Game Management

| Feature | Status | Notes |
|---------|--------|-------|
| Home/Away team setup | ✅ | |
| Inning-by-inning scoring | ✅ | |
| Compact line-score strip on top of all tabs | ✅ | v17 |
| Box score with totals row | ✅ | v16 |
| Plays log — single linear stream | ✅ | v31 (replaced nested half-innings) |
| Mercy rule (10-run) | ✅ | |
| 6-run half-inning rule | ✅ | |
| Call game (time / darkness) | ✅ | v34 — secondary confirmation |
| 4-inning game support | ✅ | v37 — per-event Innings selector; mercy + chkFW scale |
| Error / fielding misplay tracking | ✅ | v37 — in-AB and standalone errors; plays log shows them |
| Pre-plan fielding by inning | ✅ | v37 — Field tab inning selector with LIVE badge |
| Pre-plan fielding grid view (positions × innings) | ✅ | v38 — full game script on one screen, tap any cell to assign |
| End game | ✅ | |
| Share/Export | ✅ | |
| Game result badge only on `final===true` | ✅ | `586e418` |
| Resume modal (Resume / Start fresh / Cancel) | ✅ | `64ee616` |

---

## PWA / Technical

| Feature | Status | Notes |
|---------|--------|-------|
| Installable PWA | ✅ | |
| Service worker cache (v36) | ✅ | sw.js |
| Offline play | ✅ | |
| localStorage persistence | ✅ | |
| **Firebase / Firestore sync** | ✅ | v18–v20, project `diamond-statz` |
| **Sync guard** (blank-state overwrite prevention) | ✅ | v34 — `fbSaveGame()` checks remote ABs before push |
| Multi-device coherent state | ✅ | |
| `fbSaveGame()` strips `undefined` fields | ✅ | v34 — JSON round-trip |
| Test Sandbox (🧪 fake game) | ✅ | `49f59f0` — isolated from real W-L |
| Wipe test data button | ✅ | |
| GitHub Pages deployment | ✅ | snppr212/scorecard |

---

## Documentation

| Doc | Status | Notes |
|---|---|---|
| `FIELD_TRIAGE.md` (game-day quick ref) | ✅ | v30 — needs version bump from v30 → v39 references |
| `CHANGELOG.md` | ✅ | Updated through v39 |
| `ROADMAP.md` | ✅ | This file (v40 plan + crazy ideas) |

---

## Potential Future Enhancements (long-tail)

| Feature | Status | Notes |
|---------|--------|-------|
| Rest day calendar (eligible-to-pitch dates) | 💡 | "Eligible again: Apr 26" |
| Print-friendly scoresheet | 💡 | See v36#3 |
| Retroactive game logging UI | 💡 | See v36#1 |
| Photo capture for lineup card | 💡 | |
| Push notifications for game day | 💡 | |
| Season stats aggregation | 💡 | |
| Email/text game summary | 💡 | |
| Pitch reconstruction from results | 💡 | See v36#2 |

---

## 🚀 Crazy ideas — long-term moonshots

These are wild but plausibly amazing if we ever wanted to push the app from "great game-day tool" to "the LL scorekeeper that other coaches notice from across the dugout."

### 🎯 User-prioritized for v41+

After 2026-04-26 review, these moved up from "moonshot" to "yes when ready":

| Priority | Idea | User notes |
|---|------|-----------|
| ✅ **v41 SHIPPED** | **Print-friendly retro scorecard export** | Done in d4510ba. Box tab → "📋 Open scorecard" → cream/serif press-box style with diamond-per-AB, red-path advance lines, totals, pitching summary. Print button + `@media print` rules. |
| ✅ **v41 SHIPPED** | **Season aggregation** — per-player BA/OBP/SLG/ERA/IP/K/BB across all games | Done in 3e48091. Home screen "📊 Season Stats" button opens an aggregation screen pulling all finalized Firebase games. Batting + pitching tables sorted by BA / IP. Auto-outs excluded. |
| **📋 v42** | **AI-generated game recap** | Tap a button at end of game → narrated paragraph. **Append next 2-3 upcoming events** (practices/games — pull from `A.schedule`) with times and locations. So the email reads like a wrap-up + a coach's reminder. |
| **💡 v42+** | **Live spectator link** | Parked behind "complete a clean game first." Once we know the data is reliable end-to-end, expose a read-only URL. |
| **💡 future** | **Inning start/end timestamps** | If easy to slot in. Stamp `inn.startTs` / `inn.endTs` automatically when half-inning transitions fire. Don't need a visible 1:45 countdown — just nice-to-know data. |
| **💡 future** | **Pitch-count progress bar** | Small visual bar in the matchup bar (or pitcher card) showing distance to 75. Replaces the text projector idea. Maybe color-coded: green / amber at 40 / red at 65 / pulsing red at 75. |

### ⏸️ Parked until "clean game" milestone

| Idea | Why parked |
|---|---|
| **Pitch quality tagging** — high / outside / non-competitive / etc. | "Not ready to even try that until we can make it through a game." Save for after v40-v41 polish. |
| **Voice input for plays** | Same — wait for clean baseline. |
| **Photo → OCR scorecard import** | Same. |

### Hands-free / faster input

| # | Idea | Why it's cool | Effort |
|---|------|----------------|--------|
| 1 | **Voice input for plays** — "Hunter, single to left field" → app parses and logs the AB. "Brody, ball" → adds a ball. | Hands stay on the dugout fence. Zero taps in clean games. Web Speech API exists, ML parser fits in ~100 lines. | Medium-high |
| 2 | **Photo of paper scorecard → OCR import** | Coach brings a printed scorebook, snaps a pic, the app extracts batters / results / pitch counts automatically. Saves 90+ minutes per retroactive game vs. preview-eval scripting. | High (needs vision model API) |
| 3 | **One-tap "no pitch / no swing" auto-rules** — based on count and result, infer the pitch sequence (BB = ball, ball, ball, ball; K-swinging = whatever's needed). | Lowers the cognitive load when you can't keep up with pitches in chaotic moments. | Low |

### Sharing & spectator experience

| # | Idea | Why it's cool | Effort |
|---|------|----------------|--------|
| 4 | **Live spectator link** — read-only URL parents/grandparents can watch in real time. Score, current AB, runners on base, last 5 plays. | Grandparents who can't make it to the game can follow along. Other parents in the stands stop bothering you for the score. | Medium (Firestore listener + a simple read-only HTML view) |
| 5 | **AI-generated game recap** — at end of game, tap "Generate recap" → "The Mussels battled back from a 3-0 deficit. Hunter Bresson's clutch 2-run single in the 5th tied the game; Ezra Kalman shut the door with 5 strikeouts over 2.2 innings to seal the win." | Auto-narration. Send it to the team email list. Kids love seeing their names in the recap. | Medium (LLM API call with the AB log) |
| 6 | **Email/text summary auto-send** | Tap End Game → "Send to team?" → blast a clean summary to the team email/SMS list. | Low-medium |

### Pitcher management (you'd genuinely use this)

| # | Idea | Why it's cool | Effort |
|---|------|----------------|--------|
| 7 | **Pitch-count projector** — "Brody at 41p — projected to hit 75 in ~7 more pitches at his current rate." Live in the matchup bar. | Lets you plan a substitution before you're in trouble. | Low |
| 8 | **Rest-day calendar** — shows who's eligible to pitch when, days out from the next game. "Eligible again: Tuesday." | Already on the long-tail list but worth highlighting. End-of-season pitch-count compliance is a real LL headache. | Medium |
| 9 | **Multi-game pitch-count panel** — at game-create, see each pitcher's last 7 / 14 days of pitches. Color-coded availability. | Makes the rest-day calendar predictive: "Don't start Hunter today, he's hit 2 days max already this week." | Medium |

### Stats & history

| # | Idea | Why it's cool | Effort |
|---|------|----------------|--------|
| 10 | **Season aggregation** — per-player stats across all games (BA, OBP, SLG, ERA, IP, K, BB, HBP). | The real stat sheet at end of season. Currently we have per-game only. | Medium (just sum across games in `A.gameResults`) |
| 11 | **Achievement / milestone notifications** — "🎉 Hunter's first triple of the season!" toast at end of inning. "Brody's 100th career strikeout!" | Kids LOVE this. Print achievements at the end-of-season banquet. | Low-medium |
| 12 | **Player charts** — Hunter's hits per game over time, batting average trend, pitch count by week. Visual. | Helpful for end-of-season parent meetings or college recruiting in years to come. | Medium (Chart.js or pure SVG) |
| 13 | **Side-by-side game compare** — pick two games, see hits/runs/pitchers/etc. side by side. | "Why did we beat Hot Rods 6-4 but lose to Thunder 5-2?" Lets you spot patterns. | Low-medium |

### Risk management & game-day

| # | Idea | Why it's cool | Effort |
|---|------|----------------|--------|
| 14 | **1:45 time-limit countdown** — visible clock that turns amber at 1:30 and red at 1:40. Reminds you when "no new inning" rule kicks in. | LL Rule per Rules tab. Right now it's manual / not tracked. | Low |
| 15 | **Lightning / weather alert** — pull from a weather API on game start, warn if storms within 30 mi. | Safety. Real coaches get this from MyRadar. We could surface it inline. | Medium |
| 16 | **6-run rule auto-detection** — when a half-inning hits 6 runs, automatic "End half-inning?" prompt. Currently the rule exists but the user enforces it. | Low effort, big game-day win. | Low |

### UI delight

| # | Idea | Why it's cool | Effort |
|---|------|----------------|--------|
| 17 | **Apple Watch quick-glance score** — companion app or web shortcut showing the current score and AB. | Coach with watch can score without phone in hand. | High (separate dev) |
| 18 | **Player avatars / photos** | Tap a player → small face on their card. Personalizes the app. | Low-medium |
| 19 | **Animated pitch trajectories** on the field SVG — pitches show as ghost lines, fielding plays show as arcs. | Eye candy but kids LOVE it during reviews. | High |
| 20 | **Walk-up music / fun facts per kid** — coach mode shows "Hunter walks up to Eye of the Tiger" or "Brody loves dinosaurs". | Pure delight, no stats value. Worth it to make the kids feel seen. | Low |

### Coach intelligence

| # | Idea | Why it's cool | Effort |
|---|------|----------------|--------|
| 21 | **Defensive shift suggestions** — based on opp batter handedness + history, recommend infield/outfield positioning. | Proper LL teams already do this informally. Auto-suggest is genuinely useful. | High |
| 22 | **Substitution rule tracker** — re-entry rules, courtesy runners, etc. The app warns "X re-entered already, can't sub back in." | Catches rule violations before umps do. | Medium |
| 23 | **Tournament bracket support** — playoff-style scheduling with bye/seeding/single-elimination. | When you make playoffs, you'd love this. | Medium-high |
| 24 | **Scout mode** — quickly observe an opposing team in another game and capture their batters, pitchers, tendencies for next time we play them. | Some coaches do scouting trips. App makes it 10x faster. | Medium |

### Tongue-in-cheek but possible

| # | Idea | Why it's fun |
|---|------|--------------|
| 25 | **AI coach tactical suggestion** — "Bring in Ezra to face #5; he's 0-for-3 against righties this season." | Modern baseball is moneyball. Why not LL? Mostly for fun though. |
| 26 | **Predict-the-pitch mini-game for kids in the stands** | Pitch comes in, kid taps "ball/strike" on a tablet, gets points. Engagement. |
| 27 | **End-of-game automated highlight reel from photos** — if the team takes photos during the game, the app picks the 5 best moments + score. | Long shot. Probably too ambitious. |

---

## Known Issues / Needs Verification (carryover)

| Issue | Status |
|-------|--------|
| 40-pitch popup verification in real game | ✅ Confirmed v15 fix; verified live in `e2` |
| Undo pitch across AB boundary edge cases | 🔄 Monitor |
| Native `confirm()`/`prompt()` dialogs still used in a few spots | 📋 See v35#1 |
