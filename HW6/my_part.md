My part handles the interest button and saves interests in JSON. Each browser session can add or remove one interest for a tee time. The page shows the current count and checks for updates every two seconds.

The input is the post ID and browser session ID. Each saved interest has an interestId, postId, and studentId. The count is calculated from the saved records.

Six automated checks passed. They cover saving and reading after a new app starts, separate browser sessions, missing files, broken JSON, invalid posts, and missing form tokens. A browser check also confirmed adding interest, removing it, and updating another open page.

This is the interest part of the app. GolfCore and Open-Meteo are not connected yet. The small manual posting form is there so the interest button has a real post to work with.
