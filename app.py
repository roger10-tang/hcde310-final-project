import json
import os
import secrets
from datetime import datetime
from pathlib import Path
from threading import Lock
from uuid import uuid4
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

import api

# read .env so a partner can copy .env.example and fill in their own keys instead
# of exporting them by hand. Variables already set in the shell win.
load_dotenv()


class _NoLookup:
    """Stand-in for the live APIs so the tests never reach the network."""

    @staticmethod
    def find_course(name):
        return None  # "not reached", so the tests never cache a result

    @staticmethod
    def rain_chance(lat, lng, date, time):
        return None


def create_app(data_dir=None, secret_key=None, lookup=None):
    app = Flask(__name__)
    # tests pass their own lookup, or set GOLFFINDER_OFFLINE=1 to work without network.
    if lookup is None:
        lookup = _NoLookup if os.environ.get("GOLFFINDER_OFFLINE") == "1" else api
    folder = Path(data_dir) if data_dir else Path(__file__).parent / "data"
    folder.mkdir(parents=True, exist_ok=True)
    # keep the local session key between restarts. Never commit it.
    if secret_key is None:
        secret_key = os.environ.get("FLASK_SECRET_KEY")
        if not secret_key:
            key_file = folder / ".session-key"
            if not key_file.exists():
                key_file.write_text(secrets.token_hex(32), encoding="utf-8")
                key_file.chmod(0o600)
            secret_key = key_file.read_text(encoding="utf-8")
    app.config.update(SECRET_KEY=secret_key, SESSION_COOKIE_SAMESITE="Lax")
    file_lock = Lock()

    def load_records(filename):
        try:
            with (folder / filename).open(encoding="utf-8") as source:
                rows = json.load(source)
        except FileNotFoundError:
            return []
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError("Expected a list of records")
        return rows

    def save_records(filename, rows):
        temporary = folder / (filename + ".tmp")
        with temporary.open("w", encoding="utf-8") as destination:
            json.dump(rows, destination, indent=2)
        temporary.replace(folder / filename)

    @app.before_request
    def identify_browser():
        if "studentId" not in session:
            session["studentId"] = uuid4().hex
            session["formToken"] = secrets.token_hex(24)
        if request.method == "POST":
            token = request.form.get("formToken", "")
            if not secrets.compare_digest(token, session.get("formToken", "")):
                return "Please reload the page and try again.", 400

    def post_state(post_id, interests):
        matches = [row for row in interests if row.get("postId") == post_id]
        return {
            "count": len(matches),
            "interested": any(row.get("studentId") == session["studentId"] for row in matches),
        }

    def course_for(name, known, added):
        """Return the course for this name, asking GolfCore only the first time.

        A course's coordinates never change, so a found course is remembered in
        courses.json. That spends the free GolfCore quota once per course instead
        of on every page load.
        """
        key = name.casefold()
        if key in known:
            return known[key]
        found = lookup.find_course(name)
        if found is None:
            return None  # GolfCore unreachable: leave it uncached and retry next load
        if found is api.MISSING:
            # GolfCore really has no such course, so remember that and stop asking.
            record = {"courseName": name, "name": name, "city": None,
                      "lat": None, "lng": None}
        else:
            record = {"courseName": name, "name": found["name"], "city": found["city"],
                      "lat": found["lat"], "lng": found["lng"]}
        known[key] = record
        added.append(record)
        return record

    @app.get("/")
    def index():
        with file_lock:
            posts = load_records("tee-times.json")
            interests = load_records("interests.json")
            cached = load_records("courses.json")
        states = {post["postId"]: post_state(post["postId"], interests) for post in posts}
        # call the APIs outside the lock so a slow API cannot block another request.
        known = {row["courseName"].casefold(): row for row in cached}
        added = []
        courses, weather = {}, {}
        for post in posts:
            course = course_for(post["courseName"], known, added)
            courses[post["postId"]] = course
            # no coordinates means no forecast. The tee time still shows.
            weather[post["postId"]] = (
                lookup.rain_chance(course["lat"], course["lng"], post["date"], post["time"])
                if course and course["lat"] is not None else None
            )
        if added:
            with file_lock:
                saved = load_records("courses.json")
                seen = {row["courseName"].casefold() for row in saved}
                saved.extend(row for row in added if row["courseName"].casefold() not in seen)
                save_records("courses.json", saved)
        return render_template("index.html", posts=posts, states=states,
                               courses=courses, weather=weather)

    @app.post("/posts")
    def create_post():
        # this small manual form supplies posts until the main browse/post flow is connected.
        course = request.form.get("course", "").strip()
        date = request.form.get("date", "")
        time = request.form.get("time", "")
        if not course or len(course) > 120:
            return "Enter a course name of 1–120 characters.", 400
        try:
            tee_time = datetime.fromisoformat(f"{date}T{time}")
            if tee_time.tzinfo is not None:
                raise ValueError("Use local time")
            tee_time = tee_time.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
        except ValueError:
            return "Enter a valid date and time.", 400
        if tee_time <= datetime.now(ZoneInfo("America/Los_Angeles")):
            return "Choose a future tee time.", 400
        with file_lock:
            posts = load_records("tee-times.json")
            if any(p["courseName"].casefold() == course.casefold() and p["date"] == date and p["time"] == time for p in posts):
                return "That tee time is already posted.", 409
            posts.append({"postId": uuid4().hex, "courseName": course,
                          "studentId": session["studentId"], "date": date, "time": time})
            save_records("tee-times.json", posts)
        return redirect(url_for("index"), code=303)

    @app.post("/posts/<post_id>/interest")
    def toggle_interest(post_id):
        # the post ID comes from the URL; the student ID comes from the session.
        with file_lock:
            posts = load_records("tee-times.json")
            if not any(post.get("postId") == post_id for post in posts):
                return "This tee time was not found.", 404
            interests = load_records("interests.json")
            existing = next((row for row in interests if row.get("postId") == post_id
                             and row.get("studentId") == session["studentId"]), None)
            if existing is None:
                interests.append({"interestId": uuid4().hex, "postId": post_id,
                                  "studentId": session["studentId"]})
            else:
                interests.remove(existing)
            save_records("interests.json", interests)
        flash("Interest saved." if existing is None else "Interest removed.")
        return redirect(url_for("index"), code=303)

    @app.get("/counts")
    def counts():
        with file_lock:
            posts = load_records("tee-times.json")
            interests = load_records("interests.json")
        response = jsonify({post["postId"]: post_state(post["postId"], interests) for post in posts})
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(OSError)
    @app.errorhandler(ValueError)
    def storage_error(error):
        # preserve unreadable data and show a useful message instead of overwriting it.
        app.logger.error("Saved data could not be read or written", exc_info=error)
        return "Saved data is unavailable. Please try again after checking the data files.", 503

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5050)
