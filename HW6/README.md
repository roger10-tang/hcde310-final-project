# Roger's interest feature

Create a virtual environment first with `python3 -m venv .venv`. Install the dependencies with `.venv/bin/python -m pip install -r requirements.txt`. Run the app from the repository folder with `.venv/bin/python app.py`, then open http://127.0.0.1:5050. Run the checks with `.venv/bin/python -m pytest -q`.

Enter a future tee time in the manual form, then click "I'm interested". Click again to remove interest. Open another browser or private window to try a separate student session. Separate tabs in the same browser share the same student session.

Data is saved in data/tee-times.json, data/interests.json and data/courses.json. Missing files start as empty lists. A local session key is generated in data/.session-key so the browser session can survive a restart. The data folder is ignored by Git. FLASK_SECRET_KEY and GOLFCORE_API_KEY can be set in .env, which the app reads on startup, or in the shell, which takes priority. Copy .env.example to .env to fill in your own values.

This is a local prototype using one server process. The file lock protects requests in that process. It is not shared storage for multiple server processes.

The manual form temporarily stores courseName in each post. The final course/API integration should map posts to courseId as planned in P2. Interest records already use the P2 keys interestId, postId, and studentId.

The course and weather APIs are connected in api.py, and each card shows the course's city and the hourly chance of rain. The final date-based browse flow, the team diagram and the final recording are not complete. The data folder is ignored by Git. Each person starts with an empty local app and creates their own test posts.
