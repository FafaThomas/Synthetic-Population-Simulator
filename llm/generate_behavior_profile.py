from json_utils import parse_llm_json
from qwen_client import generate

from models import (
    Persona,
    LifestyleProfile,
    BehaviorProfile
)


def generate_behavior_profile(
    persona: Persona,
    lifestyle: LifestyleProfile
) -> BehaviorProfile:

    with open(
        "prompts/behavior_profile.txt",
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

    for attempt in range(3):

        try:

            response = generate(prompt)

            print("\nRAW BEHAVIOR RESPONSE:")
            print(response)
            print("\nREPR:")
            print(repr(response))

            data = parse_llm_json(response)

            return BehaviorProfile.model_validate(data)

        except Exception as ex:

            print(
                f"[Retry {attempt + 1}] Behavior profile generation failed: {ex}"
            )

    raise Exception(
        "Behavior profile generation failed."
    )