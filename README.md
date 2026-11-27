# GolfFinderUW

This is the current interest feature for our HCDE 310 project. Students can post a tee time, add or remove interest, and see the saved count. Each posted tee time also shows the course's official name and city from GolfCore and the chance of rain at that hour from Open-Meteo.

Use Python 3.10 or newer. From this folder, run:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open http://127.0.0.1:5050. Enter a future tee time, then try the interest button. Use a different browser or a private window for a separate student session. Two ordinary tabs in the same browser share a session.

Run the checks with:

```sh
.venv/bin/python -m pytest -q
```

The two APIs need no setup to try the app. GolfCore answers without a key today and will require one from December 4, 2026, so register for a key and set it before then. Open-Meteo needs no key. Copy .env.example to .env and fill in your own GOLFCORE_API_KEY; the app reads .env on startup. Keep .env out of Git. If either API is unreachable, the tee times still appear and the weather line reads "Weather unavailable".

The app creates its data folder on the first run. Posts, interests and cached courses start empty. Course coordinates are remembered in data/courses.json so each course costs one GolfCore request instead of one per page load. The local session key is kept in data/.session-key so a restart does not change the browser's identity. Do not share this file. FLASK_SECRET_KEY can also be set in .env or in the shell. A variable set in the shell overrides .env.

Read HANDOFF.md before merging this work. It explains ownership, the temporary posting form, and the fields the interest feature uses. This is a local, single-process prototype. It is not the complete HW6 submission.
