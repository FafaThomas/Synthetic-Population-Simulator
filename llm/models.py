from datetime import date
from pydantic import (
    BaseModel,
    Field,
    field_validator
)
from typing import List, Optional


class Archetype(BaseModel):
    name: str
    description: str
    age_range: list[int]
    common_occupations: list[str]
    lifestyle_summary: str

    @field_validator("age_range")
    @classmethod
    def validate_age_range(
        cls,
        value
    ):
        if len(value) != 2:
            raise ValueError(
                "age_range must contain [min,max]"
            )

        if value[0] < 0:
            raise ValueError(
                "minimum age cannot be negative"
            )

        if value[0] > value[1]:
            raise ValueError(
                "age_range min > max"
            )

        return value


class PersonaProfile(BaseModel):
    chronotype: str
    fitness_level: str
    gaming_hours_per_day: int
    exercise_probability: float

class LifestyleProfile(BaseModel):
    relationship_status: str
    hobbies: list[str]
    social_activity_level: str
    fitness_level: str
    chronotype: str
    work_style: str
    travel_frequency: str
    exercise_probability: float = Field(
    ge=0.0,
    le=1.0
    )


class Persona(BaseModel):
    id: str
    first_name: str
    last_name: str
    age: int = Field(
        ge=18,
        le=100
    )
    occupation: str
    city: str
    country: str

class RoutineActivity(BaseModel):
    name: str
    probability: float = Field(
        ge=0.0,
        le=1.0
    )
    time_slot: list[str]

class RoutineActivities(BaseModel):
    hobbies: list[RoutineActivity] = []
    leisure_activities: list[RoutineActivity] = []
    exercise_activities: list[RoutineActivity] = []
    social_activities: list[RoutineActivity] = []
    entertainment_activities: list[RoutineActivity] = []
    learning_activities: list[RoutineActivity] = []
    travel_activities: list[RoutineActivity] = []

class Routine(BaseModel):
    weekday_wake_time: str
    weekday_sleep_time: str
    weekend_wake_time: str
    weekend_sleep_time: str
    activities: RoutineActivities


class BehaviorProfile(BaseModel):
    weekday_work_probability: float = Field(
        ge=0.0,
        le=1.0
    )
    weekend_work_probability: float = Field(
        ge=0.0,
        le=1.0
    )
    exercise_probability: float = Field(
        ge=0.0,
        le=1.0
    )
    social_probability: float = Field(
        ge=0.0,
        le=1.0
    )
    travel_probability: float = Field(
        ge=0.0,
        le=1.0
    )

class DailyActivity(BaseModel):
    activity_name: str
    start_time: str
    end_time: str
    location_type: str

class DailySchedule(BaseModel):
    date: str
    wake_time: str
    sleep_time: str
    activities: list[DailyActivity]


class SyntheticPerson(BaseModel):
    archetype: Archetype
    persona: Persona
    lifestyle: LifestyleProfile
    behavior_profile: BehaviorProfile
    routine: Routine

class DayContext(BaseModel):
    simulation_date: date
    is_weekend: bool
    work_day: bool
    exercise_day: bool
    social_day: bool
    travel_day: bool
    wake_time: str
    sleep_time: str

class TimeBlock(BaseModel):
    start_time: str
    end_time: str

