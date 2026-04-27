# Mighty Mussels Scorecard — Changelog

## v64 (2026-04-27) — 9b1dae0
**Base font switched to Roboto**
- Body font changed from Georgia (serif) to Roboto with system fallbacks (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif`)
- Loaded from Google Fonts (400 / 500 / 700 weights) with `font-display:swap`
- All headings, schedule items, panel titles now render in clean Roboto
- Retro scorecard's Caveat / Patrick Hand fonts are unaffected (still lazy-loaded)

## A.gameResults restore (2026-04-27)
**Data fix — record was showing 0-0**
- The home-screen record was rendering as "0-0 (12 games)" because `A.gameResults` had been wiped at some point
- Rebuilt entries for e2 (Hot Rods W 6-4), e4 (Thunder L 2-5), e6 (Bulls W 6-3) by reading each game's `gdata.as` / `gdata.hs` from Firebase and pushing back to `A`
- Record now correctly shows **2-1 (12 games)** with proper W/L badges on each schedule entry
- No code change — pure data restore via runtime eval

## v63 (2026-04-27) — bf8f4c0
**CRITICAL FIX: ID collision — `sc-content` was being used by both at-bat tab and retro scorecard**
- Root cause of every "fucked up base app" complaint
- The retro scorecard's content div was `id="sc-content"`, but the at-bat tab's scroll container was ALSO `id="sc-content"` (predated the scorecard work)
- Result: every `#sc-content` CSS rule meant for the retro scorecard (cream background, dark text, Patrick Hand font) was leaking onto the at-bat tab via the duplicate ID
- Fix: renamed all retro scorecard IDs with `rsc-` prefix:
  - `sc-content` → `rsc-content` (38 CSS selectors + HTML element)
  - `sc-printable` → `rsc-printable`
  - `sc-sub` → `rsc-sub`
- The original at-bat tab IDs (`sc-content`, `sc-title`, `sc-sub`) are unchanged

## v62 (2026-04-26) — 0e1f7bd
**e7 (Lugnuts) wiped + TBD postponement highlight + lazy fonts**
- e7 game data deleted from Firebase (game was postponed)
- Schedule entry reset: date='TBD', time='', location=''
- TBD events now sort to the END of the schedule
- Visual highlight: red border + red-tinted background, "POSTPONED · TAP EDIT" badge
- Tapping a TBD entry toasts "Edit to set new date / time / location" instead of starting a game
- **Removed Google Fonts `<link>` from `<head>`** — fonts now lazy-load only when retro scorecard is opened. Base app loads zero external fonts.

## Retro scorecard parked as WIP (2026-04-26) — e33e23b
- Removed prominent "📋 Open scorecard" button from the Box/Export tab
- Added small (9px, 50% opacity) "retro scorecard preview (WIP)" link at the bottom of the Rules tab
- Created `RETRO_SCORECARD_TODO.md` documenting all known issues vs the @MlbScorecards source — 14 items with detailed accounting and recommended order of operations for picking it up later

## v41 part 6 (2026-04-26) — c94112d
**Retro scorecard — fix the actual scoring conventions**
- Out # now correctly assigned only to ABs that resulted in outs (1, 2, 3 per inning); built `_scComputeOuts(g)` walking ABs and tallying outs per half-inning
- Count dots laid out horizontally (3 balls top row, 2 strikes bottom row)
- Result text dead-centered on the cell + diamond
- End-of-inning diagonal slash via CSS gradient on `.end-inn` class
- Out notation prefers user-typed `ab.not` (so "F8", "4-3", "6-3" show properly)
- RBI dots in lower-LEFT (not red text); one filled circle per RBI
- Borders lightened from #1a1a1a to #888 at 0.75px

## v41 part 5 (2026-04-26) — bb8686c
**Retro scorecard — fix header redundancy and cell layout**
- Removed fake "@MightyMussels" handle
- Stripped "Field N" suffix from location display
- Cells widened (54×54), diamond positioned below count/bnum corners (no overlap)

## v41 part 4 (2026-04-26) — 3f00489
**Retro scorecard polish round 2 — dot rendering, name compaction, layout tightening**

Iterating on the press-box style after first-look review. All 7 issues from the review fixed:

1. **Count box** — replaced 6×6 squares (which rendered as solid blobs at small size) with proper circular dots. Empty: thin grey outline circle. Filled: solid dark fill. Layout: 3 rows × 2 cols, 4×4px dots, 1px gaps. Clearly readable now.
2. **Batter # of inning** — bumped to 13px Caveat with a circle outline around it (matches @MlbScorecards aesthetic).
3. **Row spacing** — cell height reduced 50→42px; ~20% more compact overall.
4. **Position column** — fixed `_scPlayerPos` to scan all innings of `G.fa` (was only checking inning 1). Now finds first inning where the player has a position assigned.
5. **Long result codes** (HBP, LLHR, GIDP, SAC) — auto-shrink via `.sc-result.long` class (11px instead of 14px).
6. **Filled-diamond outline** — thicker (1.6px) so it pops against the grey fill.
7. **Name shortening** — new `_scShortName()` helper returns last name only, except when there's a duplicate last name in the lineup (Bresson family) where it falls back to "H. Bresson" / "C. Bresson". Saves horizontal space.

Bumps sw.js to v58.

## v41 part 3 (2026-04-26) — d4bc9c7
**Retro scorecard major polish — Caveat font, scored detection, count box, batter # marker, per-inning footer**

- Google Fonts: **Caveat** (handwriting) + **Patrick Hand** (small text). Player names render in Caveat script, result codes in Caveat bold.
- Cell anatomy: count box top-left, batter # top-right, diamond center, RBI bottom-right.
- **Scored detection**: cross-references `G.runs[]` for matching `bi+team+inn+half`. Diamond fills with grey background when batter eventually scored.
- Per-inning Runs/Hits/Errors footer rows.
- TEAM totals row at the bottom of each batting table.
- Pitcher TBF column (counts batters faced via `ab.pitcher` stamp).
- Print: `@page` set to landscape letter for the wider grid.

## v41 part 2 (2026-04-26) — d4510ba
**Retro scorecard export — printable press-box style**

New "Retro scorecard" section on the Box/Export tab opens a dedicated screen styled like a classic press-box scorebook (inspired by [@MlbScorecards](https://x.com/MlbScorecards)).

- Cream paper background, Georgia serif font, ink-style borders
- Header: teams, date, location, final score, W/L badge
- Batting tables for both teams: row per batter, columns for innings 1..N, then AB/R/H/RBI/BB/K totals
- Each AB cell renders a small diamond SVG showing the batter's path through the bases (red path), with the result code (K, 1B, BB, etc.) inside. Filled red diamond when the batter scored.
- RBI count in tiny red text in the cell corner
- Pitching tables (both teams) with IP, PC, H, R, ER, BB, K, HBP, ERA
- Footer with legend
- Print support: `@media print` rules, "🖨 Print" button, letter-size page

Bumps sw.js to v56.

## v41 part 1 (2026-04-26) — 3e48091
**Season aggregation — per-player career stats**

New "📊 Season Stats" button on the home screen opens a Season Stats screen.
- Pulls all finalized games from Firebase, excludes test-sandbox
- Batting table: per-player aggregated stats (G/PA/AB/R/H/RBI/HR/BB/K/SB) plus BA/OBP/SLG, sorted by BA descending. TEAM totals row.
- Pitching table: per-pitcher aggregated stats (G/IP/PC/H/R/ER/BB/K/HBP/ERA), sorted by IP. STAFF totals row.
- Player names show jersey # prefix when available
- "G" (games played) only counts games where player had ≥1 PA or pitcher had ≥1 pitch
- Auto-out ABs excluded from PA

## v40 prep (2026-04-26) — 81a201c
**Pitchers tab "Avail?" column — now shows the eligible date**

- Was: ✓ or ✗ per pStatus
- Now: ✓ if eligible today, "Tomorrow", or "Mon Apr 28" — the actual day name + date the pitcher is next eligible
- Uses existing rest-days rule (`restD(pitches)`) applied to each pitcher's last outing date in `A.pitchLog`
- New helpers: `pNextEligibleDate(name)`, `fmtAvailDate(elig, today)`
- Bumps sw.js to v55

## v39.1 (2026-04-26)
**Rules tab — Rest days reformatted**
- Rest days on the Rules tab now render one threshold per line with bold day counts, instead of bunched together with `·` separators
- Bumps sw.js to v54

---

## v39 (2026-04-26) — 731a8b9
**Plays log redesign, edit/swap ABs, placeholders, jersey #s, PA, skip-our-batter, "Call game" relocated**

Shipped as 4 batches across the day after Lugnuts game testing.

### Batch 1 — quick wins (sw v50)
- **A1: "Call game" safety** — removed the red Call-game button from the end-of-half-inning modal (m-innend) where it was easy to fat-finger; relocated to the bottom of the Rules tab. Gear menu's Call-game button stays as the primary entry point.
- **B4: PA counter** — `gps()` now returns `s.pa` (counts plate appearances, excludes auto-outs). Bat list, matchup bar, and box score all show `0/1 (3PA)` when PA differs from AB. Box score gets a new PA column.
- **A3: Jersey # ahead of name in box score** — new `_findJersey(name)` and `boxName(p)` helpers. Batting and pitching tables show `#12 L. Kesselman` instead of just `L. Kesselman`.
- **B5: Skip-this-batter for our team** — new `skipBatter(i)` mirrors the opponent skip. Each row in the bat-list (our team only) gets a small `skip` / `un-skip` toggle button. For the bathroom-kid scenario.

### Batch 2 — placeholder names + propagation (sw v51)
- **A2 part 1: Placeholder format** — `oppbatGhost()` now stores names as `(Leadoff)`, `(Cleanup)`, or `(N-hole)` (parens included in the actual `name` field, not just the visual label). New `placeholderName(i)` and `isPlaceholder(name)` helpers.
- **A2 part 2: Propagation fix** — `abBatterDisplay` now looks up the CURRENT lineup entry by `bi` index first (then falls back to name match). Renaming a placeholder on the Lineup tab to a real name now propagates to the Plays log immediately. Lineup-tab inputs auto re-render Plays log, Box score, and At Bat via new `_propagateLineupEdit()` helper.
- **A2 part 3: Light-red rendering** — placeholder names render in `#ff8888` italic everywhere: Plays log, Box score, At Bat tab, batting list, matchup bar, opp picker.

### Batch 3 — Plays log redesign (sw v52)
- **B1+B2+B3: 4-column grid + sub-lines**
- New layout: `# | batter | pitch sequence | result badge` — fixed widths on cols 1 & 4 so long pitch sequences wrap instead of pushing the result badge off-screen
- Removed the right-side `+R` badge — runs now show as an indented sub-line
- **Sub-lines under each AB:**
  - **Steals**: green `↳ SB by J. Smith (1st → 2nd)` — multiple steals = multiple sub-lines
  - **Caught stealing**: red `↳ CS by J. Thomas (2nd → 3rd, OUT)`
  - **Runs scored**: amber italic `↳ Scored: Ethan T., Miles B. (+2 R)`
- **Data model additions:**
  - `ab.pscored` — names of runners who scored on this AB; stamped at finAB time via a global buffer that `logRun` feeds into
  - `steal.during_ab_num` — set to `G.abc + 1` at log time so the Plays log knows which AB to attach the sub-line to
  - `cs.during_ab_num` + `cs.name` + `cs.from` — captured from `G.bases` before the base is cleared
  - `G.runs` entries also get `half:G.half` (was missing on some paths)

### Batch 4 — edit & swap ABs (sw v53)
- **B6: Plays log gets ✎ (edit) and ⇄ (swap) icons on each AB row**
- **Edit-AB modal**: change batter (dropdown of lineup), result, RBI, notation. Save → recalculates pitcher stats. Delete option also available with confirm prompt.
- **Swap-AB modal**: pick another AB from the same half-inning. Confirm → swaps ONLY `bi` and `batter` (pitches, result, RBI stay with their original AB). For the out-of-order-batting scenario when you don't catch it live.

---

## v38 (2026-04-25) — f41524c
**Pre-plan fielding spreadsheet (grid) view**

Field tab gains a "By Inning / Grid" toggle. Grid view shows the entire game's fielding script on one screen so you can pre-plan rotations and adjust at the field in real time.

- Toggle at the top of the Field tab; defaults to "By Inning"
- Grid renders positions as rows (P/C/1B/2B/3B/SS/LF/CF/RF/RCF) and innings as columns (1-6 by default)
- Bench row at the bottom auto-derives who's sitting each inning (lineup minus assigned players, excluding DNP)
- Current inning's column highlighted with a gold-tinted header
- Cells show player first name truncated to 6 chars (with period) for compact display; empty cells show "—"
- Tapping any cell opens the position picker scoped to that specific (inning, position) — picker title reads "Assign LF (Inn 4)" so the scope is clear
- Each pickable player shows their current innings count for at-a-glance balance ("3i", "2i", etc.)
- Horizontal scroll on narrow screens
- Innings-per-player summary still shown below the grid in both modes

### v37.1 — Always 6-inning games; "Call game" prominent
- Per actual league rules, games are always scheduled as 6 innings (mercy/time/darkness/weather can call them early)
- Removed the per-event Innings dropdown (was added in v37, premature)
- Replaced the bare "End Game" button in gear menu with "🏁 Call game (end early)" routed through the existing confirmation flow
- m-callgame copy updated to mention all 4 valid reasons (time / darkness / weather / mercy)

---

## v37 (2026-04-25) — 559e89a
**4-inning games, pre-plan fielding, error tracking**

### 4-inning game support
- Event create/edit modal now has an Innings dropdown (6 regular / 4 early-season-or-playoff)
- `resetG` reads `ev.innings` (defaults to 6) and sizes the inning score arrays accordingly
- `showIE` uses `G.ti` instead of hardcoded 5 — game ends only after the scheduled innings have been played
- Mercy rule scales: 10-run lead after 4 innings for a 6-inn game, after 3 for a 4-inn game
- Min-fielding warning (`chkFW`) scales: 3 innings min for 6-inn, 2 for 4-inn (per Rules tab)

### Pre-plan fielding assignments
- Field tab now has an inning selector at the top, defaulting to current inning
- "● LIVE" badge shows when viewing the current inning; "⟲ Current" button when viewing past/future
- All field assignment operations (`renderFT`, `openPM`, `asgPos`, `clrPos`, `copyField`) honor the view-inning state via new `viewInn()` helper
- Field SVG reflects the viewed inning so you can preview a planned setup
- Pitcher auto-sync only fires when assigning the current inning's P (pre-planning future innings doesn't change the live pitcher)
- Workflow: script your fielding rotations ahead of time, adjust at the field in real time

### Standalone fielding error tracking
- New "⚠️ Err" button in the runner action bar for errors during baserunning (overthrow, missed cutoff, dropped pickoff)
- `m-serr` modal: position picker showing current fielder names, error type (Fielding / Throwing / Mental / Catching), optional description, "Bases advanced" selector (with note about LL's 1-base-on-overthrow rule)
- Recorded as `{player, pos, inn, half, type, play, adv, standalone:true}` in `G.errs`
- If "Bases advanced" is set, the lead runner advances that many bases (or scores) automatically
- Plays log shows standalone errors as italic amber lines after the half's ABs (e.g. "⚠️ E5 (Throwing) — E.Kalman — Overthrow on SB attempt — runner +1")
- Existing in-AB error logging now also records `half` and `standalone:false` for consistency
- New `_posNum()` helper maps positions to E1/E2/E3/etc. notation

---

## v36 (2026-04-25) — 0773e1c
**Per-AB pitcher stamp, threshold fixes, retroactive recalc**

### Mid-inning pitcher change tracking
- Every AB now records the pitcher who faced it (`ab.pitcher`, `ab.pitcherTeam`) — captured live from `curPitcher()` at `finAB` time
- Plays log shows a `⚾ Pitching: <name>` line whenever the pitcher changes between consecutive ABs in the same half-inning
- New `abPitcher(ab)` helper resolves an AB's pitcher with fallback to `G.fa[inn].P` for old ABs without stamps
- e6 backfilled — bottom-3rd Ezra→Miles transition now shows in the play log

### Pitch threshold bug fix (missed warnings)
- `chkPW()` used strict equality (`c===21`, `c===36`, etc.) — if a pitch count jumped over a threshold (e.g. 19→22 via a 3-pitch K), the warning silently skipped
- Now uses `c>=N` with the existing dedup flag (`p._lastNotif`) so each threshold fires exactly once when crossed
- Threshold labels updated to "21+", "36+", etc. for clarity

### Threshold modal queue
- New `_pwarnQueue` defers a second warning if the first is still open
- Prevents back-to-back threshold firings from overwriting modal content mid-read
- Updated "Got it — continue" button to call `_pwarnDismiss()` which pops the queue

### Retroactive pitcher recalc
- New `recalcPitcherStats()` walks `G.abs` and rebuilds every countable field per pitcher: `total`, `sw`, `lk`, `fo`, `ba`, `bip`, `hbp`, `stk`, `ip_outs`, `hits`, `runs_allowed`, `er`, `bb_allowed`, `k_pitched`, `hbp_allowed`
- CS outs credited to the pitcher of the half's last AB
- Auto-out ABs skipped (no pitcher charge)
- "⟲ Recalc stats from ABs" button added to Pitchers tab → Our Pitchers section, behind a confirm prompt

---

## v35 (2026-04-25) — 65686f1
**Stolen base checkbox UI + auto-out batter**

### Stolen base modal redesigned
- Old dropdown ("From: 1st/2nd, Player: ___") replaced with a checkbox list of physically-possible advances: "Runner2 2nd → 3rd" and "Runner1 1st → 2nd"
- Multiple checkboxes for double steals — executed lead-to-trail (so 2nd vacates before 1st advances)
- Stealing home explicitly disallowed per LL rule, with note shown when a runner is on 3rd
- Validates impossible combos (e.g. 1st→2nd when 2nd occupied without 2nd also stealing)
- Matches the Rules tab: "1 per half-inning. No stealing home. Double steals count as 1."

### Auto-out batter for CBO removal
- New "+ Auto out (player removed from CBO)" button in opponent batter picker
- For the legitimate LL Rule 4.04(h) case: a player who started the game gets removed (injury / ejection / left early) — their CBO spot becomes an auto-out each time through
- When the auto-out spot comes up: logs an AB with result `AO`, 0 pitches, 0 RBI, no pitcher attribution; increments outs
- Auto-fires on half-inning start, normal advancement, and manual pick — no UI interaction needed
- Slot stays in rotation each time through the order
- Rules tab updated to note: "Player removed mid-game = automatic out each time spot comes up (LL 4.04(h))"

---

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
