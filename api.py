"""Live course and weather lookups for GolfFinderUW.

Both functions return None instead of raising when anything goes wrong, so a
failed lookup never stops a posted tee time from appearing on the page.
"""

import os

import requests

COURSE_URL = "https://api.golfcore.org/v1/courses"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
# keep the page responsive: give up on a slow API rather than make the user wait.
TIMEOUT_SECONDS = 6
# find_course returns one of three things, so the caller can tell a real answer
# from a failure: a dict (GolfCore knows the course), MISSING (GolfCore answered
# but has no such course), or None (GolfCore could not be reached).
MISSING = object()


def find_course(name, city="Seattle"):
    """Look up one course's official name, city and coordinates in GolfCore.

    Returns a dict, MISSING if GolfCore has no such course, or None if GolfCore
    could not be reached.
    """
    params = {"q": name, "city": city, "country": "us", "limit": 1}
    # the key is optional today. GolfCore requires one from December 4, 2026.
    key = os.environ.get("GOLFCORE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    try:
        response = requests.get(COURSE_URL, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        courses = response.json().get("courses", [])
    except (requests.RequestException, ValueError):
        return None
    if not courses:
        return MISSING
    found = courses[0]
    try:
        return {
            "name": found["name"],
            "city": found.get("city") or city,
            "lat": float(found["lat"]),
            "lng": float(found["lng"]),
        }
    except (KeyError, TypeError, ValueError):
        return None


def rain_chance(lat, lng, date, time):
    """Percent chance of rain at the tee time's hour, or None if unavailable.

    Open-Meteo answers by hour, not by tee time, so a 14:30 tee time reads the
    14:00 row. The forecast only reaches about 16 days ahead; past that there is
    no matching hour and this returns None.
    """
    wanted_hour = f"{date}T{time[:2]}:00"
    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": "precipitation_probability",
        "start_date": date,
        "end_date": date,
        "timezone": "America/Los_Angeles",
    }
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        hourly = response.json()["hourly"]
        # match the tee time to its hour instead of assuming a position in the list.
        chance = hourly["precipitation_probability"][hourly["time"].index(wanted_hour)]
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return None
    return None if chance is None else int(chance)
