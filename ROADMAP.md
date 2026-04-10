# Mighty Mussels Scorecard — Roadmap

## Status Key
- ✅ Done
- 🔄 In Progress / Needs Verification
- 📋 Planned
- 💡 Idea / Future

---

## Core Scoring & At-Bat

| Feature | Status | Notes |
|---------|--------|-------|
| Ball/Strike/Out counter | ✅ | |
| Pitch sequence display (real-time) | ✅ | Fixed v15 — renderCB ID mismatch was root cause |
| Previous AB pitch sequence (faded) | ✅ | v14 — G.lastABPitches |
| All result buttons (1B/2B/3B/HR, outs, FC, DP, etc.) | ✅ | |
| Undo last pitch | ✅ | |
| Undo last AB | ✅ | |
| Runner advancement (SB, CS, WP, etc.) | ✅ | |
| Auto-advance to next batter | ✅ | |

---

## Pitcher Tracking & Limits

| Feature | Status | Notes |
|---------|--------|-------|
| Pitch count per pitcher | ✅ | |
| Pitch type breakdown (SW/LK/FO/BA/BIP) | ✅ | |
| HBP counter per pitcher | ✅ | v10 |
| **21-pitch threshold popup** | ✅ | v15 fix |
| **36-pitch threshold popup** | ✅ | v15 fix |
| **40-pitch threshold popup** | ✅ | v15 fix — user may want to verify in real game |
| **51-pitch threshold popup** | ✅ | v15 fix |
| **65-pitch threshold popup** | ✅ | v15 fix |
| **66-pitch threshold popup** | ✅ | v15 fix |
| **75-pitch hard block (our pitcher)** | ✅ | v14/v15 — modal with Make Change + Override |
| **75-pitch notify (opponent pitcher)** | ✅ | v14/v15 — notify umpire modal |
| **3-HBP forced removal (our pitcher)** | ✅ | v14 — block modal |
| **3-HBP forced removal (opponent)** | ✅ | v14 — notify umpire modal |
| Threshold checks on ALL AB outcomes | ✅ | v13/v14 — chkPW in finAB |
| Override rule violation option | ✅ | v14 — red button with confirm dialog |
| Pitching change UI | ✅ | |
| Innings pitched tracking | ✅ | |

---

## Fielding & Lineup

| Feature | Status | Notes |
|---------|--------|-------|
| 9-player field positions | ✅ | |
| 10-player with RCF (was 4OF) | ✅ | v10/v11 |
| CF left of center / RCF right of center | ✅ | v11 |
| RCF counts in innings-per-player | ✅ | v10 — getActivePOS() fix |
| Innings per player tracking | ✅ | |
| Minimum play rule warnings | ✅ | |
| Catcher pitch-count limit | ✅ | |
| DNP / availability tracking | ✅ | |

---

## Field Graphic

| Feature | Status | Notes |
|---------|--------|-------|
| Solid green rectangle background | ✅ | v12 |
| Removed fake outfield wall arc | ✅ | v12 |
| Base paths and diamond | ✅ | |
| Player position dots | ✅ | |
| Runner indicators on bases | ✅ | |

---

## Matchup Bar

| Feature | Status | Notes |
|---------|--------|-------|
| Our pitcher name + pitch count | ✅ | |
| Opponent batter name | ✅ | |
| Opponent batter jersey number | ✅ | v10 |
| HBP count shown on pitcher | ✅ | v10 |

---

## Game Management

| Feature | Status | Notes |
|---------|--------|-------|
| Home/Away team setup | ✅ | |
| Inning-by-inning scoring | ✅ | |
| Box score | ✅ | |
| Play log | ✅ | |
| Mercy rule (10-run) | ✅ | |
| 6-run half-inning rule | ✅ | |
| End game | ✅ | |
| Share/Export | ✅ | |

---

## PWA / Technical

| Feature | Status | Notes |
|---------|--------|-------|
| Installable PWA | ✅ | |
| Service worker cache (v15) | ✅ | |
| Offline play | ✅ | |
| localStorage persistence | ✅ | |
| GitHub Pages deployment | ✅ | snppr212/scorecard |

---

## Potential Future Enhancements

| Feature | Status | Notes |
|---------|--------|-------|
| Rest day calendar (track when pitcher can pitch again) | 💡 | Show "eligible again: Apr 12" |
| Print-friendly scoresheet | 💡 | |
| Photo capture for lineup card | 💡 | |
| Push notifications for game day | 💡 | |
| Season stats aggregation | 💡 | |
| Email/text game summary | 💡 | |

---

## Known Issues / Needs Verification

| Issue | Status |
|-------|--------|
| 40-pitch popup — user may have missed it in real game testing; confirmed working in preview | 🔄 Verify in real game |
| Undo pitch across AB boundary edge cases | 🔄 Monitor |
