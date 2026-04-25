# Mighty Mussels Scorecard — Changelog

## v34 (2026-04-24) — 216ea51
**Bug fixes, opponent batter UX, sync guard, game data entry**

### Bug Fixes
- **Non-blocking alerts** — `chkFW()` and `chkPitcherRest()` now use a dismissable modal (`m-info`) instead of native `alert()`, which was freezing the UI mid-game
- **FC base movement** — Fielder's choice now shows a runner picker ("who is out?") and places the batter on 1B; previously FC left bases unchanged
- **CS ip_outs** — `confirmCS()` now increments `ip_outs` on the current pitcher so caught-stealing outs count toward innings pitched
- **Multi-runner scoring** — `finAB` extra-base logic allows RBI to exceed bases advanced (e.g. single with R2 scoring from 2nd = 2 RBI)
- **Sync guard** — `fbSaveGame()` checks remote AB count before writing; blocks if remote has ABs and local has 0, preventing blank-state overwrites (caused e2 data loss)
- **Undefined field stripping** — `fbSaveGame()` runs `JSON.parse(JSON.stringify(G))` before Firestore `set()` to strip `undefined` values

### Opponent Batter UX (major)
- **Auto-open picker** — opponent batter picker automatically opens at game start, after each opponent AB, and when returning to At Bat tab after fielding assignments. No more hunting for "+ Add next batter"
- **Ghost slots** — "Skip — fill in later" adds placeholder with ordinal labels: Leadoff Hole, Second Hole, Third Hole, Cleanup Hole, Fifth Hole, etc.
- **Skip batter** — skip a slot (kid in bathroom, late arrival); skipped batters show dimmed with SKIP label; skips auto-clear when the batting order wraps
- **Change / skip button** — visible in batting list when opponent lineup is locked; opens picker with "up next" and "skipped" badges per batter
- **Locked lineup flexibility** — after "End of order", user can still pick any batter or add substitutes via the picker

### Our Team Batting
- **Out-of-order support** — when no batter is selected, all batters show with green selectable styling and "Tap any batter to start their at-bat" instruction banner
- `selBat()` un-skips a batter if manually picked

### Other
- **Call game** — "Call game (time / darkness)" button on end-of-half modal with secondary confirmation to prevent accidental taps; clears bases/count and calls `endGame()`
- Service worker bumped to v36

### Game Data
- Entered **e6: Mussels 6 – Bulls 3** (Apr 24) — 64 ABs, full play-by-play, 9 steals
- Recovered **e2: Mussels 6 – Hot Rods 4** (Apr 11) from old session transcript after sync bug overwrote it
- Season record: **2-1** (W Hot Rods, L Thunder, W Bulls)

---

## v33 (2026-04-11) — ff4641f
**Hot Rods roster + retroactive game logging**
- Added **Jack Van Dyke** to `OPP_ROSTERS['Hot Rods']` (new player who joined Hot Rods mid-season)
- Retroactively logged **Mussels 6 – Hot Rods 4** (e2, Apr 11) via preview-eval scripting after the live log was lost mid-game
- Documented several bugs surfaced during the retroactive replay (see Known Issues in ROADMAP)

## v32 (2026-04-11) — 54d85e4
**Opponent on-the-fly lineup + no-batter AB flow**
- Opponent batter picker (`m-oppbat`) now allows adding a new opponent batter inline during the game without rebuilding the full lineup up front
- "End of order" button locks the lineup as built and cycles back through it
- AB flow tolerates `cbi=-1` with pitches in the buffer — pitches stay logged against the current pitcher even before a batter is picked
- Useful when the opposing scorebook is incomplete or batters arrive late

## v31 (2026-04-11) — de641f0
**Plays screen linear + lineup edit mode**
- Plays log redesigned to a single linear stream (vs. previous nested half-innings) — easier to scroll on phone
- Lineup tab gains in-game **Edit** mode toggle: reorder via up/down arrows, mark DNP, support late arrivals

## Field Graphic redesign sequence (Apr 10–11)
- `180a1c3` Bigger gold runner circles centered on bases (visibility from across the dugout)
- `a403381` Field labels show player first name when assigned
- `6ccd8f9` Position name labels in dark boxes, visible dirt around bases + mound
- `a341125` Restored v22 field graphic (solid green wide angle), flipped home plate point downward
- `4851a57` Reverted field graphic to prior version
- `c7843f5` Initial low-angle landscape redesign (later reverted)
- `879da83` Initial proper baseball-diamond rewrite

## v30 (2026-04-10) — `ab6129d`
**Game-day field reference**
- Added `FIELD_TRIAGE.md` — pre-game checklist, sandbox testing notes, common-quirk reference for in-game troubleshooting

## Test Sandbox + Resume hardening (Apr 9–10)
- `49f59f0` **Test Sandbox** — gold 🧪 button on home screen spins up a fake `vs TEST OPPONENT` game; isolated from real data and W-L record; one-tap **Wipe test data** clears all sandbox state including `pitchLog` entries tagged `eventId='test-sandbox'`
- `64ee616` **Resume modal** with three explicit buttons: *Resume*, *Start fresh (erase data)*, *Cancel* — prevents accidental wipes mid-game; auto-cleanup of test sandbox state on launch
- `586e418` Game result badge (W/L/T) on schedule only renders when `gameResults[eid].final === true`

## Firebase integration (v18–v20, Apr 8–9)
- `85f8ab3` **Firebase + Firestore integration** — game state and roster sync to `diamond-statz` project; multi-device coherent state
- `73665e8` Fixed Firebase SDK URL to use compat-version
- `84ba5b5` Bumped service worker to v18 for Firebase integration
- `d82b444` **Fixed infinite recursion** in `sa()`/`sg()` Firebase wrappers — root cause of the "tapping a game does nothing" hang. Wrappers were defined as `function` declarations that hoisted *before* the originals were captured, so `saOrig()` referenced the wrapper itself. Switched to assignments.

