"""Run a bare field (no irrigation) through one real year of Qacha's Nek weather.

Usage, from the repo root:  python -m simulator.demo_field [sand|loam|clay]
"""
import sys
from datetime import datetime

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from simulator.clock import STEPS_PER_DAY, Clock
from simulator.field import Field
from simulator.weather import WeatherModel

texture = sys.argv[1] if len(sys.argv) > 1 else "loam"
weather = WeatherModel("simulator/climates/qachas_nek_daily.csv", seed=42)
clock = Clock(datetime(2024, 1, 1))
field = Field(texture)

rows = []
for _ in range(366):  # 2024 is a leap year
    day = clock.local.date()
    for _ in range(STEPS_PER_DAY):
        field.step(
            weather.temperature(clock.local),
            clock.hour,
            weather.rain_mm(clock.local),
            0.0,
            clock.dt_days,
        )
        clock.tick()
    rows.append((day, field.theta))

df = pd.DataFrame(rows, columns=["date", "theta"])
df["month"] = pd.to_datetime(df["date"]).dt.month
wp, fc = field.soil["wilting_pt"], field.soil["field_cap"]
half = wp + 0.5 * (fc - wp)  # 50% of plant-available water used up

print(f"Soil: {texture}  (wilting {wp}, field capacity {fc}, half-available {half})")
print(df.groupby("month")["theta"].agg(["min", "mean", "max"]).round(1))
print(f"\nDays below half of available water: {(df['theta'] < half).sum()} of {len(df)}")
print(f"Lowest moisture of the year: {df['theta'].min():.1f}%")

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(pd.to_datetime(df["date"]), df["theta"], label="soil moisture")
ax.axhline(fc, color="green", ls="--", label="field capacity")
ax.axhline(half, color="orange", ls="--", label="half of available water")
ax.axhline(wp, color="red", ls="--", label="wilting point")
ax.set_ylabel("Soil moisture (%)")
ax.set_title(f"{texture} soil, no irrigation, Qacha's Nek weather 2024")
ax.legend(loc="lower right")
fig.tight_layout()
out = f"docs/field_demo_{texture}.png"
fig.savefig(out, dpi=120)
print("Saved", out)