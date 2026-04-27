# Retro Scorecard — Detailed Accounting of What's Wrong

**Status:** Hidden behind a stealth link at the bottom of the Rules tab ("retro scorecard preview (WIP)"). Removed from the prominent Box-tab button.

**Reference:** [@MlbScorecards on X](https://x.com/MlbScorecards) — the user's gold standard. They mailed a sample with the Colorado Rockies vs San Diego game.

This document captures **everything that's broken** in the current implementation, **why it's different from the @MlbScorecards style**, and **how to fix each issue**. Pick this up later when there's bandwidth.

---

## Lineup vs cell anatomy

### What @MlbScorecards has, in each AB cell

```
┌──────────────────────────────┐
│ ┌─────┐   ┌──┐               │
│ │ ●●● │   │② │               │  ← top-left: count grid (3+2 horizontal dots)
│ │ ●●  │   └──┘               │  ← top-right: OUT NUMBER (only on outs)
│ └─────┘                      │
│         ╱╲                   │
│        ╱  ╲                  │  ← center: diamond
│        ╲  ╱   F8             │  ← result notation IN/AT the diamond, centered
│         ╲╱                   │
│ ●●                           │  ← bottom-left: RBI dots (one per RBI)
└──────────────────────────────┘
```

### What I have

- ✅ Count grid (top-left), but layout is right-ish
- ❌ Out# circle is partially right but **rendered in WRONG POSITION** and **inconsistently** (see below)
- ✅ Diamond center with result code — but result is **NOT actually centered visually**
- ❌ RBI dots placement OK but inconsistent
- ❌ End-of-inning slash is rendering on **the wrong cells** because I'm using a CSS `linear-gradient` that draws across the whole cell and looks wonky

---

## Detailed bug inventory

### 1. ❌ Out# rendering broken on multiple levels

**What @MlbScorecards does:**
- A small CIRCLE with a number 1, 2, or 3 appears in the top-right of the cell
- ONLY on cells where the AB resulted in an out
- The number = which out of the inning this AB produced
- 3 circles maximum per inning (across all batter rows)
- For DP/GIDP, it shows the LATER number (e.g., a DP that's outs 2 and 3 shows "3")

**What I have:**
- I only render the circle for outs (correct logic in `_scComputeOuts`)
- BUT in screenshots, circles are appearing on cells where the player WALKED or got a hit
- Why: looking at the latest user-shared image, the circles in the top-right appear on Chatnani's BB (inning 3, marked "3"), Kalman's HR (marked "3"), Kalman's 1B (marked "3") — **NONE of which are outs**. So my code IS rendering them wrong.
- Suspected cause: I have a residual reference to "batter # of inning" code from earlier that's still firing somewhere, OR the `outsMap[ab.num]` lookup is getting wrong values.
- Could also be a rendering issue where my CSS class `.sc-bnum` (old) is still being matched.

**Goal:** Walk through `_scComputeOuts` again with real data, verify the map only contains out-resulting ABs. Verify the render code only emits the circle when `outNum` is truthy. Test against e6 game data and confirm.

### 2. ❌ End-of-inning slash is wrong

**What @MlbScorecards does:**
- A diagonal line drawn through the cell where the 3rd out of the inning was made
- Goes from upper-LEFT to lower-RIGHT (or in some scorecards, upper-right to lower-left)
- The slash is roughly 60-70% of the cell, drawn as a single ink line
- It marks "this is where the half-inning ended"
- ALSO in their scorecard, BETWEEN the starter row and sub row, there's a subtle horizontal-ish slash showing where the substitution happened

**What I have:**
- I'm using a CSS `linear-gradient` that draws a diagonal stripe across the entire cell background
- It renders inconsistently and overlaps weirdly with the diamond outline
- It's drawn in CELLS where I detect "end of inning" but my detection logic is off
- Specifically `_scIsEndOfInning` checks `outsMap[ab.num]===3` — but this fails for half-innings that ended without 3 outs (e.g., 6-run rule, walk-off, game called)

**Goal:** Replace the `linear-gradient` approach with an actual SVG line drawn over the cell. Make `_scIsEndOfInning` correctly identify the LAST AB of every half-inning (not just 3rd-out cases). The slash should be visible but not overpowering — maybe 1.5px stroke at 60% opacity.

### 3. ❌ Result text is NOT centered on the diamond

**What @MlbScorecards does:**
- The result code is dead-center on the diamond (and therefore the cell)
- For ground outs like "4-3", the text spans the diamond width but is centered
- For longer codes like "GIDP" the source uses smaller font OR shorter abbrev
- The text is INSIDE the diamond, not below or above

**What I have:**
- My CSS positions `.sc-result` at `top:50%; left:50%; transform:translate(-50%,-50%)` which SHOULD center it
- BUT the screenshots show the text rendering at the bottom-center of the diamond, not the actual middle
- Why: I think the diamond SVG is 30×30 with `top:50%` on a 46px-tall cell, so its center is at y=23 in the cell. My text is also at top:50% (y=23). Both should overlap.
- BUT there's an issue with the `.sc-diamond` element having `position:absolute; top:50%; transform:translate(-50%,-50%)` and the SVG inside it. The SVG might have padding or the wrapper could be shifted.

**Goal:** Make the result text TRULY centered on the diamond. Test by rendering with no diamond (just the result) to verify the centering works in isolation. Then bring the diamond back.

### 4. ❌ Lineup data and ordering issues

**What user noticed:**
- "i think you have our lineup wrong but whatever. beck was after bresson"
- The user's actual Lugnuts game lineup had Hunter Bresson BEFORE Miles Beck. My render shows them in the order they appear in `G.alu` which may differ from actual batting order due to live-entry sequencing.

**Goal:** Verify that the lineup rendering uses the FINAL `G.hlu`/`G.alu` order (after any reorder operations), not the chronological add-order. This may require validating the lineup state before rendering.

### 5. ❌ Out notation doesn't match scoring conventions

**What @MlbScorecards does:**
- Fly out: "F#" where # is the position (e.g., "F8" = fly to CF)
- Pop out: "P#" where # is the position (e.g., "P6" = pop to SS)
- Line out: "L#" (e.g., "L9" = lineout to RF)
- Ground out: "#-#" position chain (e.g., "4-3" = 2B to 1B; "5-3" = 3B to 1B; "6-3" = SS to 1B)
- Double play groundball: "#-#-#" chain (e.g., "4-6-3") with "GIDP" notation
- Double play flyball: just "DP"
- Strikeouts: "K" swinging, "Ⓚ" (backwards K) for called/looking
- Walks: "BB"
- HBP: "HBP" or "HP"
- Sac: "SAC" or "SF"

**What I have:**
- I added `_scResultDisp(ab)` which uses `ab.not` (user-typed notation) when present
- This works for outs the user manually typed (F8, 4-3, etc.)
- BUT for plays where the user didn't type a notation, I fall back to "F", "G", "L" — which is incomplete (missing the position number)

**Goal:** When the user logs an AB result via the result buttons (FO, GO, LO), prompt for the position number OR auto-suggest based on the recorded `not` field. The Plays log already does this; the scorecard renderer just needs to surface it correctly.

### 6. ❌ Players out on the bases (not in their AB) — runner-out indicator missing

**What @MlbScorecards does:**
- When a runner is out trying to advance (CS, picked off, etc.), they draw:
  - A short line from home toward the base they were going to (about half the diamond's path length)
  - A perpendicular tail at the end (looks like a `T` rotated)
- This appears in the cell of the AB where the runner ORIGINALLY got on base
- Visually says "they reached this base, then tried to advance and were OUT"

**What I have:**
- Nothing. CS events are in `G.css[]` but I don't draw the half-line indicator on the original AB cell.

**Goal:** Cross-reference each AB with `G.css[]` entries that match the runner. When a CS happened to a runner who was on base from a particular AB, draw the half-line + tail in that AB's cell.

### 7. ❌ RBI dots present but inconsistent

**What @MlbScorecards does:**
- Small red dots in the lower-LEFT of the cell
- One dot per RBI

**What I have:**
- I added the dots in lower-left
- Sometimes they don't render or they overlap with the end-of-inning slash
- The slash gradient covers them up

**Goal:** Make sure RBI dots have `z-index:3` so they appear above the slash. Test rendering with both end-inning + RBIs in the same cell.

### 8. ❌ Borders too uniform / too dark

**What @MlbScorecards does:**
- Border weight varies — outer edges of the table are thicker, inner cell dividers are thinner
- Color is more like a medium grey ink, not pure black

**What I have:**
- All borders are `0.75px solid #888` — uniform
- Looks "computery" because of the uniformity

**Goal:** Use a 2-tier border:
- Outer table border: 1.5px #555
- Inner cell borders: 0.5px #aaa
- Also: every Nth row could have a slightly heavier divider (e.g., every 3 batters) to break visual monotony

### 9. ❌ Cells render small / cramped on mobile preview

**What @MlbScorecards does:**
- Their scorecard is sized for printing on letter or larger paper, in landscape
- Cells are roughly 60-80px wide on screen, scaled appropriately for print

**What I have:**
- Cells are 60×46 px
- Mobile preview at 375px wide compresses everything
- The diamond + count + out# + RBI fight for space when there are many columns

**Goal:** 
- Always render at print size (e.g., 720px wide minimum)
- Add a CSS rule to scale down the *whole* scorecard via `transform:scale(0.5)` on small viewports so it stays readable
- OR show a "Best viewed in landscape / print" message on mobile

### 10. ❌ Two-row player slots (starter + sub) missing entirely

**What @MlbScorecards does:**
- Each batting slot has TWO rows: starter on top, sub on bottom
- Sub's name shows their substitution inning, e.g., "Frias (6)" came in during inning 6
- Inning cells are split: starter's ABs in the upper portion, sub's ABs in the lower portion

**What I have:**
- One row per batter
- Subs would just appear as new rows below if added live
- This is the BIGGEST structural difference from the source

**Goal:** Major refactor. Track substitution info on lineup entries (currently we have `addGB` for late arrivals but no "substituted in inning N" metadata). Each row could be a 2-row visual with the starter on top, sub on bottom, and inning cells split by horizontal line in the middle.

### 11. ❌ Pitcher table missing W/L/S, BK, WP columns

**What @MlbScorecards does:**
- Columns: # | Pitcher | W/L/S | IP | H | R | ER | BB | K | HBP | BK | WP | TBF
- W/L/S column shows Win / Loss / Save / Hold

**What I have:**
- Columns: Pitcher | IP | PC | H | R | ER | BB | K | HBP | TBF | ERA
- No W/L/S, no BK (balks), no WP (wild pitches)

**Goal:** 
- Add W/L/S column. Compute by examining `G.runs` and pitcher game-state at runs-scored time. Whoever was pitching when the winning team took a lead they didn't relinquish = W; pitcher of record when losing team scored go-ahead = L.
- Add BK and WP columns; we don't track these yet, so they'd be 0 always until we add the tracking

### 12. ❌ Per-inning footer rows (R/H/E) wrong placement / styling

**What @MlbScorecards does:**
- 3 rows BELOW the AB grid: Runs / Hits / Errors per inning
- Aligned with inning columns above
- Bold weight, slightly different background

**What I have:**
- I have these but they're rendering inconsistently — the styling is OK but the column alignment with the inning columns above doesn't always work

**Goal:** Use the same column structure as the AB grid above (matching `colspan` and column widths). Verify the alignment in the rendered output.

### 13. ❌ Game time tracking missing

**What @MlbScorecards does:**
- Bottom-right of the AB grid: "Game Time: 2:43"
- Total elapsed time from first pitch to last pitch

**What I have:**
- Nothing. We don't track timestamps on innings or pitches.

**Goal:** Stamp `G.gameStart` at the first pitch of inning 1 and `G.gameEnd` at end-game. Display the difference in HH:MM format.

### 14. ❌ Header layout regression on narrow viewport

**Problem:** When the preview panel is mobile-width (375px), the 3-column header (date/title/result) compresses badly:
- Date wraps to multiple lines
- Title wraps "Mighty" / "Mussels" awkwardly
- Result "W 6-3 / @ Bulls" gets squeezed

**Goal:** Add a media query for narrow viewports. Stack the three sections vertically OR scale the entire scorecard down with `transform:scale()`.

---

## Recommended order of operations when picking this back up

1. **First, fix the out# rendering bug** — this is probably a stale code path. Verify `_scComputeOuts` output by `console.log`'ing it for a known game; check that the renderer ONLY emits the circle when `outsMap[ab.num]` is set.

2. **Replace the linear-gradient end-of-inning slash with an SVG line.** Detect the last AB of each half-inning correctly.

3. **Verify result-text centering** — render with no diamond first, confirm it lands dead-center, then bring the diamond back.

4. **Fix the result notation** — for outs without user-typed `ab.not`, generate one based on the position fields if available.

5. **Then tackle the rest** in priority order based on what looks wrong on a real print.

---

## Why this got messy

- I made multiple iterations without re-validating against the source image each time
- Some changes ADDED issues while fixing others (e.g., the gradient slash, the cell-size adjustments)
- I was confident the code was right when actually the rendered output was wrong — should have screenshotted at every step
- The user is correct that I "regressed" — comparing my final output to the @MlbScorecards source, important details (like out# only on outs, count dots horizontal, slash convention) drifted out of correct as I made other changes

Next time:
- Start with a focused checklist matching the source 1:1
- Rebuild from a clean implementation rather than incrementally patching
- Validate each piece against the source image before moving on
- Don't trust intermediate screenshots without comparing to source carefully

---

**Hidden access:** Bottom of Rules tab, small "retro scorecard preview (WIP)" link.

**Code location:** `index.html` — search for `function openRetroScorecard` and `function renderRetroScorecard`.

**Last commit:** `c94112d` (v60). After this, only the access-point change to hide it from Box tab.
