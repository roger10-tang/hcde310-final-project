A user can post a tee time, express interest, remove interest, and see the saved interest count.

The local interest prototype works. It uses a browser session to identify each student and saves interestId, postId, and studentId in data/interests.json. Six automated checks passed, including reading saved interest after starting a new app instance. A browser check confirmed posting through the form, adding and removing interest, and another open page updating without a refresh. The recording or screenshots and team flow diagram still need to be added.

The main work left is connecting GolfCore and Open-Meteo to the real browse page, matching forecasts to the tee time, and showing useful messages for API failure or no results. Next, finish the date-based browse flow, course relationships, and handling past posts. Then finish the diagram and recording, test with users, and make changes from their feedback. The P3 rubric page was unavailable when checked on November 23, so this list still needs to be checked against the rubric when it opens.

One design decision is to use a browser session instead of building accounts for this version. It keeps the interest feature small while letting two different browsers have separate interests. A second click removes the existing record. The count is calculated from the records instead of saved as a separate number.

The temporary manual posting form stores courseName directly in each post so the interest feature can run before API integration. This differs from the P2 courseId relationship and needs to be reconciled when the course data is connected.

The P2 testing plan is to ask three UW student golfers to try the app at the UW Golf Club range meetup on Friday, December 4. The individual participants and arrangements still need confirmation. We should leave time to fix problems before P3.

Roger keeps his personal CC2 draft separately. The implementation is shared on the roger/hw6-interest branch. Ownership and integration details are in HANDOFF.md.
