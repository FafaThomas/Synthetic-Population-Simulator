from datetime import date

from person_loader import (
get_all_persona_ids
)

from history_generator import (
generate_history
)

START_DATE = date(2021,1,1)

END_DATE = date(2025,12,31)

persona_ids = get_all_persona_ids()

print(
f"Found {len(persona_ids)} personas"
)

for index, persona_id in enumerate(persona_ids):

    
    print(
        f"[{index + 1}/{len(persona_ids)}] "
        f"Generating {persona_id}"
    )

    generate_history(
        persona_id=persona_id,
        start_date=START_DATE,
        end_date=END_DATE
    )


print(
"History generation complete."
)
