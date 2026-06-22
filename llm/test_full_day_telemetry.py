from datetime import date

from person_loader import load_person
from device_loader import load_devices

from behavior_engine import generate_day

from telemetry_generator import (
    generate_telemetry
)

PERSONA_ID = (
    "dc5aa98d-bc0e-4aca-8604-a8726ae47e22"
)

person = load_person(
    PERSONA_ID
)

devices = load_devices(
    PERSONA_ID
)

day = generate_day(
    person,
    date(2026, 6, 23)
)

print("\n=== GENERATED SCHEDULE ===\n")

for activity in day.activities:

    print(
        f"{activity.start_time}"
        f" -> "
        f"{activity.end_time}"
        f" | "
        f"{activity.activity_name}"
    )

events = generate_telemetry(
    person,
    devices,
    day.activities
)

print("\n=== GENERATED TELEMETRY ===\n")

for event in events:

    print(event)

print(
    f"\nTotal Events: "
    f"{len(events)}"
)