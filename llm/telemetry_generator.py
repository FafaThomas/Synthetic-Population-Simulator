from dataclasses import dataclass
from datetime import timedelta,datetime
import random


@dataclass
class TelemetryEvent:
    persona_id: str
    device_id: str
    timestamp: datetime
    source: str
    category: str
    metric_group: str
    metric: str
    value: str

def create_event(
    persona_id,
    device_id,
    timestamp,
    source,
    category,
    metric_group,
    metric,
    value
):

    return TelemetryEvent(
        persona_id=persona_id,
        device_id=device_id,
        timestamp=timestamp,
        source=source,
        category=category,
        metric_group=metric_group,
        metric=metric,
        value=str(value)
    )

def get_device(
    devices,
    device_type
):

    for device in devices:

        if device["device_type"] == device_type:

            return device

    return None


def random_timestamp_between(
    start_dt,
    end_dt
):

    seconds = int(
        (end_dt - start_dt).total_seconds()
    )

    return start_dt + timedelta(
        seconds=random.randint(
            0,
            seconds
        )
    )



def generate_sleep(
    person,
    desktop,
    watch,
    start_dt,
    end_dt
):

    events = []

    sleep_stages = [

        ("Light", 0.0),

        ("Deep", 0.2),

        ("REM", 0.6),

        ("Light", 0.8)
    ]

    for stage, progress in sleep_stages:

        timestamp = start_dt + (
            end_dt - start_dt
        ) * progress

        events.append(

            create_event(
                person.persona.id,
                watch["id"],
                timestamp,
                watch["device_name"],
                "Biometrics",
                "Sleep",
                "State",
                stage
            )
        )

    current = start_dt

    while current <= end_dt:

        hr = random.randint(
            48,
            65
        )

        events.append(

            create_event(
                person.persona.id,
                watch["id"],
                current,
                watch["device_name"],
                "Biometrics",
                "HeartRate",
                "Reading",
                hr
            )
        )

        current += timedelta(
            minutes=30
        )

    return events

    
def generate_gaming(
    person,
    desktop,
    watch,
    start_dt,
    end_dt
):

    events = []

    events.append(

        create_event(
            person.persona.id,
            desktop["id"],
            start_dt,
            desktop["device_name"],
            "Activity",
            "Valorant",
            "Event",
            "Launching"
        )
    )

    events.append(

        create_event(
            person.persona.id,
            desktop["id"],
            start_dt + timedelta(
                minutes=5
            ),
            desktop["device_name"],
            "Activity",
            "Valorant",
            "Event",
            "Match Found"
        )
    )

    current = start_dt + timedelta(
        minutes=10
    )

    while current < end_dt:

        if random.random() < 0.5:

            event_type = random.choice(
                [
                    "Kill_Event",
                    "Death_Event"
                ]
            )

            result = random.choice(
                [
                    "Headshot",
                    "Non-Headshot"
                ]
            )

            events.append(

                create_event(
                    person.persona.id,
                    desktop["id"],
                    current,
                    desktop["device_name"],
                    "Activity",
                    "Valorant",
                    event_type,
                    result
                )
            )

            hr = random.randint(
                85,
                115
            )

            events.append(

                create_event(
                    person.persona.id,
                    watch["id"],
                    current,
                    watch["device_name"],
                    "Biometrics",
                    "HeartRate",
                    "Reading",
                    hr
                )
            )

        current += timedelta(
            minutes=random.randint(
                2,
                5
            )
        )

    events.append(

        create_event(
            person.persona.id,
            desktop["id"],
            end_dt,
            desktop["device_name"],
            "Activity",
            "Valorant",
            "Event",
            "Exit"
        )
    )

    return events

def generate_coding(
    person,
    desktop,
    watch,
    start_dt,
    end_dt
):

    events = []

    events.append(

        create_event(
            person.persona.id,
            desktop["id"],
            start_dt,
            desktop["device_name"],
            "Activity",
            "IDE",
            "Event",
            "Launch"
        )
    )

    events.append(

        create_event(
            person.persona.id,
            desktop["id"],
            start_dt + timedelta(
                minutes=5
            ),
            desktop["device_name"],
            "Activity",
            "IDE",
            "Active_Project",
            "alisa-v2-backend"
        )
    )

    midpoint = start_dt + (
        end_dt - start_dt
    ) / 2

    events.append(

        create_event(
            person.persona.id,
            desktop["id"],
            midpoint,
            desktop["device_name"],
            "Activity",
            "Chrome",
            "URL",
            "github.com"
        )
    )

    events.append(

        create_event(
            person.persona.id,
            desktop["id"],
            end_dt,
            desktop["device_name"],
            "Activity",
            "IDE",
            "Event",
            "Exit"
        )
    )

    return events

ACTIVITY_ALIAS = {

    "Work": "Coding",

    "Learning languages": "Coding",

    "Online courses or webinars related to content creation and digital marketing":
        "Coding",

    "Photography": "Walking",

    "Exploring local cuisine": "Walking",

    "Walking in local parks": "Walking",

    "Gaming": "Gaming",

    "Sleep": "Sleep"
}

ACTIVITY_GENERATORS = {

    "Sleep":
        generate_sleep,

    "Gaming":
        generate_gaming,

    "Coding":
        generate_coding
}

def generate_telemetry(
    person,
    devices,
    activities,
    activity_date
):

    events = []

    desktop = get_device(
        devices,
        "desktop"
    )

    watch = get_device(
        devices,
        "smart_watch"
    )

    phone = get_device(
        devices,
        "phone"
    )

    

    for activity in activities:

        start_time = datetime.strptime(
            activity.start_time,
            "%H:%M"
        ).time()

        start_dt = datetime.combine(
            activity_date,
            start_time
        )

        end_time = datetime.strptime(
            activity.end_time,
            "%H:%M"
        ).time()

        end_dt = datetime.combine(
            activity_date,
            end_time
        )

        activity_name = ACTIVITY_ALIAS.get(
            activity.activity_name,
            activity.activity_name
        )

        generator = ACTIVITY_GENERATORS.get(
            activity_name
        )

        if generator is None:
            continue

        activity_events = generator(
            person,
            desktop,
            watch,
            start_dt,
            end_dt
        )

        events.extend(
            activity_events
        )

    events.sort(
        key=lambda e: e.timestamp
    )

    return events
    


