from datetime import date
from datetime import datetime
from datetime import timedelta
import random

from models import (
    SyntheticPerson,
    DailyActivity,
    DailySchedule,
    RoutineActivity
)


def time_to_datetime(
    time_string: str
) -> datetime:

    return datetime.strptime(
        time_string,
        "%H:%M"
    )


def fits_before_sleep(
    end_time: str,
    sleep_time: str
) -> bool:

    end_dt = time_to_datetime(
        end_time
    )

    sleep_dt = time_to_datetime(
        sleep_time
    )

    #
    # Sleep after midnight
    #

    if sleep_dt.hour < 12:

        sleep_dt += timedelta(
            days=1
        )

        if end_dt.hour < 12:
            end_dt += timedelta(
                days=1
            )

    return end_dt < sleep_dt


def add_minutes(
    time_string: str,
    minutes: int
) -> str:

    dt = datetime.strptime(
        time_string,
        "%H:%M"
    )

    dt += timedelta(
        minutes=minutes
    )

    return dt.strftime(
        "%H:%M"
    )


def randomize_time(
    time_string: str,
    variance: int
) -> str:

    dt = datetime.strptime(
        time_string,
        "%H:%M"
    )

    dt += timedelta(
        minutes=random.randint(
            -variance,
            variance
        )
    )

    return dt.strftime(
        "%H:%M"
    )


def generate_day(
    person: SyntheticPerson,
    simulation_date: date
) -> DailySchedule:

    is_weekend = (
        simulation_date.weekday() >= 5
    )

    work_probability = (
        person.behavior_profile.weekend_work_probability
        if is_weekend
        else person.behavior_profile.weekday_work_probability
    )

    #
    # Wake / Sleep
    #

    if is_weekend:

        wake_time = randomize_time(
            person.routine.weekend_wake_time,
            45
        )

        sleep_time = randomize_time(
            person.routine.weekend_sleep_time,
            60
        )

    else:

        wake_time = randomize_time(
            person.routine.weekday_wake_time,
            30
        )

        sleep_time = randomize_time(
            person.routine.weekday_sleep_time,
            45
        )

    #
    # Build activity pool
    #

    routine_activities: list[RoutineActivity] = []

    routine_activities.extend(
        person.routine.activities.hobbies
    )

    routine_activities.extend(
        person.routine.activities.leisure_activities
    )

    routine_activities.extend(
        person.routine.activities.social_activities
    )

    routine_activities.extend(
        person.routine.activities.entertainment_activities
    )

    routine_activities.extend(
        person.routine.activities.learning_activities
    )

    if is_weekend:

        routine_activities.extend(
            person.routine.activities.travel_activities
        )

    #
    # Timeline
    #

    activities = []

    current_time = wake_time

    #
    # Breakfast
    #

    breakfast_end = add_minutes(
        current_time,
        30
    )

    activities.append(
        DailyActivity(
            activity_name="breakfast",
            start_time=current_time,
            end_time=breakfast_end,
            location_type="home"
        )
    )

    current_time = breakfast_end

    #
    # Work
    #

    if random.random() < work_probability:

        work_start = add_minutes(
            current_time,
            60
        )

        work_end = add_minutes(
            work_start,
            480
        )

        if fits_before_sleep(
            work_end,
            sleep_time
        ):

            activities.append(
                DailyActivity(
                    activity_name="work",
                    start_time=work_start,
                    end_time=work_end,
                    location_type="work"
                )
            )

            current_time = add_minutes(
                work_end,
                30
            )

    #
    # Routine Activities
    #

    for activity in routine_activities:

        if random.random() > activity.probability:
            continue

        duration = random.randint(
            60,
            180
        )

        activity_end = add_minutes(
            current_time,
            duration
        )

        if not fits_before_sleep(
            activity_end,
            sleep_time
        ):
            continue

        activities.append(
            DailyActivity(
                activity_name=activity.name,
                start_time=current_time,
                end_time=activity_end,
                location_type="mixed"
            )
        )

        current_time = add_minutes(
            activity_end,
            15
        )

    #
    # Exercise
    #

    for exercise in (
        person.routine.activities.exercise_activities
    ):

        if random.random() > exercise.probability:
            continue

        exercise_end = add_minutes(
            current_time,
            random.randint(
                30,
                90
            )
        )

        if not fits_before_sleep(
            exercise_end,
            sleep_time
        ):
            continue

        activities.append(
            DailyActivity(
                activity_name=exercise.name,
                start_time=current_time,
                end_time=exercise_end,
                location_type="gym"
            )
        )

        current_time = add_minutes(
            exercise_end,
            15
        )

    return DailySchedule(
        date=simulation_date.isoformat(),
        wake_time=wake_time,
        sleep_time=sleep_time,
        activities=activities
    )