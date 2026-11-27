---
trigger: always_on
description: Automatically sync, read, and update the Ocean Saga character database and user roster with GitHub (tsyt-dev/ocean-saga-db).
---

# Ocean Saga Auto-Sync Rule

When working in this workspace (`ocean-saga-db` / `OP_Cha`) on any Ocean Saga question, team-building request, or roster update:

1. **Auto-Sync & Auto-Read (Start of Task):**
   - Run `git pull --rebase` first to make sure local files have the latest updates from other machines.
   - Read `ข้อมูล/Ocean_Saga_AI_Context_Export.md` as the primary context (current ID roster, verified `Real Tier List`, and current recommended team).
   - Use `ข้อมูล/characters_th.json` (and `ข้อมูล/analysis_results.json`) whenever checking exact character stats or skill descriptions — do NOT re-scrape `guragon.com`.
   - Always prioritize the verified `Real Tier List` (current server patch: Ace & Sabo + Boa Lilith) over future-patch units unless the user asks about future meta.
   - Standard team formation is 6 heroes: 2 Front-line and 4 Back-line.

2. **Auto-Update & Auto-Push (Whenever Roster/Team/Tier List Changes):**
   - Whenever the user adds new characters, changes star levels, switches IDs, or updates the Real Tier List:
     1. Update both `ข้อมูล/Ocean_Saga_AI_Context_Export.md` and `ข้อมูล/Ocean_Saga_AI_Context_Export.json`.
     2. Run `git add .`, commit with a clear message (e.g. `Update roster: <summary>`), and run `git push` to `origin main` automatically so all other machines stay in sync.
   - Never commit secrets, passwords, or temporary cache files.
