# Mighty Mussels Scorecard — Roadmap

**Current version:** v38.4 (`3936dae`, 2026-04-26)
**Status as of:** 2026-04-26, after grid view + game-day fixes (opp lineup popup, resume flow, sync guard improvements)

## Status Key
- ✅ Done
- 🔄 In Progress / Needs Verification
- 📋 Planned (next release)
- 💡 Idea / Future
- 🐞 Known Bug

---

## v39 — HIGH PRIORITY (after testing wraps)

These are the items the user surfaced during the Lugnuts game testing on 2026-04-26. Hold for implementation until further test feedback is collected.

| # | Issue | Priority | Notes |
|---|---|---|---|
| 1 | **Move "Call game" out of end-of-inning popup** | 🔥 High | Currently the m-innend modal has a red "Call game (time / darkness)" button — too easy to fat-finger when ending a half-inning. Remove from m-innend; relocate to **the bottom of the Rules tab**. The gear menu's "🏁 Call game (end early)" button stays as the primary entry point. Goal: prevent accidental game-ends. |
| 2 | **Placeholder name format and propagation** | 🔥 High | Multiple parts: (a) When "Don't know — use ordinal placeholder" is tapped, the name should be stored as **`(Leadoff)`, `(2-hole)`, `(3-hole)`, `(Cleanup)`, `(5-hole)`** etc. — parentheses included. Currently labels like "Leadoff Hole" / "Cleanup Hole" are displayed but the underlying `name` field is empty, leading to inconsistent rendering across pages. (b) The placeholder should appear on **every** screen — Plays log, Box score, At Bat tab, Lineup tab — not just some. **Bug observed:** user added a placeholder, edited it on the Lineup tab to a real name, the box score updated but the Plays log did not. (c) Visual: render placeholders in **light red text** so they stand out. (d) Editing the placeholder on the Lineup tab should propagate the new name everywhere immediately — including any already-logged ABs that referenced the placeholder. |
| 3 | **Box score: jersey # ahead of name in Player column** | 🔥 High | Currently the Box score "Player" column shows just the name (or `F. Lastname` short form). Should be `#12  Leo Kesselman` or `(12) Leo Kesselman` so it's easier to confirm against a paper scorebook or umpire calls. Apply to both batting and pitching tables, both teams. |
| 4 | **Per-fielder error count in box / stats** | 📋 Medium | `G.errs[]` is fully populated now (v37) — surface a per-player error tally on the Box / Stats page so you can see who's making errors at a glance. |
| 5 | **Walk-off / top-of-last-inning game end detection** | 📋 Medium | If home is leading after top of last inning, app still asks for bottom half. Should auto-end. Walk-off in bottom of last when home takes lead also not auto-detected. |
| 6 | Replace remaining native `confirm()` / `prompt()` dialogs with non-blocking modals | 📋 Medium | Spots: `selBat()` "Switch? Pitches lost", `oppbatEndOrder()` confirm, `runnerM()` prompt for manually adding a runner, `markDNP()`, recalc stats confirm, addTaxi prompt, addGB prompts. |
| 7 | **Pre-fill from saved opponent roster (opt-in)** | 💡 Low | Now that OPP_ROSTERS auto-populate is removed, add an opt-in "Pre-fill from saved roster" button to the opp lineup entry screen for known opponents. Note: v38.7 already shows OPP_ROSTERS as a live menu inside the m-oppbat picker, which may have made this less needed. |
| 8 | **Per-CS pitcher attribution** | 📋 Low | `recalcPitcherStats()` credits CS outs to the half's last AB pitcher — works in most cases but could be wrong if the pitcher changed mid-inning right before the CS. Add `cs.pitcher` field, set at log time. |
| 9 | Backfill pitcher stamps for e2 and e4 | 💡 Low | Old games (Hot Rods, Thunder) don't have per-AB pitcher stamps. Plays log shows no transition lines for those games. |

### ✅ Recently Completed (v35-v38.4)

**Live-game fixes (v38.1-v38.4, today):**
- Opponent lineup choice popup ("Pre-enter" vs "Add live as they bat")
- Pre-entry screen with ↑↓ reorder arrows on each row
- Removed OPP_ROSTERS auto-populate (was hard-coding the roster)
- Resume flow goes straight to scorecard (was incorrectly routing through lineup builder)
- startG checks Firebase before resetting local state (preload race fix)
- Sync guard expanded to also block fielding/pitcher overwrites with empty data

**Earlier (v35-v38):**
- Pre-plan fielding spreadsheet/grid view (positions × innings, bench row)
- Pre-plan fielding by inning (Field tab inning selector)
- Standalone error tracking ("⚠️ Err" button + modal, plays log integration)
- "Call game (end early)" prominent in gear menu — for time/darkness/weather/mercy
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
