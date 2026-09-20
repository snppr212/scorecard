# Archive — Spring 2026 season (AA division)

Read-only snapshot of the **entire Spring 2026 season**, pulled from Firestore
(project `diamond-statz`) on **2026-09-19** via the REST API before any
new-season reset. Nothing here has been altered.

## Files (raw Firestore REST JSON — nested `mapValue`/`stringValue` shape)
| File | Firestore doc | Contents |
|---|---|---|
| `appdata_roster.json` | `appdata/roster` | `adata`: roster (12 players), schedule (18 events), gameResults, all app settings |
| `appdata_oppPitcherLog.json` | `appdata/oppPitcherLog` | League-wide opponent pitch-count log (11 opponent teams) |
| `games_page1.json` | `games/*` | 11 game scorecards + `test-sandbox` (full pitch-by-pitch `gdata`) |

Game docs: `e2, e4, e6, e8, e9, e10, e12, e13, e14, e15, e19` (+ `test-sandbox`).
`gameResults` also lists `e7` and `e17` — rained-out entries with no scorecard (expected, no `gdata`).

## To decode into plain JSON
Every file is Firestore's typed-value format. Convert with the same `conv()`
helper used elsewhere in this repo's tools, e.g.:
```python
import json
def conv(v):
    if 'stringValue' in v: return v['stringValue']
    if 'integerValue' in v: return int(v['integerValue'])
    if 'doubleValue' in v: return float(v['doubleValue'])
    if 'booleanValue' in v: return v['booleanValue']
    if 'timestampValue' in v: return v['timestampValue']
    if 'nullValue' in v: return None
    if 'mapValue' in v: return {k:conv(x) for k,x in v['mapValue'].get('fields',{}).items()}
    if 'arrayValue' in v: return [conv(x) for x in v['arrayValue'].get('values',[])]
    return None
roster = conv(json.load(open('appdata_roster.json'))['fields']['adata'])
```

## Season summary (for quick reference)
- Team: Mighty Mussels, **AA** division, 10 games played (record tracked in-app).
- Roster: Shapiro, Langford, Steinberg, Cobe Bresson, Thomas, Kalman, Hunter Bresson,
  Aronstein, Singer, McPherson, Chatnani, Beck.
- Full stats (batting/pitching/advanced/spray/pitches-per-out) are reproducible from
  these files with the `tools/*.html` diagnostics (repoint them at this JSON, or
  restore to a scratch Firestore project).

## ⚠️ This is the safety net for the reset
The new-season reset (see `season-setup/SEASON_SETUP.md`, Phase 1a) **overwrites**
the live `appdata/roster`, `games/*`, and `appdata/oppPitcherLog`. This archive is
the recovery source if anything needs to be referenced or restored afterward.
