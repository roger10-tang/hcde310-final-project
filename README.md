# GolfFinderUW

This is the current interest feature for our HCDE 310 project. Students can post a tee time, add or remove interest, and see the saved count. GolfCore and Open-Meteo are not connected yet.

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

The app creates its data folder on the first run. Posts and interests start empty. The local session key is kept in data/.session-key so a restart does not change the browser's identity. Do not share this file. FLASK_SECRET_KEY can also be supplied as a shell environment variable. The app does not automatically load a .env file.

Read HANDOFF.md before merging this work. It explains ownership, the temporary posting form, and the fields the interest feature uses. This is a local, single-process prototype. It is not the complete HW6 submission.
