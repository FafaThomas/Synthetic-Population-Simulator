from datetime import timedelta

from person_loader import load_person
from device_loader import load_devices

from behavior_engine import generate_day
from telemetry_generator import generate_telemetry

from clickhouse_writer import insert_events


def generate_history(
    persona_id,
    start_date,
    end_date
):

    person = load_person(
        persona_id
    )

    devices = load_devices(
        persona_id
    )

    current_date = start_date

    total_events = 0

    while current_date <= end_date:

        print(
            f"Generating {current_date}"
        )

        day = generate_day(
            person,
            current_date
        )

        events = generate_telemetry(
            person,
            devices,
            day.activities,
            current_date
        )

        insert_events(
            events
        )

        total_events += len(events)

        current_date += timedelta(days=1)

    print(
        f"Generated {total_events} events"
    )

