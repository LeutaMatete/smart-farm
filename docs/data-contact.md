# Data Contract v1

Every component (simulator, gateway, ingestion, API) must follow this document.
Changing a field name, type or meaning means bumping the version number.

## Rules
- Timestamps are ISO 8601 in UTC, ending in Z.
- Units are metric and appear in the field name (moisture_pct, temp_c).
- Every message has a version `v` and a unique `msg_id` (lowercase UUID).
- IDs (field, node) use only lowercase letters, digits, hyphen and underscore.
- Invalid messages go to a dead-letter table, never silently dropped.

## Topics
    farm/<field_id>/<node_id>/soil      telemetry from a node
    farm/<field_id>/<node_id>/status    online/offline (retained, Last Will)
    farm/<field_id>/<node_id>/cmd       command to the pump
    farm/<field_id>/<node_id>/ack       pump confirmation

Example: farm/qn-field1/node3/soil

## Telemetry (soil topic)
Required: v, msg_id, ts, node, moisture_pct (0-100), temp_c (-30 to 60)
Optional: humidity_pct (0-100), battery_v (0-5), soil_ph (0-14), ec_ds_m (0-20)

    {
      "v": 1,
      "msg_id": "a3f1c9e2-5b7d-4c1a-9f20-6d2e8b1a0c44",
      "ts": "2026-10-08T08:30:00Z",
      "node": "node3",
      "moisture_pct": 41.2,
      "temp_c": 12.8,
      "humidity_pct": 63.0,
      "battery_v": 3.92
    }

Formal schema: docs/schemas/telemetry.v1.json

## Status (status topic)
    {"v": 1, "ts": "2026-10-08T08:30:00Z", "state": "online"}
state is "online" or "offline". Published retained; "offline" is set
automatically by the MQTT Last Will when a node dies.

## Command (cmd topic)
    {"v": 1, "cmd_id": "<uuid>", "ts": "...", "action": "pump_on", "duration_s": 600}
action is "pump_on" or "pump_off". duration_s is required for pump_on.

## Acknowledgement (ack topic)
    {"v": 1, "cmd_id": "<uuid>", "ts": "...", "pump_state": "WATERING", "result": "ok"}
pump_state is IDLE, WATERING, COOLDOWN or FAULT (the pump state machine).
result is "ok", "rejected" or "fault".

## Field profile (not sent as telemetry)
Static facts about a field (soil texture, pH, location, slope) are stored in
the database and entered by the farmer, not sent by sensors.