from dotenv import load_dotenv
from clickhouse_connect import get_client

import os

load_dotenv()

client = get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=int(os.getenv("CLICKHOUSE_PORT")),
    username=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
    database=os.getenv("CLICKHOUSE_DB")
)

def insert_events(events):

    rows = []

    for event in events:

        rows.append(
            [
                event.persona_id,
                event.device_id,
                event.timestamp,
                event.source,
                event.category,
                event.metric_group,
                event.metric,
                str(event.value)
            ]
        )

    if rows:

        client.insert(
            "telemetry_events",
            rows
        )