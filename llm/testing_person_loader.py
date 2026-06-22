from person_loader import load_person

person = load_person(
    "dc5aa98d-bc0e-4aca-8604-a8726ae47e22"
)

print(
    person.model_dump_json(
        indent=2
    )
)