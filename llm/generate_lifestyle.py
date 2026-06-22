from json_utils import parse_llm_json
from qwen_client import generate

from models import (
    Archetype,
    Persona,
    LifestyleProfile
)


def generate_lifestyle(
    archetype: Archetype,
    persona: Persona
) -> LifestyleProfile:

    with open(
        "prompts/lifestyle.txt",
        "r",
        encoding="utf-8"
    ) as f:

        prompt = f.read()

    prompt = prompt.replace(
        "{persona_json}",
        persona.model_dump_json(indent=4)
    )

    prompt = prompt.replace(
        "{archetype_json}",
        archetype.model_dump_json(indent=4)
    )

    for attempt in range(3):

        try:

            response = generate(prompt)

            data = parse_llm_json(response)

            return LifestyleProfile.model_validate(data)

        except Exception as ex:

            print(
                f"[Retry {attempt + 1}] Lifestyle generation failed: {ex}"
            )

    raise Exception(
        "Lifestyle generation failed."
    )