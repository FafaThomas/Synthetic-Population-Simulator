import json
import uuid
from db import get_connection

from generate_archetypes import generate_archetype
from generate_persona import generate_persona
from generate_lifestyle import generate_lifestyle
from generate_behavior_profile import generate_behavior_profile
from generate_routine import generate_routine

from models import SyntheticPerson

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

def insert_archetype(
    cur,
    archetype
):

    archetype_id = str(
        uuid.uuid4()
    )

    cur.execute(
        """
        INSERT INTO archetypes
        (
            id,
            name,
            description,
            age_min,
            age_max,
            common_occupations,
            lifestyle_summary
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            archetype_id,
            archetype.name,
            archetype.description,
            archetype.age_range[0],
            archetype.age_range[1],
            json.dumps(
                archetype.common_occupations
            ),
            archetype.lifestyle_summary
        )
    )

    return archetype_id


def insert_persona(
    cur,
    archetype_id,
    persona
):

    persona_id = str(
        uuid.uuid4()
    )

    cur.execute(
        """
        INSERT INTO personas
        (
            id,
            archetype_id,
            first_name,
            last_name,
            age,
            occupation,
            city,
            country
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            persona_id,
            archetype_id,
            persona.first_name,
            persona.last_name,
            persona.age,
            persona.occupation,
            persona.city,
            persona.country
        )
    )

    return persona_id

def insert_lifestyle(
    cur,
    persona_id,
    lifestyle
):

    cur.execute(
        """
        INSERT INTO lifestyles
        (
            persona_id,
            relationship_status,
            hobbies,
            social_activity_level,
            fitness_level,
            chronotype,
            work_style,
            travel_frequency,
            exercise_probability
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            persona_id,
            lifestyle.relationship_status,
            json.dumps(
                lifestyle.hobbies
            ),
            lifestyle.social_activity_level,
            lifestyle.fitness_level,
            lifestyle.chronotype,
            lifestyle.work_style,
            lifestyle.travel_frequency,
            lifestyle.exercise_probability
        )
    )

def insert_behavior_profile(
    cur,
    persona_id,
    behavior
):

    cur.execute(
        """
        INSERT INTO behavior_profiles
        (
            persona_id,
            weekday_work_probability,
            weekend_work_probability,
            exercise_probability,
            social_probability,
            travel_probability
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s
        )
        """,
        (
            persona_id,
            behavior.weekday_work_probability,
            behavior.weekend_work_probability,
            behavior.exercise_probability,
            behavior.social_probability,
            behavior.travel_probability
        )
    ) 


def insert_routine(
    cur,
    persona_id,
    routine
):

    cur.execute(
        """
        INSERT INTO routines
        (
            persona_id,
            weekday_wake_time,
            weekday_sleep_time,
            weekend_wake_time,
            weekend_sleep_time,
            activities
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s
        )
        """,
        (
            persona_id,
            routine.weekday_wake_time,
            routine.weekday_sleep_time,
            routine.weekend_wake_time,
            routine.weekend_sleep_time,
            json.dumps(
                routine.activities.model_dump()
            )
        )
    )

def save_person(
    conn,
    person
):

    with conn.cursor() as cur:

        archetype_id = insert_archetype(
            cur,
            person.archetype
        )

        persona_id = insert_persona(
            cur,
            archetype_id,
            person.persona
        )

        insert_lifestyle(
            cur,
            persona_id,
            person.lifestyle
        )

        insert_behavior_profile(
            cur,
            persona_id,
            person.behavior_profile
        )

        insert_routine(
            cur,
            persona_id,
            person.routine
        )

    conn.commit()


TARGET_USERS = 1000

def main():

    for i in range(TARGET_USERS):

        try:

            person = build_person()

            with get_connection() as conn:

                save_person(
                    conn,
                    person
                )

            print(
                f"[SUCCESS {i+1}/{TARGET_USERS}] "
                f"{person.persona.first_name} "
                f"{person.persona.last_name}"
            )

        except Exception as ex:

            print(
                f"[SKIPPED USER {i+1}/{TARGET_USERS}] "
                f"{type(ex).__name__}: {ex}"
            )

if __name__ == "__main__":
    main()

