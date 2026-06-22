import json

from db import get_connection

from models import (
    Archetype,
    Persona,
    LifestyleProfile,
    BehaviorProfile,
    Routine,
    RoutineActivities,
    RoutineActivity,
    SyntheticPerson
)

def build_activity_list(
    activities: list
) -> list[RoutineActivity]:

    return [
        RoutineActivity(**activity)
        for activity in activities
    ]

def get_all_persona_ids():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT id
        FROM personas
        ORDER BY id
        """
    )

    persona_ids = [
        str(row[0])
        for row in cur.fetchall()
    ]

    cur.close()
    conn.close()

    return persona_ids

def load_person(
    persona_id: str
) -> SyntheticPerson:

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            #
            # Persona
            #

            cur.execute(
                """
                SELECT *
                FROM personas
                WHERE id = %s
                """,
                (persona_id,)
            )

            persona_row = cur.fetchone()

            if not persona_row:
                raise ValueError(
                    f"Persona {persona_id} not found"
                )

            archetype_id = persona_row[1]

            #
            # Archetype
            #

            cur.execute(
                """
                SELECT *
                FROM archetypes
                WHERE id = %s
                """,
                (archetype_id,)
            )

            archetype_row = cur.fetchone()

            #
            # Lifestyle
            #

            cur.execute(
                """
                SELECT *
                FROM lifestyles
                WHERE persona_id = %s
                """,
                (persona_id,)
            )

            lifestyle_row = cur.fetchone()

            #
            # Behavior Profile
            #

            cur.execute(
                """
                SELECT *
                FROM behavior_profiles
                WHERE persona_id = %s
                """,
                (persona_id,)
            )

            behavior_row = cur.fetchone()

            #
            # Routine
            #

            cur.execute(
                """
                SELECT *
                FROM routines
                WHERE persona_id = %s
                """,
                (persona_id,)
            )

            routine_row = cur.fetchone()

    finally:

        conn.close()

    archetype = Archetype(
        name=archetype_row[1],
        description=archetype_row[2],
        age_range=[
            archetype_row[3],
            archetype_row[4]
        ],
        common_occupations=archetype_row[5],
        lifestyle_summary=archetype_row[6]
    )

    persona = Persona(
        id=str(persona_row[0]),

        first_name=persona_row[2],
        last_name=persona_row[3],

        age=persona_row[4],
        occupation=persona_row[5],

        city=persona_row[6],
        country=persona_row[7]
    )

    lifestyle = LifestyleProfile(
        relationship_status=lifestyle_row[1],
        hobbies=lifestyle_row[2],
        social_activity_level=lifestyle_row[3],
        fitness_level=lifestyle_row[4],
        chronotype=lifestyle_row[5],
        work_style=lifestyle_row[6],
        travel_frequency=lifestyle_row[7],
        exercise_probability=float(
            lifestyle_row[8]
        )
    )

    behavior_profile = BehaviorProfile(
        weekday_work_probability=float(
            behavior_row[1]
        ),
        weekend_work_probability=float(
            behavior_row[2]
        ),
        exercise_probability=float(
            behavior_row[3]
        ),
        social_probability=float(
            behavior_row[4]
        ),
        travel_probability=float(
            behavior_row[5]
        )
    )

    activities = routine_row[5]

    routine_activities = RoutineActivities(
        hobbies=build_activity_list(
            activities.get(
                "hobbies",
                []
            )
        ),
        leisure_activities=build_activity_list(
            activities.get(
                "leisure_activities",
                []
            )
        ),
        exercise_activities=build_activity_list(
            activities.get(
                "exercise_activities",
                []
            )
        ),
        social_activities=build_activity_list(
            activities.get(
                "social_activities",
                []
            )
        ),
        entertainment_activities=build_activity_list(
            activities.get(
                "entertainment_activities",
                []
            )
        ),
        learning_activities=build_activity_list(
            activities.get(
                "learning_activities",
                []
            )
        ),
        travel_activities=build_activity_list(
            activities.get(
                "travel_activities",
                []
            )
        )
    )

    routine = Routine(
        weekday_wake_time=str(
            routine_row[1]
        )[:5],
        weekday_sleep_time=str(
            routine_row[2]
        )[:5],
        weekend_wake_time=str(
            routine_row[3]
        )[:5],
        weekend_sleep_time=str(
            routine_row[4]
        )[:5],
        activities=routine_activities
    )

    return SyntheticPerson(
        archetype=archetype,
        persona=persona,
        lifestyle=lifestyle,
        behavior_profile=behavior_profile,
        routine=routine
    )    