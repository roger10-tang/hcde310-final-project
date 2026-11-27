9: cc2 prep
On the team diagram it is step 3, next to the GolfCore box. It passes the course's lat and lng on to step 4. 
lines 84–106 of app.py

What it does
course_for() finds a golf course's location. It looks in courses.json first. If the course isn't there, it asks GolfCore and saves the answer so it doesn't have to ask again. 

Edge cases

Empty input: create_post() doesn't allow an empty course name, so this shouldn't happen. If an empty name did get in, say from editing tee-times.json by hand, it would go straight to GolfCore, and the result would depend on api.find_course.
API fails: find_course gives back None, so nothing is saved and the app tries again next time. The tee time still shows, just without a forecast. I'd check that index.html doesn't break when the course is None.
JSON file doesn't exist yet: the app treats a missing courses.json as an empty list. It looks up every course, then creates the file when it saves. If the file exists but is broken, the page shows the "Saved data is unavailable" error.

Change one line of text: line 58
raise ValueError("Expected a list of records")
to:
raise ValueError("This JSON file should be a list of records")

rewording the message so it says what's wrong in plainer language.


10: Look back at your HW5.
The problem: My app caught every error at once and printed the real error text on the page, so when the API said 403 the page showed my API address — and any coding mistake of mine would be hidden the same way. Next time I'd catch it by breaking the API on purpose (wrong key or wrong URL) and seeing if the page shows the error text instead of a friendly message.

My project: No. In api.py:35 and api.py:73 I only catch the few errors I expect and return nothing instead of showing the error, so the user sees my own message and real bugs still show up in the log.