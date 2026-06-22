from models import Persona
from models import Schedule


def validate_persona(persona: Persona):

    if persona.age < 13:
        raise ValueError("Invalid age")


def validate_schedule(schedule: Schedule):

    if not schedule.wake_time:
        raise ValueError("Wake time missing")

    if not schedule.sleep_time:
        raise ValueError("Sleep time missing")