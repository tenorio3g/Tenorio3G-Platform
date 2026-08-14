from app.domains.identity.people.entities import (
    Person,
)

from .people_view_model import (
    PersonItemViewModel,
    PeopleViewModel,
)


class PeoplePresenter:

    @staticmethod
    def present(
        people: list[Person],
    ) -> PeopleViewModel:

        ordered_people = sorted(
            people,
            key=lambda person: person.name.lower(),
        )

        items = [
            PersonItemViewModel(
                code=person.code,
                name=person.name,
                position=(
                    person.position
                    or "Sin puesto registrado"
                ),
                status=(
                    "Activo"
                    if person.is_active
                    else "Inactivo"
                ),
                is_active=person.is_active,
            )
            for person in ordered_people
        ]

        return PeopleViewModel(
            items=items
        )