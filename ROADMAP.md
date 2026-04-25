# Mighty Mussels Scorecard — Roadmap

**Current version:** v33 (`ff4641f`, 2026-04-11)
**Status as of:** 2026-04-11, after retroactive Mussels 6 – Hot Rods 4 logging

## Status Key
- ✅ Done
- 🔄 In Progress / Needs Verification
- 📋 Planned (next release)
- 💡 Idea / Future
- 🐞 Known Bug

---

## v34 — Priority Bugs (surfaced during Hot Rods retroactive replay)

These are the things that bit us today during the retroactive replay of `e2`. Ordered by impact on a live game.

| # | Issue | Priority | Notes |
|---|---|---|---|
| 1 | `chkFW()` schedules a native `alert()` via `setTimeout(..., 300)` at start of inn 4. The blocking alert pops *after* the eval/render returns and freezes the renderer; subsequent taps appear to do nothing. | 🐞 High | `index.html:1436`. Replace with non-blocking toast/modal so it doesn't stall the UI mid-game. Same pattern in `chkPitcherRest` (`index.html:1372-1377`). |
| 2 | Multi-runner scoring on short hits is impossible — `advanceWithRBI` only advances each runner by `adv` physical bases. A single with R2+R1 should be able to score R2 (with hold or read), but app forces R2 to 3B. Today: Bodhi T2 2B (2 RBI) and Sav B4 2B (2 RBI) had to be manually patched via eval. | 🐞 High | `index.html:1297-1315`. Need a "extra base for R2/R3?" prompt or per-runner advance picker. |
| 3 | `confirmCS()` removes the runner and increments `G.outs` but **does not** increment `ip_outs` for the current pitcher — caught stealing outs vanish from IP totals. | 🐞 High | `index.html:1467-1473`. One-line fix: `if(p)p.ip_outs++;`. Affects every CS we log going forward. |
| 4 | **FC** result doesn't advance bases. Brody T2 FC 5u left bases unchanged — had to manually move runners. | 🐞 Medium | `finAB` treats FC as an out but skips base movement. Needs runner-out picker (which base is the lead out at?) and batter-to-1B advance. |
| 5 | Mid-inning pitcher change tracking — `G.fa[]` records who was pitching at the *start* of an inning, not all pitchers within it. T1 Hot Rods had Livingston→Van Dyke mid-inning; only Livingston shows in the inning slot. | 🐞 Medium | `index.html` field-assignment array. Either record fa-events with batter index or stamp pitcher onto each AB and rebuild from there. |
| 6 | `fbSaveGame()` rejects `undefined` field values. `confirmInnEnd` sets `G._csBatterIdx=undefined`; Firestore SDK throws `Unsupported field value: undefined (found in field gdata._csBatterIdx)`. | 🐞 Medium | `index.html:1810-1815`. Add `JSON.parse(JSON.stringify(G))` round-trip in `fbSaveGame()` to strip undefineds before `set()`. |
| 7 | Pitch-threshold modals (`m-plimit`, etc.) can stack on top of each other when ABs end quickly back-to-back. The 21/36/40 popups should be deduped per pitcher per session, not per check. | 🐞 Low | `p._lastNotif` exists per v14 — verify it's actually being respected for stacked thresholds. |
| 8 | Innings-pitched outs aren't decremented when the pitcher who recorded those outs is changed retroactively. Workaround today was to set `G.chp` *before* the inning's ABs. | 🐞 Low | Acceptable for now; the retroactive flow is the rare case. |

---

## v35+ — Feature Gaps (surfaced from today's experience)

Things that would have made today *much* easier and that we'll want before another lost-data scenario.

| # | Feature | Priority | Notes |
|---|---|---|---|
| 1 | **Retroactive game logging UI** — a "log a past game" mode that doesn't try to enforce live-game timing/Firebase sync, suitable for entering games from a paper scorebook after the fact. Should let you paste linescore, pick pitchers per inning, and step through ABs without the chkFW/chkPitcherRest alerts firing. | 📋 v34 | This took 90+ minutes via preview-eval today. A scorecard-style entry form would be ~10 minutes for the same game. |
| 2 | **Error / overthrow / fielding misplay tracking** — currently no way to log E5, E6, throwing errors, missed cutoffs, etc. as separate events. LLHR result type (v16) hints at the error tracking but it's batter-result-only. | 📋 v34 | Needed for fielder accountability and to make play log tell the actual story. |
| 3 | **4-inning game support** — Little League playoff/early-season games are 4 innings, not 6. Currently `showIE` only calls `endGame()` if `G.inn>=5 && oneAhead`. Need a per-game `inningsTotal` field set at game create. | 📋 v34 | Easy fix; comes up regularly. Today's game was 4 innings (rain shortened? scheduled?). |
| 4 | **Pitch reconstruction from result** — when no pitch sequence is known (paper scorebook entry, retroactive logging), default to a sensible pitch synthesis (e.g. K = 3 strikes, BB = 4 balls, BIP = 1 strike) so totals match without manual eval. | 💡 v35 | Goes hand-in-hand with retroactive logging UI. |
| 5 | **Per-AB pitcher stamp** — every AB should record which pitcher faced it. Currently relies on `G.chp/cap` at write time, which makes pitcher reattribution painful. | 💡 v35 | Foundational fix for #5 in v34 priority bugs. |
| 6 | **Game data export / paper scorecard reprint** — print-friendly single-page summary so a parent or coach can reconstruct the game from the app even if they weren't watching. | 💡 v35 | Already in "Future Enhancements" but bumping priority — would have prevented today's retroactive replay entirely. |

