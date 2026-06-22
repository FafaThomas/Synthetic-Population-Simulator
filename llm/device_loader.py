from db import get_connection


def load_devices(
    persona_id
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            device_name,
            device_type,
            manufacturer,
            model,
            protocol,
            connection_address,
            mac_address
        FROM registered_devices
        WHERE persona_id = %s
        """,
        (persona_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    devices = []

    for row in rows:

        devices.append(
            {
                "id": str(row[0]),
                "device_name": row[1],
                "device_type": row[2],
                "manufacturer": row[3],
                "model": row[4],
                "protocol": row[5],
                "connection_address": row[6],
                "mac_address": row[7]
            }
        )

    return devices