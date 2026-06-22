from datetime import datetime

from person_loader import load_person
from device_loader import load_devices

from telemetry_generator import (
    generate_gaming,
    get_device
)

PERSONA_ID = "dc5aa98d-bc0e-4aca-8604-a8726ae47e22"

person = load_person(
    PERSONA_ID
)

devices = load_devices(
    PERSONA_ID
)

desktop = get_device(
    devices,
    "desktop"
)

watch = get_device(
    devices,
    "smart_watch"
)

events = generate_gaming(
    person,
    desktop,
    watch,
    datetime(
        2026,
        6,
        23,
        10,
        0
    ),
    datetime(
        2026,
        6,
        23,
        10,
        34
    )
)

for event in events:

    print(event)