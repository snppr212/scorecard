#!/usr/bin/env python3
"""
import_league_pool.py — Update the LMLL eval data in Firestore from a draft xlsx.

Usage:
    python3 tools/import_league_pool.py /path/to/AA-2027-Draft.xlsx [--season 2027-AA]

What it does:
1. Reads the Big Board sheet (eval ratings per kid)
2. Cross-references with the Draft sheet (team assignments)
3. Builds the league-player pool data structure
4. Writes a JSON file ready to push to Firestore appdata/leaguePool

The Firestore push step is manual (paste into the browser console of the
running app) so this script doesn't need Firebase credentials. Output the
JSON to stdout + save to /tmp/league_pool_<season>.json.

Schema requirements (xlsx must have):
- "Big Board" sheet with columns: Name, Round, Adj Eval Score, Hitting,
  Throwing, Fielding, Pitching, Sam's, District Team, School
- "Draft" sheet with team headers in row 1 and player names in round
  rows (rows 7-18) per team column

Tested against the 2026 AA draft. Adjust if the spreadsheet layout
changes year-to-year.
"""
import sys
import json
import argparse
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Missing pandas. Install: pip3 install pandas openpyxl", file=sys.stderr)
    sys.exit(1)


# Name canonicalizations applied at write time (in case the xlsx has variations)
CANONICAL = {
    'Brady Duncan': 'Brady S. Duncan',
    '*Josh Land*': 'Jack Land',  # asterisks → strip; Josh = Jack per coach
    'Neel KHATNANI': 'Neel Khatnani',
    'owen tatlow': 'Owen Tatlow',
}


def cleanf(v):
    return float(v) if pd.notna(v) else None


def cleans(v):
    return str(v).strip() if pd.notna(v) else None


def normalize(name):
    """Apply canonicalizations and strip stray asterisks."""
    if not name:
        return name
    n = str(name).strip().replace('*', '')
    return CANONICAL.get(n, n)


def parse_big_board(xl):
    """Read Big Board sheet, return name → eval-data dict (case-insensitive keys)."""
    bb = pd.read_excel(xl, sheet_name='Big Board')
    bb = bb[bb['Name'].notna()].copy()
    out = {}
    for _, r in bb.iterrows():
        raw_name = normalize(r['Name'])
        key = raw_name.lower()
        out[key] = {
            'evalTier': int(r['Round']) if pd.notna(r['Round']) else None,
            'evalScore': cleanf(r['Adj Eval Score']),
            'hitting': cleanf(r['Hitting']),
            'throwing': cleanf(r['Throwing']),
            'fielding': cleanf(r['Fielding']),
            'pitching': cleanf(r['Pitching']),
            'samPitching': cleanf(r["Sam's"]),
            'districtTeam': str(r['District Team']).strip().upper() == 'Y' if pd.notna(r['District Team']) else False,
            'school': cleans(r['School']),
        }
    return out


def parse_draft_teams(xl):
    """Read Draft sheet, return team → list of player names (in roster order)."""
    df = pd.read_excel(xl, sheet_name='Draft', header=None)
    # Find team header columns in row 1
    team_cols = {}
    for c in range(df.shape[1]):
        v = df.iat[1, c]
        if isinstance(v, str) and v.strip():
            s = v.strip()
            # Filter out non-team header strings
            if s.upper() == s.lower():  # purely numeric
                continue
            if s in ('TEAM',):
                continue
            # Heuristic: if there's a player name in the row 7 same column, it's a team
            if pd.notna(df.iat[7, c]):
                team_cols[s] = c
    # Pull rosters
    rosters = {}
    for team, col in team_cols.items():
        roster = []
        for r in range(7, 19):  # rounds 1-12
            n = df.iat[r, col]
            if pd.notna(n) and isinstance(n, str) and n.strip():
                roster.append(normalize(n))
        rosters[team] = roster
    return rosters


