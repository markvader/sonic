# SONIC 0.2.4 — test build

- Removed legacy timezone dependency from telemetry timestamp handling.
- Uses module-level ZoneInfo for the Sonic API timestamp.
- Handles a missing telemetry timestamp safely.
- Uses a timezone-aware datetime.
- Uses Home Assistant's standard L/min flow-rate unit.
- Replaced async_timeout with asyncio.timeout.
- Removed redundant one-task asyncio.gather calls.
- Runs Sonic details and telemetry API requests concurrently.
- Fixed PropertyEntity.async_update reference.
- Uses coordinator update success for property availability.
- Version 0.2.4.
