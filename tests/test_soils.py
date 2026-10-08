import json
from pathlib import Path

SOILS = json.loads(Path("simulator/config/soils.json").read_text())


def test_three_textures_present():
    assert set(SOILS) == {"sand", "loam", "clay"}


def test_water_levels_are_ordered():
    for name, s in SOILS.items():
        assert 0 < s["wilting_pt"] < s["field_cap"] < s["saturation"] <= 100, name


def test_clay_holds_more_water_than_sand_at_field_capacity():
    assert SOILS["clay"]["field_cap"] > SOILS["sand"]["field_cap"]


def test_loam_has_the_most_plant_available_water():
    awc = {n: s["field_cap"] - s["wilting_pt"] for n, s in SOILS.items()}
    assert max(awc, key=awc.get) == "loam"