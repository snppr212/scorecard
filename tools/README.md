# Tools — Firestore push utilities

These tools let you write directly to the production Firestore (`diamond-statz`) without going through the app's in-app paste flows. They use the same client-side Firebase config the app uses.

## File naming convention

- `push_league_pool.html` + `import_league_pool.py` — the original league pool toolchain (xlsx → JSON → Firestore). See [§ League Pool Management](#league-pool-management) below.
- `push_<thing>.html` — one-shot pushes for specific data drops. Hardcoded data, single button. Kept as an audit trail of what was pushed when.

## Audit log

Each row is a one-shot push that was created in a Claude session and run by the user. Re-running any of them is safe (all are idempotent — pitcher logs dedupe by team+pitcher+date, standings overwrite cleanly).

| Date created | File | What it pushed | Status |
|--------------|------|----------------|--------|
| (initial)    | `push_league_pool.html` | `appdata/leaguePool` (full season eval data, generic — takes pasted JSON) | reusable per-season |
| 2026-05-14   | `push_lugnuts_pitcher_log.html` | Lugnuts: 11 outings across 3 games (Apr 12 / Apr 30 / May 9) | run, then superseded |
| 2026-05-14   | `push_opp_pitcher_log.html` | Iron Pigs (Apr 23) + Bulls (May 6) + Grasshoppers (May 9) — 10 outings | run via push_all_pending |
| 2026-05-14   | `push_league_standings.html` | `appdata/leagueStandings` — May 14 LMLL AA snapshot (12 teams, us 3-4 / -19 SD) | run via push_all_pending |
| 2026-05-14   | `push_all_pending.html` | Combined: standings + all 4 teams' pitcher logs (21 outings, 6 games) | run — most recent |

The three "superseded" files are kept for audit; `push_all_pending.html` writes the same data (plus standings) in one click.

## Adding a new push tool

For a new data drop, copy `push_all_pending.html`, edit the `STANDINGS` / `OPP_OUTINGS` constants, rename to something date- or topic-specific, and add a row to the audit log. The skeleton is small (Firebase init + one async push function + idempotent merge logic). Then:

```bash
open tools/push_<your_new_file>.html
```

…and click the button.

---

## League Pool Management

These two tools let you update the LMLL eval data in Firestore without releasing the app.

## When to use this

- **Before each new season** — once the league publishes the draft results, run the import to refresh the player pool with new ratings/teams
- **Mid-season corrections** — if a kid moves teams, gets re-evaluated, etc.
- **Other leagues** (future) — point at a different draft xlsx and use a different `--season` tag

## Step 1: Generate JSON from xlsx

```bash
python3 tools/import_league_pool.py /path/to/AA-2027-Draft.xlsx --season 2027-AA
```

Output:
- Writes `/tmp/league_pool_<season>.json` with all 130-ish players
- Stderr shows any kids that didn't match a Big Board entry (usually ones who weren't evaluated by the coach pool)
- Stderr also prints the next-step push instructions

## Step 2: Push to Firestore

**Option A — browser tool (easiest):**

Open `tools/push_league_pool.html` directly in your browser:

```bash
open tools/push_league_pool.html       # macOS
xdg-open tools/push_league_pool.html   # Linux
```

Then:
1. Paste the contents of `/tmp/league_pool_<season>.json` into the Players textarea
2. Set the season tag (e.g. `2027-AA`)
3. Click **Push to Firestore**
4. Confirm the count looks right
5. Reload the running app — eval features now use the new data

**Option B — DevTools console:**

1. Open the deployed app at https://snppr212.github.io/scorecard
2. Open DevTools (F12)
3. Paste:

```js
const players = /* paste contents of /tmp/league_pool_<season>.json here */;
await db.collection('appdata').doc('leaguePool').set({
  season: '2027-AA',
  league: 'LMLL',
  updated: new Date(),
  players: players
}, {merge: false});
```

## What gets pushed

The `appdata/leaguePool` doc has shape:

```js
{
  season: '2026-AA',
  league: 'LMLL',
  updated: <Timestamp>,
  players: {
    '<canonical name>': {
      team: 'Hurricanes',          // matches OPP_ROSTERS keys
      evalTier: 1,                  // 1-12 (Sam's projection grouping)
      evalScore: 88.5,              // 0-100 composite
      hitting: 4.9, throwing: 3.62, // 1-5 ratings
      fielding: 3.8, pitching: 4.25,
      samPitching: 4.0,             // private rating, where given
      districtTeam: true,           // travel-team flag
      school: 'Penn Wynne'
    },
    ...
  }
}
```

## Schema requirements for the xlsx

The script expects two sheets:

### `Big Board` sheet
Columns: `Name`, `Round`, `Adj Eval Score`, `Hitting`, `Throwing`, `Fielding`, `Pitching`, `Sam's`, `District Team`, `School`. Other columns are ignored.

### `Draft` sheet
- Row 1: team headers in specific columns (auto-detected by scanning row 1)
- Rows 7-18: each round's pick per team

If the xlsx layout changes year-to-year, edit `tools/import_league_pool.py` accordingly. The parser is tolerant but expects roughly the 2026 structure.

## Name canonicalization

The script applies these fixes to match the app's `OPP_ROSTERS` naming:

- `Brady Duncan` → `Brady S. Duncan`
- `*Josh Land*` → `Jack Land` (asterisks stripped, name normalized)
- `Neel KHATNANI` → `Neel Khatnani`
- `owen tatlow` → `Owen Tatlow`

Edit `CANONICAL` in `import_league_pool.py` to add new mappings.

## Code paths that use this data

- `_getLeaguePlayer(name)` — case-insensitive lookup
- `_getTeamRoster(teamName)` — full roster sorted by eval score
- `_getLeagueCutoffs()` — Q3 and top-15 thresholds for danger-stretch alerts
- `_evalBadge(name)` — inline badge HTML for matchup bar / opp picker
- `openScoutCard(team)` — pre-game scouting modal
- `_evalDangerCheck()` — fires danger-stretch toasts in-game

All gated by `A.evalDisplayEnabled` (toggleable in Roster modal).
