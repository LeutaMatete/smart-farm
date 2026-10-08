"""The soil 'bucket' model. See docs/soil-model.md for the equations."""
import json
import math
from pathlib import Path

SOILS = json.loads((Path(__file__).parent / "config" / "soils.json").read_text())

# Exercise 2 in docs/soil-model.md: the daily average of the daylight factor is
# 1/pi, and we want a half-life of 5 days at 20 C, so k_peak / pi = ln(2) / 5.
K_PEAK = math.pi * math.log(2) / 5  # about 0.4355 per day
T_REF = 20.0
ROOT_DEPTH_MM = 300.0


def daylight_factor(hour):
    """s(h): zero at night, peaks at noon, zero again at 18:00."""
    return max(0.0, math.sin(math.pi * (hour - 6) / 12))


def drying_rate(temp_c, hour, k_peak=K_PEAK):
    """k in equation (2), in units of 1/day."""
    if temp_c <= 0:
        return 0.0
    return k_peak * 2 ** ((temp_c - T_REF) / 10) * daylight_factor(hour)


class Field:
    def __init__(self, texture="loam", theta=None, root_depth_mm=ROOT_DEPTH_MM, k_peak=K_PEAK):
        if texture not in SOILS:
            raise ValueError(f"Unknown soil texture: {texture}")
        self.texture = texture
        self.soil = SOILS[texture]
        self.root_depth_mm = root_depth_mm
        self.k_peak = k_peak
        self.theta = self.soil["field_cap"] if theta is None else theta
        if not self.soil["wilting_pt"] <= self.theta <= self.soil["saturation"]:
            raise ValueError("theta must be between wilting point and saturation")

    def step(self, temp_c, hour, rain_mm, irrigation_mm, dt_days):
        """Advance the soil by one time step and return the new moisture (%)."""
        s = self.soil
        # Equations (2) and (3): drying, solved exactly over the step
        k = drying_rate(temp_c, hour, self.k_peak)
        available = (self.theta - s["wilting_pt"]) * math.exp(-k * dt_days)
        theta = s["wilting_pt"] + available
        # Equation (4): water in
        theta += (rain_mm + irrigation_mm) / self.root_depth_mm * 100
        # Equation (5): runoff above saturation
        theta = min(theta, s["saturation"])
        # Equation (6): drainage back towards field capacity
        if theta > s["field_cap"]:
            excess = theta - s["field_cap"]
            theta = s["field_cap"] + excess * math.exp(-s["drainage_per_day"] * dt_days)
        self.theta = theta
        return theta