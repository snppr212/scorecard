# Mighty Mussels Scorecard — Changelog

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
- 3-HBP routing fixed: our pitcher → block modal with pitching change button; opponent pitcher → notify umpire modal
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
