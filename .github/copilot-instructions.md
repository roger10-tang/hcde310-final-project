
# Context for Copilot

## Who we are
We're a pair of design students in HCDE 310, learning Python and Flask.

## How we work with AI (Stage 4: spec first)
- Don't write specs or checks for us. Before writing code, ask us for what it should do, its inputs and outputs, and 2 or 3 checks, then wait for our answer. After we write them, you may point out what's missing.
- Build in small pieces. Before you change files, tell us which ones. Don't commit.

## How we like to work
- Explain code in beginner-friendly language.
- Work on one small feature at a time.
- Explain what each file and function does.
- Don't change multiple files without telling us first.

## Our project
We're building GolfFinderUW, a web app for UW students who want to find other students to play golf with near Seattle.

Students can:
- Browse golf courses and student-posted tee times.
- Post a tee time they found on a golf course booking website.
- Tap "I'm interested" to show interest in joining a round.
- See updated interest counts from other students.
- Choose a date on the browse page, starting with today's date.
- Choose a course from GolfCore or enter a course name and location manually.
- Include an optional booking link in a tee-time post.
- Post only a future date and time.
- Express or remove interest once through a browser session.

We use:
- GolfCore Course Data API for golf course names and locations.
- Open-Meteo Forecast API for hourly precipitation probability.
- Flask and JSON files to manage student-posted tee times and interests.

GolfCore provides course information, not live tee time availability. Open-Meteo provides weather forecasts, not tee time information.

The final interface does not need a course filter or rain-chance sorting.

Interest and duplicate-interested-state are identified by browser session ID. Tapping "I'm interested" again removes that student's interest. The same browser session ID also represents the poster. Duplicate tee-time posts for the same course, date, and time are not allowed.

Past tee-time posts are deleted automatically. GolfCore failures should not prevent manually posted tee times from appearing when their course name and location are stored. If a manual course cannot provide GolfCore coordinates, show "Weather unavailable."

## Not decided yet
- Whether students will have accounts or use display names.
- Whether posted tee times should show the student's display name or remain unattributed.
- Final details of the interface and additional features.

## Wrap up
When we say "wrap up": add an entry to ai_use.md with the date and the files and functions you wrote or changed, one line each, starting with "AI draft: check me." Leave "Reflection:" blank. Suggest a commit message. Don't commit until we say yes.
