from clickhouse_connect import get_client

client = get_client(
    host="localhost",
    port=8123,
    username="hts_user",
    password="hts_password"
)

print(
    client.command(
        "SELECT 1"
    )
)