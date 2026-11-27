"""Keep the test suite offline.

These tests check saved data, interest counts and error handling, not the live
APIs, so the course and forecast lookups are turned off for every test. That
keeps the suite fast and keeps it passing with no network and no API quota.
"""

import os

os.environ["GOLFFINDER_OFFLINE"] = "1"
