# Current Git progress

Roger's interest feature is implemented and checked. The API and main-page work below is the proposed split based on P2. Won has not confirmed this split yet.

| Owner | Scope | Main code |
| --- | --- | --- |
| Roger | Interest button, add/remove interest, JSON storage, interest counts, automatic count updates | toggle_interest(), load_records(), save_records(), post_state(), counts() in app.py; static/counts.js; interest form in templates/index.html |
| Won, proposed | GolfCore and Open-Meteo, matching weather to the tee time, course information, date-based browsing, final posting form and page layout | New API code; index() and create_post() in app.py; course and weather parts of templates/index.html |
| Together | Connect the features, run the full flow, diagram, recording, progress.md and user testing | Shared integration and documentation |

app.py and templates/index.html are shared files. Please compare changes before replacing either file. The current manual posting form is a small scaffold for trying the interest feature. It is not a finished replacement for the planned posting flow.

Each interest record uses interestId, postId and studentId. studentId comes from the Flask browser session, not a user-entered name. Keep each postId stable when adding course and weather data.

The temporary post format is postId, courseName, studentId, date and time. P2 used courseId instead of courseName. When courseId is added, update the page to look up the course name and keep the existing postId for the interest links. Decide how to handle any old local posts before changing the format.

The interest form sends POST /posts/<post_id>/interest with the session's formToken as a hidden input. The route toggles that session's interest and redirects to the page. GET /counts returns an object keyed by postId. Each value has count and interested. static/counts.js reads it every two seconds. It currently returns all posts, without filtering by date.

The count is calculated from saved interest records. Keep this rule when connecting the API code. Do not save a second independent count in the post. Keep the existing formToken protection on both POST forms.

Six automated checks pass for restart persistence, separate sessions, missing files, broken JSON, bad post input and missing form tokens. Browser verification on November 24 covered posting, adding and removing interest, and another open tab updating without a reload. The two tabs shared one session; separate identities were checked with two Flask test clients.

Still to finish are live API data, forecast matching and failure messages, the date-based page, course relationships, past-post handling, the team diagram, demonstration media and user testing. The implementation is shared on the roger/hw6-interest branch. The team should check the final P3 rubric when available.

We will share changes through the team Git repository. Keep data/, .venv/ and .env local. Roger's personal CC2 draft is kept separately from the shared app work. The implementation is shared on the roger/hw6-interest branch.
