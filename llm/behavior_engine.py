from datetime import date
from datetime import datetime
from datetime import timedelta

import random

from pydantic import BaseModel

from models import (
    SyntheticPerson,
    DailyActivity,
    DailySchedule,
    RoutineActivity,
    DayContext,
    TimeBlock
)



def randomize_time(
    time_string: str,
    variance_minutes: int
) -> str:

    dt = datetime.strptime(
        time_string,
        "%H:%M"
    )

    dt += timedelta(
        minutes=random.randint(
            -variance_minutes,
            variance_minutes
        )
    )

    return dt.strftime(
        "%H:%M"
    )

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

def to_minutes(
    time_string: str
) -> int:

    dt = datetime.strptime(
        time_string,
        "%H:%M"
    )

    return (
        dt.hour * 60
        + dt.minute
    )


def overlaps(
    start_a: str,
    end_a: str,
    start_b: str,
    end_b: str
) -> bool:

    a_start = to_minutes(start_a)
    a_end = to_minutes(end_a)

    b_start = to_minutes(start_b)
    b_end = to_minutes(end_b)

    return (
        a_start < b_end
        and
        b_start < a_end
    )

def find_available_slot(
    window_start: str,
    window_end: str,
    duration_minutes: int,
    occupied: list[TimeBlock]
):

    window_start_min = to_minutes(window_start)
    window_end_min = to_minutes(window_end)

    for _ in range(50):

        latest_start = (
            window_end_min
            - duration_minutes
        )

        if latest_start <= window_start_min:
            return None

        candidate_start = random.randint(
            window_start_min,
            latest_start
        )

        candidate_end = (
            candidate_start
            + duration_minutes
        )

        conflict = False

        for block in occupied:

            if overlaps(
                f"{candidate_start//60:02d}:{candidate_start%60:02d}",
                f"{candidate_end//60:02d}:{candidate_end%60:02d}",
                block.start_time,
                block.end_time
            ):
                conflict = True
                break

        if not conflict:

            return (
                f"{candidate_start//60:02d}:{candidate_start%60:02d}",
                f"{candidate_end//60:02d}:{candidate_end%60:02d}"
            )

    return None

def build_day_context(
    person: SyntheticPerson,
    simulation_date: date
) -> DayContext:

    is_weekend = (
        simulation_date.weekday() >= 5
    )

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

    work_probability = (
        person.behavior_profile.weekend_work_probability
        if is_weekend
        else person.behavior_profile.weekday_work_probability
    )

    return DayContext(
        simulation_date=simulation_date,
        is_weekend=is_weekend,

        work_day=(
            random.random()
            < work_probability
        ),

        exercise_day=(
            random.random()
            < person.behavior_profile.exercise_probability
        ),

        social_day=(
            random.random()
            < person.behavior_profile.social_probability
        ),

        travel_day=(
            random.random()
            < person.behavior_profile.travel_probability
        ),

        wake_time=wake_time,
        sleep_time=sleep_time
    )

LOCATION_MAP = {

    "Photography": "park",

    "Exploring local cuisine": "restaurant",

    "Learning languages": "home",

    "Walking in local parks": "park",

    "Yoga at home": "home",

    "Meet friends for coffee or drinks": "cafe",

    "Attending cultural events in Bangkok": "event",

    "Online courses or webinars related to content creation and digital marketing":
        "home",

    "Gaming": "home"
}

def resolve_location(
    activity_name: str
) -> str:

    return LOCATION_MAP.get(
        activity_name,
        "home"
    )

def generate_meals(
    context: DayContext,
    occupied: list[TimeBlock]
):

    meals = []

    #
    # Lunch
    #

    lunch_slot = find_available_slot(
        "11:30",
        "14:00",
        45,
        occupied
    )

    if lunch_slot:

        start_time, end_time = lunch_slot

        occupied.append(
            TimeBlock(
                start_time=start_time,
                end_time=end_time
            )
        )

        meals.append(
            DailyActivity(
                activity_name="Lunch",
                start_time=start_time,
                end_time=end_time,
                location_type=random.choice(
                    [
                        "home",
                        "restaurant",
                        "cafe"
                    ]
                )
            )
        )

    #
    # Dinner
    #

    dinner_slot = find_available_slot(
        "18:00",
        "21:00",
        60,
        occupied
    )

    if dinner_slot:

        start_time, end_time = dinner_slot

        occupied.append(
            TimeBlock(
                start_time=start_time,
                end_time=end_time
            )
        )

        meals.append(
            DailyActivity(
                activity_name="Dinner",
                start_time=start_time,
                end_time=end_time,
                location_type=random.choice(
                    [
                        "home",
                        "restaurant"
                    ]
                )
            )
        )

    return meals

