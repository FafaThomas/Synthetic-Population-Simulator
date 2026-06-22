CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- ARCHETYPES
-- =====================================================

CREATE TABLE archetypes
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT NOT NULL,

    description TEXT NOT NULL,

    age_min INTEGER NOT NULL,

    age_max INTEGER NOT NULL,

    common_occupations JSONB NOT NULL,

    lifestyle_summary TEXT NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =====================================================
-- PERSONAS
-- =====================================================

CREATE TABLE personas
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    archetype_id UUID NOT NULL
        REFERENCES archetypes(id)
        ON DELETE CASCADE,

    first_name TEXT NOT NULL,

    last_name TEXT NOT NULL,

    age INTEGER NOT NULL,

    occupation TEXT NOT NULL,

    city TEXT NOT NULL,

    country TEXT NOT NULL,

    generation_version TEXT NOT NULL DEFAULT 'v1',

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =====================================================
-- LIFESTYLES
-- =====================================================

CREATE TABLE lifestyles
(
    persona_id UUID PRIMARY KEY
        REFERENCES personas(id)
        ON DELETE CASCADE,

    relationship_status TEXT,

    hobbies JSONB NOT NULL,

    social_activity_level TEXT,

    fitness_level TEXT,

    chronotype TEXT,

    work_style TEXT,

    travel_frequency TEXT,

    exercise_probability NUMERIC(5,4),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =====================================================
-- BEHAVIOR PROFILES
-- =====================================================

CREATE TABLE behavior_profiles
(
    persona_id UUID PRIMARY KEY
        REFERENCES personas(id)
        ON DELETE CASCADE,

    weekday_work_probability NUMERIC(5,4),

    weekend_work_probability NUMERIC(5,4),

    exercise_probability NUMERIC(5,4),

    social_probability NUMERIC(5,4),

    travel_probability NUMERIC(5,4),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =====================================================
-- ROUTINES
-- =====================================================

CREATE TABLE routines
(
    persona_id UUID PRIMARY KEY
        REFERENCES personas(id)
        ON DELETE CASCADE,

    weekday_wake_time TIME NOT NULL,

    weekday_sleep_time TIME NOT NULL,

    weekend_wake_time TIME NOT NULL,

    weekend_sleep_time TIME NOT NULL,

    activities JSONB NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =====================================================
-- INDEXES
-- =====================================================


CREATE TABLE registered_devices (

    id UUID PRIMARY KEY
        DEFAULT gen_random_uuid(),

    persona_id UUID NOT NULL
        REFERENCES personas(id)
        ON DELETE CASCADE,

    device_name TEXT NOT NULL,

    device_type TEXT NOT NULL,

    protocol TEXT NOT NULL,

    connection_address TEXT,

    mac_address TEXT,

    manufacturer TEXT,

    model TEXT,

    operating_system TEXT,

    first_seen TIMESTAMP,

    last_seen TIMESTAMP,

    created_at TIMESTAMP
        DEFAULT NOW()
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_personas_archetype
    ON personas(archetype_id);

CREATE INDEX idx_personas_country
    ON personas(country);

CREATE INDEX idx_personas_city
    ON personas(city);

CREATE INDEX idx_personas_occupation
    ON personas(occupation);

CREATE INDEX idx_routines_activities
    ON routines
    USING GIN (activities);

CREATE INDEX idx_lifestyles_hobbies
    ON lifestyles
    USING GIN (hobbies);