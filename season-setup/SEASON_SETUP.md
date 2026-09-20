# 🐚 2026 Fall Season Setup — Master Task List

Kickoff: **new season starts ~2026-09-20**. Division moves **AA → AAA**.
Owner: Sam. This is the living checklist — check items off as we go.

> **Legend:** `[x]` done · `[ ]` to do · 🔴 needs you (blocked on input/decision) ·
> 🟠 destructive (do together, timed with season start) · 💡 feature idea

---

## ✅ Phase 0 — Done autonomously this session (2026-09-19)
- [x] **Archived the entire Spring 2026 season** (read-only) → `archive/2026-spring/`
  (roster+schedule+results, league pitch log, all 11 game scorecards). Safety net for the reset.
- [x] **Extracted the new AAA rulebook** → `reference/2026-aaa-rules.txt` (28 KB, full text).
- [x] **Diffed AA → AAA** for rules that change app *logic* (see Phase 1d).
- [x] **Drafted all fall rosters** → `season-setup/2026-fall-rosters.md`
  (Mussels + Thunder authoritative; opponents best-effort, flagged).
- [x] Confirmed the data model + exact docs the reset must touch (Phase 1a).

---

## 🧱 Phase 1 — Foundational (before / at season start)

### 1a. Archive last season, then reset for the new one
- [x] Raw JSON snapshot saved (done above).
- [ ] 🔴 **Decide the "reference last year" UX** — pick one:
  - **(A)** Static read-only HTML page ("Spring 2026 Archive") that loads the snapshot JSON and shows final standings + batting/pitching/advanced. Simplest, permanent, zero risk. *(Recommended)*
  - **(B)** In-app **season switcher** — a `seasonId` namespace so the app can toggle live vs archived seasons. Most powerful, biggest build.
  - **(C)** Keep JSON + point the existing `tools/*.html` at it on demand. Cheapest, least polished.
