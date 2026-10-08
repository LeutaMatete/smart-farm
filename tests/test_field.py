import pytest

from simulator.field import K_PEAK, Field, daylight_factor

DT = 1 / 144


def run(field, days, temp_c, rain_mm=0.0, dt=DT):
    steps = round(days / dt)
    steps_per_day = round(1 / dt)
    for i in range(steps):
        hour = (i % steps_per_day) * dt * 24
        field.step(temp_c, hour, rain_mm, 0.0, dt)
    return field.theta


def test_k_peak_matches_exercise_2():
    assert abs(K_PEAK - 0.4355) < 0.001


def test_daylight_factor_shape():
    assert daylight_factor(3) == 0 and daylight_factor(22) == 0
    assert abs(daylight_factor(12) - 1.0) < 1e-12


def test_half_life_is_five_days_at_20c():
    f = Field("loam")  # starts at field capacity: 28, so available water = 16
    run(f, 5, 20.0)
    assert abs((f.theta - 12) - 8.0) < 0.05


def test_no_drying_when_freezing():
    f = Field("loam", theta=20.0)
    run(f, 3, -2.0)
    assert f.theta == 20.0


def test_never_dries_below_wilting_point():
    f = Field("loam")
    run(f, 60, 35.0)
    assert f.theta >= 12


def test_exercise_3_six_mm_raises_loam_by_two_points():
    f = Field("loam", theta=20.0)
    f.step(20.0, 0.0, 0.0, 6.0, DT)  # hour 0: no daylight, so no drying
    assert abs(f.theta - 22.0) < 1e-9


def test_runoff_cap_and_drainage_back_to_field_capacity():
    f = Field("loam", theta=20.0)
    f.step(20.0, 0.0, 500.0, 0.0, DT)
    assert f.theta <= 47  # saturation
    run(f, 5, 20.0)
    assert f.theta < 28.1  # back near field capacity (28)


def test_sand_drains_faster_than_clay():
    sand, clay = Field("sand", theta=43.0), Field("clay", theta=47.0)
    run(sand, 1, 0.0)
    run(clay, 1, 0.0)
    assert (sand.theta - 17) < (clay.theta - 32)


def test_exercise_4_exact_step_stays_valid_with_a_huge_time_step():
    f = Field("loam", theta=28.0)
    f.step(40.0, 12.0, 0.0, 0.0, 1.0)  # k*dt is about 1.7: simple Euler would go negative
    assert f.theta >= 12


def test_step_size_barely_matters():
    fine, coarse = Field("loam"), Field("loam")
    run(fine, 2, 20.0, dt=1 / 144)
    run(coarse, 2, 20.0, dt=1 / 24)
    assert abs(fine.theta - coarse.theta) < 0.05


def test_unknown_texture_rejected():
    with pytest.raises(ValueError):
        Field("gravel")


def test_start_below_wilting_point_rejected():
    with pytest.raises(ValueError):
        Field("loam", theta=5.0)