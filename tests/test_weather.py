from datetime import datetime, timedelta

import pytest

from simulator.weather import WeatherModel

CSV = """date,tmax_c,tmin_c,tmean_c,precip_mm,et0_mm
2025-01-01,24.0,10.0,17.0,12.0,4.5
2025-01-02,20.0,8.0,14.0,0.0,3.9
2025-01-03,18.0,6.0,12.0,0.05,3.5
"""


@pytest.fixture
def csv_path(tmp_path):
    p = tmp_path / "weather.csv"
    p.write_text(CSV)
    return p


def day_steps(day):
    return [datetime(2025, 1, day) + timedelta(minutes=10 * i) for i in range(144)]


def test_temperature_peaks_at_tmax_and_bottoms_at_tmin(csv_path):
    w = WeatherModel(csv_path)
    assert abs(w.temperature(datetime(2025, 1, 1, 15, 0)) - 24.0) < 1e-9
    assert abs(w.temperature(datetime(2025, 1, 1, 3, 0)) - 10.0) < 1e-9


def test_rain_over_a_day_adds_up_to_the_daily_total(csv_path):
    w = WeatherModel(csv_path, seed=1)
    assert abs(sum(w.rain_mm(t) for t in day_steps(1)) - 12.0) < 1e-9


def test_dry_and_drizzle_days_have_no_rain(csv_path):
    w = WeatherModel(csv_path)
    assert sum(w.rain_mm(t) for t in day_steps(2)) == 0
    assert sum(w.rain_mm(t) for t in day_steps(3)) == 0


def test_same_seed_gives_same_rain_timing(csv_path):
    a = [WeatherModel(csv_path, seed=7).rain_mm(t) for t in day_steps(1)]
    b = [WeatherModel(csv_path, seed=7).rain_mm(t) for t in day_steps(1)]
    assert a == b


def test_rain_falls_in_one_continuous_window(csv_path):
    w = WeatherModel(csv_path, seed=3)
    wet = [i for i, t in enumerate(day_steps(1)) if w.rain_mm(t) > 0]
    assert wet == list(range(wet[0], wet[-1] + 1))


def test_missing_day_raises_clear_error(csv_path):
    with pytest.raises(KeyError):
        WeatherModel(csv_path).temperature(datetime(2030, 1, 1))


def test_bad_row_raises_clear_error(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("date,tmax_c,tmin_c,tmean_c,precip_mm,et0_mm\n2025-01-01,,10,15,0,3\n")
    with pytest.raises(ValueError):
        WeatherModel(p)