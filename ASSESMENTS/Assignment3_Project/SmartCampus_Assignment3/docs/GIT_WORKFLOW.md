# Git / GitHub workflow evidence
Use feature branches for separate work and protect the main branch. Suggested branches:
- `feature/booking-overlap`: booking overlap prevention and validation.
- `feature/ticket-sla`: maintenance ticket status and SLA fields.
- `fix/duplicate-sensor-event`: idempotent sensor event ingestion.

For each pull request include: issue link, purpose, changed files, tests run, screenshots if UI changes, reviewer decision and merge result. Use small meaningful commits. Keep `.env`, credentials, database dumps and generated build output out of Git.

Conflict demonstration: both branches edit the same booking overlap policy. Merge branch A first, then merge branch B and resolve the marked conflict by preserving the stricter validation. Record the real Git output and final commit in the report after performing it.
