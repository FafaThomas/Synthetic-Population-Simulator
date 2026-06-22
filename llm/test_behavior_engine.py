from datetime import date
from datetime import timedelta

from generate_archetypes import generate_archetype
from generate_persona import generate_persona
from generate_lifestyle import generate_lifestyle
from generate_behavior_profile import generate_behavior_profile
from generate_routine import generate_routine

from models import SyntheticPerson

from behavior_engine import generate_day


def build_person():

    archetype = generate_archetype()

    persona = generate_persona(
        archetype
    )

    lifestyle = generate_lifestyle(
        archetype,
        persona
    )

    behavior_profile = generate_behavior_profile(
        persona,
        lifestyle
    )

    routine = generate_routine(
        persona,
        lifestyle,
        behavior_profile
    )

    return SyntheticPerson(
        archetype=archetype,
        persona=persona,
        lifestyle=lifestyle,
        behavior_profile=behavior_profile,
        routine=routine
    )


def main():

    person = build_person()

    print()
    print("=" * 80)
    print("PERSON")
    print("=" * 80)

    print(
        person.persona.model_dump_json(
            indent=4
        )
    )

    print()

    for i in range(7):

        simulation_day = (
            date.today()
            + timedelta(days=i)
        )

        schedule = generate_day(
            person,
            simulation_day
        )

        print()
        print("=" * 80)
        print(simulation_day)
        print("=" * 80)

        print(
            schedule.model_dump_json(
                indent=4
            )
        )


if __name__ == "__main__":
    main()