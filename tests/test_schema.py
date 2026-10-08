import json
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA = json.loads(Path("docs/schemas/telemetry.v1.json").read_text())
validator = Draft202012Validator(SCHEMA)

GOOD = {
    "v": 1,
    "msg_id": "a3f1c9e2-5b7d-4c1a-9f20-6d2e8b1a0c44",
    "ts": "2026-10-08T08:30:00Z",
    "node": "node3",
    "moisture_pct": 41.2,
    "temp_c": 12.8,
}


def test_valid_message_passes():
    assert validator.is_valid(GOOD)


def test_missing_required_field_fails():
    bad = {k: v for k, v in GOOD.items() if k != "moisture_pct"}
    assert not validator.is_valid(bad)


def test_moisture_out_of_range_fails():
    assert not validator.is_valid({**GOOD, "moisture_pct": 140})


def test_unknown_field_fails():
    assert not validator.is_valid({**GOOD, "colour": "red"})


def test_local_time_instead_of_utc_fails():
    assert not validator.is_valid({**GOOD, "ts": "2026-10-08T10:30:00+02:00"})