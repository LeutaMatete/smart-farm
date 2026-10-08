"""Turns daily weather (from Open-Meteo) into 10-minute weather for the simulator.

Simplifications in v0.1:
- Temperature follows a cosine between the day's min and max, peaking at 15:00.
  There can be a small jump at midnight between one day and the next.
- A day's rain falls in ONE random window; heavier days rain for longer.
- rain_mm() is the rain in the 10-minute step starting at the given time.
"""
import csv
import math
import random
from datetime import date

from simulator.clock import STEP_MINUTES, STEPS_PER_DAY

TMAX_HOUR = 15


class WeatherModel:
    def __init__(self, csv_path, seed=0):
        self.seed = seed
        self.days = {}
        self._plans = {}
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                d = date.fromisoformat(row["date"])
                try:
                    self.days[d] = {
                        "tmax": float(row["tmax_c"]),
                        "tmin": float(row["tmin_c"]),
                        "precip": float(row["precip_mm"]),
                        "et0": float(row["et0_mm"]),
                    }
                except ValueError:
                    raise ValueError(f"Missing or invalid weather values on {d}")
        if not self.days:
            raise ValueError(f"No weather rows found in {csv_path}")

    def _day(self, local_dt):
        d = local_dt.date()
        if d not in self.days:
            raise KeyError(f"No weather data for {d}")
        return d, self.days[d]

    def temperature(self, local_dt):
        _, w = self._day(local_dt)
        hour = local_dt.hour + local_dt.minute / 60
        mean = (w["tmax"] + w["tmin"]) / 2
        amp = (w["tmax"] - w["tmin"]) / 2
        return mean + amp * math.cos(2 * math.pi * (hour - TMAX_HOUR) / 24)

    def _rain_plan(self, d, mm):
        if d not in self._plans:
            if mm < 0.1:
                self._plans[d] = None
            else:
                rng = random.Random(f"{self.seed}-{d.isoformat()}")
                hours = min(12, max(1, round(mm / 2)))
                n_steps = hours * 60 // STEP_MINUTES
                start = rng.randrange(0, STEPS_PER_DAY - n_steps + 1)
                self._plans[d] = (start, n_steps)
        return self._plans[d]

    def rain_mm(self, local_dt):
        d, w = self._day(local_dt)
        plan = self._rain_plan(d, w["precip"])
        if plan is None:
            return 0.0
        start, n_steps = plan
        idx = (local_dt.hour * 60 + local_dt.minute) // STEP_MINUTES
        return w["precip"] / n_steps if start <= idx < start + n_steps else 0.0

    def et0_mm_day(self, local_dt):
        """Reference evapotranspiration for the day. Not used by the v0.1 drying model."""
        return self._day(local_dt)[1]["et0"]