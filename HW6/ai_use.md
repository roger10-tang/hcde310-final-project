# HW6 AI Use

[Course AI Use Card](https://canvas.uw.edu/courses/1959879/pages/ai-use-card)

This covers our AI use since P2 (submitted 2026-11-22).

## Won

AI draft: check me. 2026-11-26 — Claude Code (Opus): read every file in the repo and explained what each one does, then checked the repo against the HW6 criteria. No project files changed.

AI draft: check me. 2026-11-26 — Claude Code (Opus): created the virtual environment, ran app.py, and drove the posting and interest flow with curl to confirm the saved JSON is read back after an app restart. No project files changed.

AI draft: check me. 2026-11-26 — P1/ai_use.md, P2/ai_use.md, .github/copilot-instructions.md: Claude Code restored these three files from main after the HW6 branch deleted the two AI-use logs and removed the wrap-up rule that asks for an AI-use entry.

AI draft: check me. 2026-11-26 — HW6/ai_use.md: Claude Code drafted this file from the repository's Git history and from its own actions in that session.

AI draft: check me. 2026-11-26 — api.py: new file. Claude Code wrote find_course() for the GolfCore Course Data API and rain_chance() for the Open-Meteo Forecast API. Both return None instead of raising, so a failed lookup never hides a posted tee time.

AI draft: check me. 2026-11-26 — api.py: Claude Code changed find_course() to report three outcomes (course found, no such course, GolfCore unreachable) so a course name GolfCore does not know is only looked up once instead of on every page load. This protects the free plan's 500 requests per month.

AI draft: check me. 2026-11-26 — app.py: Claude Code added course_for(), which remembers found courses in data/courses.json, and changed index() to pass each post's course and rain chance to the template.

AI draft: check me. 2026-11-26 — templates/index.html: Claude Code added the course's official name and city from GolfCore, and the rain chance line that falls back to "Weather unavailable".

AI draft: check me. 2026-11-26 — conftest.py: new file. Claude Code turned the course and forecast lookups off during tests, so the suite runs with no network and spends no API quota.

AI draft: check me. 2026-11-26 — .env.example, requirements.txt: Claude Code added the GOLFCORE_API_KEY name and the requests dependency.

AI draft: check me. 2026-11-26 — Claude Code ran both APIs live to check the code, confirmed a 14:30 tee time reads the 14:00 forecast row, and confirmed every tee time still appears with "Weather unavailable" when both APIs are unreachable.

AI draft: check me. 2026-11-26 — app.py, requirements.txt: Claude Code added python-dotenv and a load_dotenv() call so the app reads .env on startup. We chose this because the assignment describes .env.example as a file a partner copies to .env. A variable set in the shell still overrides .env.

AI draft: check me. 2026-11-26 — README.md, HW6/README.md: Claude Code corrected the sentences saying GolfCore and Open-Meteo were not connected, documented the GOLFCORE_API_KEY setup and the December 4, 2026 key deadline, and added data/courses.json to the list of saved files.

AI draft: check me. 2026-11-26 — Claude Code copied the project to a separate folder with no .venv, no data and no .env, installed from requirements.txt, ran the tests and the app, and posted a tee time, to check that a partner can run the project from a fresh copy.

AI draft: check me. 2026-11-26 — no files changed. Claude Code pointed out that GolfCore's API key becomes required on December 4, 2026, the same day as our planned user test, and that a rejected key would quietly show "Weather unavailable" on every card. We decided to register for a key before the test rather than rely on the fallback.

## Roger

<!-- Roger: describe the AI use behind commit 62bccf4 "Add saved interests and live counts for HW6"
     (app.py, templates/index.html, static/counts.js, tests/test_interest.py, HW6/spec.md,
     HW6/my_part.md, HANDOFF.md). Which tool, what it wrote, what you wrote or changed yourself.
     Write "No AI used" if that is the case. -->

## Reflection  