---

## Core Scoring & At-Bat

| Feature | Status | Notes |
|---------|--------|-------|
| Ball/Strike/Out counter | ✅ | |
| Pitch sequence display (real-time) | ✅ | v15 — `renderCB` ID mismatch fix |
| Previous AB pitch sequence (faded) | ✅ | v14 — `G.lastABPitches` |
| All result buttons (1B/2B/3B/HR, outs, FC, DP, etc.) | ✅ | FC base-advance broken, see v34#4 |
| Undo last pitch | ✅ | |
| Undo last AB | ✅ | |
| Runner advancement (SB, CS, WP, etc.) | ✅ | CS doesn't credit `ip_outs`, see v34#3 |
| Auto-advance to next batter | ✅ | |
| Multi-runner scoring on short hits | 🐞 | See v34#2 |
| AB flow tolerates `cbi=-1` with pitches in buffer | ✅ | v32 |

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
| Innings pitched tracking | ✅ | Doesn't include CS outs, see v34#3 |
| Per-AB pitcher stamp | 📋 | See v35#5 |

---

## Fielding & Lineup

| Feature | Status | Notes |
|---------|--------|-------|
| 9-player field positions | ✅ | |
| 10-player with RCF (was 4OF) | ✅ | v10/v11 |
| CF left of center / RCF right of center | ✅ | v11 |
| RCF counts in innings-per-player | ✅ | v10 |
| Innings per player tracking | ✅ | |
| Minimum play rule warnings | ✅ | But blocking alert, see v34#1 |
| Catcher pitch-count limit | ✅ | |
| DNP / availability tracking | ✅ | |
| "Remove" button (renamed from DNP) | ✅ | v16 |
| Pitching change → prompt fielder update | ✅ | v16 |
| Block pitch logging until pitcher assigned | ✅ | v16 |
| In-game lineup edit mode (reorder, late arrivals) | ✅ | v31 |
| Mid-inning pitcher in `G.fa[]` | 🐞 | See v34#5 |

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
| 4-inning game support | 📋 | See v35#3 |
| End game | ✅ | |
| Share/Export | ✅ | |
| Game result badge only on `final===true` | ✅ | `586e418` |
| Resume modal (Resume / Start fresh / Cancel) | ✅ | `64ee616` |

---

## PWA / Technical

| Feature | Status | Notes |
|---------|--------|-------|
| Installable PWA | ✅ | |
| Service worker cache (v33) | ✅ | sw.js |
| Offline play | ✅ | |
| localStorage persistence | ✅ | |
| **Firebase / Firestore sync** | ✅ | v18–v20, project `diamond-statz` |
| Multi-device coherent state | ✅ | |
| Test Sandbox (🧪 fake game) | ✅ | `49f59f0` — isolated from real W-L |
| Wipe test data button | ✅ | |
| GitHub Pages deployment | ✅ | snppr212/scorecard |
| `fbSaveGame()` strips `undefined` fields | 🐞 | See v34#6 |

---

## Documentation

| Doc | Status | Notes |
|---|---|---|
| `FIELD_TRIAGE.md` (game-day quick ref) | ✅ | v30 — needs version bump from v30 → v33 references |
| `CHANGELOG.md` | ✅ | Updated through v33 |
| `ROADMAP.md` | ✅ | This file |

---

## Potential Future Enhancements (long-tail)

| Feature | Status | Notes |
|---------|--------|-------|
| Rest day calendar (eligible-to-pitch dates) | 💡 | "Eligible again: Apr 12" |
| Print-friendly scoresheet | 💡 | Bumped — see v35#6 |
| Photo capture for lineup card | 💡 | |
| Push notifications for game day | 💡 | |
| Season stats aggregation | 💡 | |
| Email/text game summary | 💡 | |
| Pitch reconstruction from results | 💡 | See v35#4 |

---

## Known Issues / Needs Verification (carryover)

| Issue | Status |
|-------|--------|
| 40-pitch popup verification in real game | 🔄 Confirmed v15 fix; verified live in `e2` |
| Undo pitch across AB boundary edge cases | 🔄 Monitor |
