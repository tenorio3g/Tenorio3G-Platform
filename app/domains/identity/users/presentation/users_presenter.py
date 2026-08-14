from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.users.entities import (
    User,
)

from .users_view_model import (
    UserItemViewModel,
    UsersViewModel,
)


class UsersPresenter:

    @staticmethod
    def present(
        users: list[User],
        people: list[Person],
        roles: list[Role],
    ) -> UsersViewModel:

        people_by_code = {
            person.code: person
            for person in people
        }

        roles_by_code = {
            role.code: role
            for role in roles
        }

        ordered_users = sorted(
            users,
            key=lambda user: user.username,
        )

        items = []

        for user in ordered_users:

            person = people_by_code.get(
                user.person_code
            )

            role = roles_by_code.get(
                user.role_code
            )

            items.append(
                UserItemViewModel(
                    username=user.username,
                    person_code=user.person_code,
                    person_name=(
                        person.name
                        if person
                        else "Persona no encontrada"
                    ),
                    role_code=user.role_code,
                    role_name=(
                        role.name
                        if role
                        else "Rol no encontrado"
                    ),
                    status=(
                        "Activo"
                        if user.is_active
                        else "Inactivo"
                    ),
                    is_active=user.is_active,
                )
            )

        return UsersViewModel(
            items=items
        )