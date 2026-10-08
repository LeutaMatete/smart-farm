import re
from datetime import datetime

from simulator.clock import STEPS_PER_DAY, Clock

TS_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"


def test_steps_per_day():
    assert STEPS_PER_DAY == 144


def test_utc_conversion_subtracts_two_hours():
    clock = Clock(datetime(2026, 1, 1, 0, 0))
    assert clock.utc_iso() == "2025-12-31T22:00:00Z"


def test_tick_advances_ten_minutes():
    clock = Clock(datetime(2026, 1, 1, 12, 0))
    clock.tick()
    assert clock.hour == 12 + 10 / 60


def test_dt_days_is_one_144th_of_a_day():
    assert abs(Clock(datetime(2026, 1, 1)).dt_days - 1 / 144) < 1e-12


def test_timestamp_matches_data_contract_pattern():
    assert re.match(TS_PATTERN, Clock(datetime(2026, 6, 15, 8, 30)).utc_iso())