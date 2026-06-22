CREATE DATABASE IF NOT EXISTS hts;

USE hts;

CREATE TABLE IF NOT EXISTS activity_history
(
    persona_id UUID,

    activity_date Date,

    activity_name LowCardinality(String),

    start_time DateTime,

    end_time DateTime,

    location_type LowCardinality(String)
)
ENGINE = MergeTree

PARTITION BY toYYYYMM(activity_date)

ORDER BY
(
    persona_id,
    activity_date,
    start_time
);


CREATE TABLE IF NOT EXISTS telemetry_events
(
    persona_id UUID,

    device_id UUID,

    event_timestamp DateTime64(3),

    source LowCardinality(String),

    category LowCardinality(String),

    metric_group LowCardinality(String),

    metric String,

    value String
)
ENGINE = MergeTree

PARTITION BY toYYYYMM(event_timestamp)

ORDER BY
(
    persona_id,
    event_timestamp,
    device_id
);


CREATE TABLE IF NOT EXISTS daily_state
(
    persona_id UUID,

    state_date Date,

    sleep_hours Float32,

    avg_heart_rate Float32,

    total_steps UInt32,

    stress_score Float32,

    focus_score Float32,

    fatigue_score Float32,

    performance_score Float32
)
ENGINE = MergeTree

PARTITION BY toYYYYMM(state_date)

ORDER BY
(
    persona_id,
    state_date
);