## v17 (2026-04-09) — 0ce0e61
**Compact line score strip**
- Compact inning-by-inning strip added to top of At Bat, Plays, and Box tabs — running totals always visible

## v16 (2026-04-10)
**Plays log, box totals, lineup UX, pitch enforcement, result buttons, catcher/pitcher rules**
- **Plays screen**: Rewritten inning-by-inning (newest first), alternating top/bottom with bold divider; ABs that score runs shown in italic amber
- **Box score**: Totals row added to bottom of both batting (AB/R/H/RBI/XBH/HR/BB/K) and pitching (IP/PC/St/Ba/H/R/ER/BB/K/ERA) tables
- **Lineup tab**: "DNP" button renamed to "Remove"
- **Pitching change**: After switching pitcher, confirm dialog offers to jump to Field tab to update all fielding positions
- **75-pitch modal**: Now shows "Finish Batter" (allows current AB, then auto-reopens removal modal) / "Make Pitching Change" / "Override"
- **Pitch logging block**: Cannot log pitches when fielding unless pitcher is assigned in Field tab
- **RBI buttons**: Options greyed out above runners-on-base + 1; impossible RBIs disabled
- **Result buttons**: Homer renamed HR; DP/GIDP merged into "Dou Play" with GIDP checkbox in popup; "Trip Play" simplified; LLHR added (Little League HR — same scoring as HR, tracks errors/misplays)
- **Catcher/pitcher warnings**: Warning when assigning P to player with 4+ innings caught; warning when assigning C to player with 41+ pitches thrown

## v15 (2026-04-09) — d3f7572
**Fix pitch bar and ALL threshold popups**
- Root cause found: `renderCB()` referenced `cb-b/s/o` but HTML element IDs are `sb-cb-b/s/o`
- This crash silently killed every `renderSC()` call, preventing the pitch bar from updating and blocking `chkPW()` from ever running
- One-line fix restores: pitch bar real-time display, all 7 threshold popups, and pitch counter color feedback

## v14 (2026-04-09) — c4e4d7c
**Pitch sequence display, popup dedup, enforcement modals, override button**
- `G.lastABPitches` preserves previous AB pitch sequence so "prev: B B S" shows faded between ABs
- `renderSeq()` shows previous AB pitches when current AB has none (faded/gray)
- `p._lastNotif` dedup flag — each threshold popup fires exactly once per pitcher regardless of how many times `chkPW()` is called
- 75-pitch block now uses proper modal (`m-plimit`) instead of just a toast
- Added **Override — accept rule violation** red button to the 75p/3-HBP block modal
- 3-HBP routing fixed: our pitcher block modal with pitching change button; opponent pitcher notify umpire modal
- `G.lastABPitches = []` cleared at inning end in `confirmInnEnd()`

## v13 (2026-04-09) — 663f5e9
**Pitch limit checks on ALL outcomes**
- `chkPW()` added at top of `finAB()` so hits, fly outs, ground outs, line outs, sac flies, DPs, etc. all trigger threshold checks
- Previously only K, BB, and HBP called `chkPW()` — any result button outcome skipped it entirely

## v12 (2026-04-08) — 5d44c5a
**Away-team pitch logging, solid green field**
- `ensurePitcher()`: auto-creates a placeholder pitcher for whichever side is currently pitching — fixes silent failure when Mussels are the away team and no pitcher was set
- Field SVG simplified: removed outfield arc/gradient/fake wall, now solid `#1e6838` green rectangle
- `endAB()` calls `ensurePitcher()` instead of returning silently when no pitcher set

## v11 (2026-04-08) — 78c1547
**Pitch thresholds via result buttons, 75p enforce, 3-HBP block, CF/RCF positions**
- `chkPW()` called in K/BB/HBP branches of `lp()` before `endAB()`
- 75-pitch reached mid-AB now sets `G.plb=true` and blocks next batter (not just between innings)
- 3-HBP triggers forced pitcher removal modal
- CF shifted left of center when RCF is in lineup; RCF placed mirrored right of center
- Auto pitcher-picker modal opens when no pitcher is set

## v10 (2026-04-07) — a90d1e9
**RCF rename, innings tracking, opponent jersey, HBP counter**
- "4OF" position renamed to "RCF" throughout
- `renderFT()` switched from `APOS` to `getActivePOS()` so RCF assignments count in innings-per-player tracking
- Matchup bar (`renderMU()`) now shows opponent batter jersey number via `tlu()` lookup
- HBP counter added per pitcher; shown in matchup bar when HBP > 0
- Pitch threshold popups added for K/BB/HBP paths in `lp()`

## Earlier versions (v1–v9)
- **v9/bca735a**: Pitch thresholds (21/36/40/51/65/66/75), mercy rule, undo AB, rest warnings, catcher limit
- **v8/6352a03**: Runner logic fixes, remove count-bar, 40p popup, skip absence screen, DNP mid-game edit
- **v7/a0eb6c4**: 7 bug fixes — pitch logging, field graphic, foul lines, force play, auto-batter, 6-run rule, opp lineup builder
- **v6/62425a8**: Fix Pitchers tab team name labels
- **v5/7fc6059**: UI + logic — tabs, field SVG, force plays, auto-batter, CS logic
- **v4/5d2f194**: Fielding display, RHP/LHP toggle, End Game flow, SW cache fix
- **v3/8f16ebc**: Pitcher limit enforcement, lineup rebuild, log notation
- **v2/c401456**: Per-team batting, pitcher stats, compact score bar