def build_work_block(
    person: SyntheticPerson,
    context: DayContext
):

    if not context.work_day:
        return []

    occupation = (
        person.persona.occupation.lower()
    )

    remote_keywords = [
        "remote",
        "freelance",
        "consultant",
        "creator",
        "developer"
    ]

    remote_worker = any(
        keyword in occupation
        for keyword in remote_keywords
    )

    if remote_worker:

        return [

            DailyActivity(
                activity_name="Work",
                start_time="11:00",
                end_time="15:00",
                location_type="coworking"
            ),

            DailyActivity(
                activity_name="Work",
                start_time="17:00",
                end_time="20:00",
                location_type="coworking"
            )
        ]

    return [

        DailyActivity(
            activity_name="Work",
            start_time="09:00",
            end_time="17:00",
            location_type="office"
        )
    ]


def select_activities(
    person: SyntheticPerson,
    context: DayContext
):

    selected = []

    for hobby in (
        person.routine.activities.hobbies
    ):

        if random.random() < hobby.probability:

            selected.append(
                hobby
            )

        if random.random() < 0.70:

            selected.append(

                RoutineActivity(
                    name="Gaming",
                    probability=0.70,
                    time_slot=[
                        "Evening",
                        "Late night"
                    ]
                )
            )
            

    if context.exercise_day:

        for activity in (
            person.routine.activities.exercise_activities
        ):

            if random.random() < activity.probability:

                selected.append(
                    activity
                )

    if context.social_day:

        for activity in (
            person.routine.activities.social_activities
        ):

            if random.random() < activity.probability:

                selected.append(
                    activity
                )

    if context.travel_day:

        for activity in (
            person.routine.activities.travel_activities
        ):

            if random.random() < activity.probability:

                selected.append(
                    activity
                )

    for activity in (
        person.routine.activities.learning_activities
    ):

        if random.random() < activity.probability:

            selected.append(
                activity
            )

    return selected

TIME_WINDOWS = {

    "Morning":
        ("08:00", "12:00"),

    "Afternoon":
        ("12:00", "17:00"),

    "Evening":
        ("17:00", "21:00"),

    "Late night":
        ("21:00", "23:59"),

    "Weekend days":
        ("10:00", "17:00"),

    "Weekend evenings":
        ("18:00", "23:00"),

    "Extended weekends and holidays":
        ("09:00", "18:00")
}

def place_activity(
    activity: RoutineActivity,
    occupied: list[TimeBlock]
):

    slot_name = random.choice(
        activity.time_slot
    )

    if slot_name not in TIME_WINDOWS:
        return None

    window_start, window_end = (
        TIME_WINDOWS[slot_name]
    )

    duration = random.randint(
        60,
        180
    )

    free_slot = find_available_slot(
        window_start,
        window_end,
        duration,
        occupied
    )

    if not free_slot:
        return None

    start_time, end_time = free_slot

    occupied.append(
        TimeBlock(
            start_time=start_time,
            end_time=end_time
        )
    )

    return DailyActivity(
        activity_name=activity.name,
        start_time=start_time,
        end_time=end_time,
        location_type=resolve_location(
            activity.name
        )
    )

def generate_day(
    person: SyntheticPerson,
    simulation_date: date
) -> DailySchedule:

    context = build_day_context(
        person,
        simulation_date
    )

    activities = []

    occupied = []

    #
    # Breakfast
    #
    

    breakfast_start = add_minutes(
        context.wake_time,
        30
    )

    breakfast_end = add_minutes(
        breakfast_start,
        30
    )

    

    activities.append(

        DailyActivity(
            activity_name="Breakfast",
            start_time=breakfast_start,
            end_time=breakfast_end,
            location_type="home"
        )
    )

    occupied.append(
        TimeBlock(
            start_time=breakfast_start,
            end_time=breakfast_end
        )
    )
    


    #
    # Work
    #

    work_blocks = build_work_block(
        person,
        context
    )

    for block in work_blocks:

        activities.append(block)

        occupied.append(
            TimeBlock(
                start_time=block.start_time,
                end_time=block.end_time
            )
        )


    #
    # Meals
    #

    activities.extend(
        generate_meals(
            context,
            occupied
        )
    )

    #
    # Personal activities
    #

    selected = select_activities(
        person,
        context
    )

    for activity in selected:

        scheduled = place_activity(
            activity,
            occupied
        )

        if scheduled:
            activities.append(
                scheduled
            )

    activities.append(

    DailyActivity(
        activity_name="Sleep",
        start_time=context.sleep_time,
        end_time="23:59",
        location_type="home"
    )
)

    activities.sort(
        key=lambda x:
        to_minutes(
            x.start_time
        )
    )

    return DailySchedule(
        date=simulation_date.isoformat(),
        wake_time=context.wake_time,
        sleep_time=context.sleep_time,
        activities=activities
    )




