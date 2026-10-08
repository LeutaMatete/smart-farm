"""Simulated time.

The simulation runs in LOCAL time (Africa/Maseru: UTC+2, no daylight saving)
because the weather data and the daylight cycle are local. Messages leave the
simulator in UTC, as the data contract requires.
"""
from datetime import timedelta

STEP_MINUTES = 10
STEPS_PER_DAY = 24 * 60 // STEP_MINUTES  # 144


class Clock:
    def __init__(self, start_local, utc_offset_hours=2, step_minutes=STEP_MINUTES):
        self.local = start_local  # a naive datetime holding local time
        self.utc_offset = timedelta(hours=utc_offset_hours)
        self.step = timedelta(minutes=step_minutes)

    def tick(self):
        self.local += self.step

    @property
    def dt_days(self):
        """Length of one step as a fraction of a day (what the physics needs)."""
        return self.step / timedelta(days=1)

    @property
    def hour(self):
        """Local hour of day as a decimal, for example 14.5 for 14:30."""
        return self.local.hour + self.local.minute / 60

    def utc_iso(self):
        """Current time as UTC ISO 8601 ending in Z, as the data contract requires."""
        return (self.local - self.utc_offset).strftime("%Y-%m-%dT%H:%M:%SZ")