- [ ] Build the chosen archive viewer.
- [ ] 🟠 **RESET live Firestore for the new season** (destructive — do together). Exact ops:
  - `appdata/roster` → set `adata` to **new roster + new schedule + `gameResults:{}`** (keep the settings flags: `ratingsSeeded*`, `swingQualityEnabled`, `errorRbiReviewEnabled`, layout prefs).
  - `games/*` → delete all Spring game docs (`e2,e4,e6,e8,e9,e10,e12,e13,e14,e15,e19,test-sandbox`).
  - `appdata/oppPitcherLog` → **archive then clear** `teams:{}` (fresh league log for fall).
  - Bump `APP_VERSION` + `sw.js` cache after reset so devices pull clean.
  - *(Do NOT run until you're at the keyboard — this wipes the live season.)*

### 1b. New roster (Mighty Mussels)
- [ ] Load the 12-player fall roster (JSON ready in `2026-fall-rosters.md`).
- [ ] 🔴 **Jersey numbers** — all blank right now; add if you want them on cards/lines.
- [ ] Seed ratings for the **2 new players** (Lucas Iskrant, Robbie Trometter) — they have no
  hitting/confidence/discipline/clutch ratings, which the optimal-lineup formula uses.
- [ ] Note departures in your head: Miles Beck (gone), Bodhi Langford (→ Thunder).

### 1c. New schedule
- [ ] 🔴 **Get the fall schedule from you** (dates, opponents, times, locations, home/away).
- [ ] Enter into `A.schedule`. Format per event:
  `{"id":"e1","type":"game","date":"Sep 20, 2026","time":"5:45 pm","title":"@ Thunder","opponent":"Thunder","loc":"...","ha":"away"}`
  (`type:"practice"` for practices; `ha:"home"|"away"`).
- [ ] Rebuild the division master schedule (for league pitch-count tracking) once available.

### 1d. New rules — AA ➜ AAA (⚠️ affects game logic, not just the Rules tab)
- [ ] **Replace the `LMLL_RULES` array** (index.html ~line 9694) with the AAA text
  (`reference/2026-aaa-rules.txt`). Header still says "2026 AA Rules".
- [ ] 🔧 **Age-based pitch limits** — AAA is tiered, app hardcodes 75:
  - 9–10 yo → **75** · 11–12 yo → **85** · 13–16 yo → **95** per day.
  - Needs a **per-player age/birth-year** field → drives the pitch-count warning ceiling. 🔴 need ages.
- [ ] 🔧 **Stealing rules (new in AAA — richer than AA).** App already logs steals/CS; add rules ref + optional validations/warnings:
  - No leadoffs; runner may leave only after ball reaches batter / is hit; **steal only once ball crosses the plate** (early = warning, 2nd = out).
  - Steal via straight steal, passed ball, or wild pitch. **Double steals** (1st+2nd) allowed.
  - **One base per batter** per runner. **One steal of home per inning** per team.
  - **No** advance on errant *catcher* throw during a steal; **+1 base** on errant *pickoff* throw.
  - **No delayed steals.** May lead/steal on a **dropped 3rd strike** (which is an out regardless).
- [ ] 🔧 **8-or-fewer players:** AAA assesses the automatic out **only in playoffs** (AA did it always). Check the app's `autoOut` path doesn't auto-out a short lineup in the regular season.
- [ ] 🔧 **Walk cannot advance runner to 2nd** (AAA rule D.13) — verify base-advance logic on BB.
- [ ] ✔️ **Verify still-true (likely unchanged):** 6-run half-inning cap (no cap in last inning), mercy = 10+ after 4 (3½ home), infield-fly, dropped-3rd = out, head-first-slide-while-advancing = out, bunting allowed (no slap/slug), max 1 intentional walk/batter, 3-HBP → pitcher removed.
- [ ] Re-test the pitch-count "days of rest" helper against AAA §7 (unchanged: 0/1/2/3/4 at 20/35/50/65/66+) and the **40-pitch → ineligible next game** rule (unchanged; suspended in playoffs).

---

## 🎨 Phase 2 — Interface / graphics / features ("better than GameChanger")

GameChanger (gc.com/baseball) is the bar. We won't do live streaming — but here's the
backlog of things worth borrowing **and improving**. Rough priority order.

### Already prototyped (pull into the app proper)
- [ ] 💡 **Spray charts** — `tools/pitcher_spray_charts.html` exists; make a clean batter + pitcher
  version inside the app (per-player card). Improve on GC: color by hardness + outcome, jittered.
- [ ] 💡 **Pitches-per-out / efficiency** (`tools/diag_pitches_per_out.html`) → in-app pitcher page. (P/O column already shipped v2.40.)
- [ ] 💡 **Balls-in-play contact profiles** (`tools/pitcher_balls_in_play.html`) → in-app.

### High-value new (AAA rest rules make these matter)
- [ ] 💡 **"Who can pitch today" availability board** — given each pitcher's last outing + AAA
  rest table (0/1/2/3/4 days) + the 40-pitch-next-game rule, show green/yellow/red per kid on
  game day. GC surfaces counts; **we'd surface eligibility**, which is what a coach actually needs.
- [ ] 💡 **Live pitch-count ceiling per pitcher** using the age-based limit (75/85/95) with a
  visual "X left / must come out" warning mid-game.
- [ ] 💡 **Shareable post-game recap graphic** — one image: score, line, top performers, win-prob
  swing. (Better than GC's plain box score.)

### Nice-to-have / polish
- [ ] 💡 Win-probability / game-flow chart per game.
- [ ] 💡 Player season cards (photo optional, splits, trends, hot/cold last-3 using the recency weighting we built).
- [ ] 💡 Play-by-play feed polish (the `experimentalPlaysLayout` cards).
- [ ] 💡 Situational splits (vs LHP/RHP not relevant at this level, but count/base-state splits are).
- [ ] 💡 Field graphic sizing pass (was fiddly last season — lock full-width, capped height).
- [ ] 💡 Optimal-lineup explainer UI (surface *why* a kid is ranked, using the score components).

### Interface/tech debt
- [ ] Single-file app is ~10k+ lines — consider a light split (or at least section index) before the feature push.
- [ ] Service-worker version discipline (already on `mm-vX.Y`).

---

## 📥 Inputs I still need from you (blockers)
1. 🔴 **Fall schedule** — dates / opponents / times / locations / home-away.
2. 🔴 **Player ages or birth-years** (for AAA age-based pitch limits 75/85/95). Jersey numbers too if you want them.
3. 🔴 **Archive UX choice** — A (static viewer), B (season switcher), or C (JSON + tools). *(A recommended.)*
4. 🔴 **When to run the reset** — it's destructive; we'll do it together, timed to the season start.
5. 🟡 **Confirm opponent rosters** — best-effort draft in `2026-fall-rosters.md` (Hurricanes/Iron Pigs split + Nationals partial names need a look).

---

## 📁 Where things live
- `archive/2026-spring/` — last season snapshot + README (the safety net).
- `reference/2026-aaa-rules.txt` — full AAA rulebook text (for the rules rewrite).
- `season-setup/2026-fall-rosters.md` — new rosters (Mussels ready to paste).
- `season-setup/SEASON_SETUP.md` — this file.
