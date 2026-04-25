# Mighty Mussels Scorecard — Roadmap

**Current version:** v34 (`216ea51`, 2026-04-24)
**Status as of:** 2026-04-24, after Bulls game (e6) W 6-3

## Status Key
- ✅ Done
- 🔄 In Progress / Needs Verification
- 📋 Planned (next release)
- 💡 Idea / Future
- 🐞 Known Bug

---

## v35 — Next Up

Things to clean up or add in the next round of work.

| # | Issue | Priority | Notes |
|---|---|---|---|
| 1 | Replace remaining native `confirm()` / `prompt()` dialogs with non-blocking modals. Spots: `selBat()` "Switch? Pitches lost", `oppbatEndOrder()` confirm, `runnerM()` prompt for manually adding a runner. | 📋 Medium | Consistency with v34 modal work. |
| 2 | **Mid-inning pitcher change tracking** — `G.fa[]` records who was pitching at the *start* of an inning, not all pitchers within it. Either record fa-events with batter index or stamp pitcher onto each AB and rebuild from there. | 📋 Medium | `index.html` field-assignment array. |
| 3 | **Per-AB pitcher stamp** — every AB should record which pitcher faced it. Currently relies on `G.chp/cap` at write time, which makes pitcher reattribution painful. | 📋 Medium | Foundational fix for mid-inning pitcher tracking. |
| 4 | **4-inning game support** — Little League playoff/early-season games are 4 innings, not 6. Currently `showIE` only calls `endGame()` if `G.inn>=5 && oneAhead`. Need a per-game `inningsTotal` field set at game create. | 📋 Low | Easy fix; comes up regularly. |
| 5 | **Error / overthrow / fielding misplay tracking** — currently no way to log E5, E6, throwing errors, missed cutoffs, etc. as separate events. LLHR result type (v16) hints at the error tracking but it's batter-result-only. | 💡 | Needed for fielder accountability. |
| 6 | Pitch-threshold modals (`m-plimit`, etc.) can stack on top of each other when ABs end quickly back-to-back. The 21/36/40 popups should be deduped per pitcher per session, not per check. | 📋 Low | `p._lastNotif` exists per v14 — verify it's actually being respected for stacked thresholds. |
| 7 | Innings-pitched outs aren't decremented when the pitcher who recorded those outs is changed retroactively. | 📋 Low | Acceptable for now; the retroactive flow is the rare case. |

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
| Per-AB pitcher stamp | 📋 | See v35#3 |

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
| Mid-inning pitcher in `G.fa[]` | 📋 | See v35#2 |

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
| 4-inning game support | 📋 | See v35#4 |
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
| `FIELD_TRIAGE.md` (game-day quick ref) | ✅ | v30 — needs version bump from v30 → v34 references |
| `CHANGELOG.md` | ✅ | Updated through v34 |
| `ROADMAP.md` | ✅ | This file |

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

## Known Issues / Needs Verification (carryover)

| Issue | Status |
|-------|--------|
| 40-pitch popup verification in real game | ✅ Confirmed v15 fix; verified live in `e2` |
| Undo pitch across AB boundary edge cases | 🔄 Monitor |
| Native `confirm()`/`prompt()` dialogs still used in a few spots | 📋 See v35#1 |
