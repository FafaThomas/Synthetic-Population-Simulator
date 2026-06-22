from json_utils import parse_llm_json
from qwen_client import generate

from models import (
    Persona,
    LifestyleProfile,
    BehaviorProfile,
    Routine
)


def generate_routine(
    persona: Persona,
    lifestyle: LifestyleProfile,
    behavior_profile: BehaviorProfile
) -> Routine:

    with open(
        "prompts/routine.txt",
        "r",
        encoding="utf-8"
    ) as f:

        prompt = f.read()

    prompt = prompt.replace(
        "{persona_json}",
        persona.model_dump_json(indent=4)
    )

    prompt = prompt.replace(
        "{lifestyle_json}",
        lifestyle.model_dump_json(indent=4)
    )

    prompt = prompt.replace(
        "{behavior_json}",
        behavior_profile.model_dump_json(indent=4)
    )

    for attempt in range(3):

        try:

            response = generate(prompt)

            data = parse_llm_json(response)

            if "routine" in data:
                data = data["routine"]

            return Routine.model_validate(data)

        except Exception as ex:

            print(
                f"[Retry {attempt + 1}] Routine generation failed: {ex}"
            )

    raise Exception(
        "Routine generation failed."
    )
    