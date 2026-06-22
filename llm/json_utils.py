# json_utils.py

import json


def parse_llm_json(
    response: str
):

    response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    open_braces = response.count("{")
    close_braces = response.count("}")

    while close_braces < open_braces:
        response += "}"
        close_braces += 1

    return json.loads(response)