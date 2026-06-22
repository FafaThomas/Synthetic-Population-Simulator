import random
import uuid

from db import get_connection


DEVICE_TEMPLATES = {

    "phone": {
        "manufacturer": "Apple",
        "model": "iPhone 14 Pro Max",
        "protocol": "WebSocket",
        "connection_address": "wss://mobile-api.synaptica.local"
    },

    "desktop": {
        "manufacturer": "Custom Build",
        "model": "Windows Workstation",
        "protocol": "REST+WebSocket",
        "connection_address": "https://desktop-api.synaptica.local"
    },

    "smart_watch": {
        "manufacturer": "Samsung",
        "model": "Galaxy Watch 6",
        "protocol": "MQTT",
        "connection_address": "mqtt://watch-broker.synaptica.local"
    }
}


def generate_mac():

    return ":".join(

        f"{random.randint(0,255):02X}"

        for _ in range(6)

    )

def generate_address(
    persona_id,
    device_type
):
    return (
        f"{device_type}-"
        f"{str(persona_id)[:8]}"
        ".synaptica.local"
    )

def build_device(
    persona_id,
    device_type,
    owner_name
):

    template = DEVICE_TEMPLATES[device_type]

    return {
        "id": str(uuid.uuid4()),
        "persona_id": str(persona_id),

        "device_name": (
            f"{owner_name}'s "
            f"{template['model']}"
        ),

        "device_type": device_type,

        "manufacturer":
            template["manufacturer"],

        "model":
            template["model"],

        "protocol":
            template["protocol"],

        "connection_address":
            generate_address(
                persona_id,
                device_type
            ),

        "mac_address":
            generate_mac()
    }

def load_personas():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            first_name,
            last_name
        FROM personas
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def has_devices(
    conn,
    persona_id
):

    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM registered_devices
        WHERE persona_id = %s
        """,
        (persona_id,)
    )

    count = cur.fetchone()[0]

    cur.close()

    return count > 0

def insert_devices(
    conn,
    devices
):

    cur = conn.cursor()

    for device in devices:

        cur.execute(
            """
            INSERT INTO registered_devices
            (
                id,
                persona_id,

                device_name,
                device_type,

                manufacturer,
                model,

                protocol,
                connection_address,

                mac_address
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                device["id"],
                device["persona_id"],

                device["device_name"],
                device["device_type"],

                device["manufacturer"],
                device["model"],

                device["protocol"],
                device["connection_address"],

                device["mac_address"]
            )
        )

    conn.commit()

    cur.close()


def generate_devices():

    personas = load_personas()

    conn = get_connection()

    total = 0

    for persona_id, first_name, last_name in personas:

        if has_devices(
            conn,
            persona_id
        ):
            continue

        owner_name = (
            f"{first_name}"
        )

        devices = [

            build_device(
                persona_id,
                "phone",
                owner_name
            ),

            build_device(
                persona_id,
                "desktop",
                owner_name
            ),

            build_device(
                persona_id,
                "smart_watch",
                owner_name
            )
        ]

        insert_devices(
            conn,
            devices
        )

        total += len(devices)

        print(
            f"Generated devices for "
            f"{first_name} {last_name}"
        )

    conn.close()

    print(
        f"\nGenerated "
        f"{total} devices"
    )


if __name__ == "__main__":

    generate_devices()