def build_league_pool(big_board, draft_teams, opp_team_key_map):
    """
    Build the LEAGUE_PLAYERS dict, keyed by canonical name.
    opp_team_key_map: maps Draft-sheet team names → app-internal team names.
    """
    pool = {}
    unmatched = []
    for draft_team_name, roster in draft_teams.items():
        app_team = opp_team_key_map.get(draft_team_name, draft_team_name)
        for name in roster:
            eval_data = big_board.get(name.lower(), {})
            if not eval_data:
                unmatched.append((draft_team_name, name))
            pool[name] = {
                'team': app_team,
                **eval_data,
            }
    return pool, unmatched


# Map from Draft sheet team labels → app-internal labels (matches OPP_ROSTERS keys)
DRAFT_TO_APP_TEAM = {
    'IRON PIGS': 'Iron Pigs',
    'CANNONBALLERS': 'Cannonballers',
    'Thunder': 'Thunder',
    'Devil Rays': 'Devil Rays',
    'Da Bulls': 'Bulls',
    'Hot Rods': 'Hot Rods',
    'Lug Nuts': 'Lugnuts',
    'Hurricanes': 'Hurricanes',
    'Grasshoppers': 'Grasshoppers',
    'Mud Hens': 'Mud Hens',
    'Mighty Mussels': 'Mighty Mussels',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xlsx', help='path to draft xlsx')
    ap.add_argument('--season', default='2026-AA', help='season tag (e.g. "2026-AA")')
    ap.add_argument('--league', default='LMLL', help='league name (default LMLL)')
    ap.add_argument('--out', default=None, help='output JSON file (default /tmp/league_pool_<season>.json)')
    args = ap.parse_args()

    xlsx_path = Path(args.xlsx)
    if not xlsx_path.exists():
        print(f'File not found: {xlsx_path}', file=sys.stderr)
        sys.exit(1)

    xl = pd.ExcelFile(xlsx_path)
    print(f'Sheets in workbook: {xl.sheet_names}', file=sys.stderr)

    big_board = parse_big_board(xl)
    print(f'Big Board: {len(big_board)} rated players', file=sys.stderr)

    draft_teams = parse_draft_teams(xl)
    print(f'Draft sheet teams: {list(draft_teams.keys())}', file=sys.stderr)

    pool, unmatched = build_league_pool(big_board, draft_teams, DRAFT_TO_APP_TEAM)
    print(f'\nPool size: {len(pool)} players', file=sys.stderr)
    if unmatched:
        print(f'\nWARNING: {len(unmatched)} players have no Big Board eval data:', file=sys.stderr)
        for team, name in unmatched:
            print(f'  - {team}: {name}', file=sys.stderr)

    out_path = Path(args.out) if args.out else Path(f'/tmp/league_pool_{args.season}.json')
    out_path.write_text(json.dumps(pool, indent=2, default=str))
    print(f'\nWrote {out_path}', file=sys.stderr)
    print(f'Total bytes: {len(out_path.read_text())}', file=sys.stderr)

    # Print a Firebase-paste snippet for next step
    print('', file=sys.stderr)
    print('=' * 60, file=sys.stderr)
    print('NEXT STEPS — push to Firestore:', file=sys.stderr)
    print('=' * 60, file=sys.stderr)
    print('', file=sys.stderr)
    print('Option A: One-time push from the running app via console:', file=sys.stderr)
    print('  1. Open the deployed app in a browser', file=sys.stderr)
    print('  2. Open DevTools console (F12)', file=sys.stderr)
    print('  3. Paste this:', file=sys.stderr)
    print('', file=sys.stderr)
    print(f'  await db.collection("appdata").doc("leaguePool").set({{', file=sys.stderr)
    print(f'    season: "{args.season}",', file=sys.stderr)
    print(f'    league: "{args.league}",', file=sys.stderr)
    print(f'    updated: new Date(),', file=sys.stderr)
    print(f'    players: {json.dumps(pool)[:80]}... // see {out_path}', file=sys.stderr)
    print(f'  }}, {{merge: false}});', file=sys.stderr)
    print('', file=sys.stderr)
    print(f'  (For the players blob, paste the contents of {out_path} as the value)', file=sys.stderr)
    print('', file=sys.stderr)
    print('Option B: Use the helper page in tools/push_league_pool.html (TODO)', file=sys.stderr)


if __name__ == '__main__':
    main()
