from json_utils import parse_llm_json
from qwen_client import generate
from models import Archetype


def generate_archetype() -> Archetype:

    with open(
        "prompts/archetype.txt",
        "r",
        encoding="utf-8"
    ) as f:

        prompt = f.read()

    for attempt in range(3):

        try:

            response = generate(prompt)

            data = parse_llm_json(response)

            return Archetype.model_validate(data)

        except Exception as ex:

            print(
                f"[Retry {attempt + 1}] Archetype generation failed: {ex}"
            )

    raise Exception(
        "Archetype generation failed."
    )