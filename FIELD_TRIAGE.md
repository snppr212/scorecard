# Field Triage — Game Day

**Game:** Mussels @ Hot Rods · 1:00 pm · South Ardmore Park Field C
**App version:** `mm-v30` (check service worker)
**Repo:** snppr212/scorecard

---

## Before the game

1. **Hard refresh on your phone.**
   - iOS: close the PWA fully, swipe up from app switcher, reopen.
   - Android: close PWA, reopen. If still old, clear cache once.
2. Confirm you're on **v30** — the field graphic should show:
   - solid green field, wide angle from home plate
   - position labels (P, C, 1B, …) in dark boxes that turn gold + show first names when assigned
   - **runners are big gold circles** sitting on the bases with first name inside
   - home plate point faces **down** toward the catcher
3. **Test Sandbox first.** Tap the gold 🧪 **Test Sandbox** button above the schedule. It spins up a fake game (`vs TEST OPPONENT`) you can run without polluting real data.
4. When done testing, tap the red **Wipe test data** button. It clears the sandbox G state, the gameResults entry, any pitchLog entries tagged `eventId='test-sandbox'`, and removes the sandbox from the schedule.
5. Then tap the real **Mussels @ Hot Rods** game.

---

## What to test in the sandbox

- Lineup builder + position assignments (drag/select for all 9–10)
- First pitch → at-bat flow → result buttons
- Pitch count thresholds: **40+ amber**, **65+ red**, **75 hard stop modal**
- HBP routing (3 HBP block)
- Force play / steal logic on bases
- DP / SAC / RBI validation
- Mid-game pitcher switch
- End game flow → summary tab

---

## During the game — quick reference

| Situation | Where to tap |
|---|---|
| Set/swap pitcher | Pitcher line on the matchup bar |
| Move/score a runner | Tap the gold circle on that base |
| Assign a fielder | Field tab → tap the position label |
| Mark a run / error | At-bat result buttons |
| Override a pitch | "..." override on the count bar |

**Pitch count colors:** green <40, amber 40+, red 65+, hard stop at 75.

---

## Known quirks to watch

- **Resume modal**: tapping a game with saved data shows 3 buttons — *Resume*, *Start fresh (erase data)*, *Cancel*. Don't hit "Start fresh" mid-game by accident.
- **Firebase sync**: changes save locally first, then push to Firestore in the background. If the field is spotty, the app keeps working — it just queues the sync.
- **Test sandbox is hidden** from the schedule list and the W-L record, so you won't see it once wiped.

---

## If something is broken

1. Note exactly which tap caused it (screen + button).
2. Screenshot if you can.
3. Tap **another** tab and back — most rendering glitches re-resolve.
4. As a last resort: close PWA, reopen. State persists in localStorage AND Firestore so you won't lose data.

---

## Recent commits (most recent first)

- `180a1c3` Field: bigger runner circles centered on bases for visibility
- `a403381` Field labels: show player first name; position name is placeholder
- `6ccd8f9` Field graphic: position name labels, visible dirt + mound, infielders behind bases
- `a341125` Restore v22 field graphic (solid green, wide angle), flip home plate
- `49f59f0` Add Test Sandbox game mode for safe pre-game testing
- `64ee616` Add Resume modal with clear labels + auto-cleanup test data
- `d82b444` Fix infinite recursion in sa/sg Firebase wrappers (the "tapping a game does nothing" bug)
