from json_utils import parse_llm_json
from qwen_client import generate

from models import Archetype
from models import Persona


def generate_persona(
    archetype: Archetype
) -> Persona:

    with open(
        "prompts/persona.txt",
        "r",
        encoding="utf-8"
    ) as f:

        prompt = f.read()

    prompt = prompt.replace(
        "{archetype_json}",
        archetype.model_dump_json(indent=4)
    )

    for attempt in range(3):

        try:

            response = generate(prompt)

            data = parse_llm_json(response)

            return Persona.model_validate(data)

        except Exception as ex:

            print(
                f"[Retry {attempt + 1}] Persona generation failed: {ex}"
            )

    raise Exception(
        "Persona generation failed."
    )