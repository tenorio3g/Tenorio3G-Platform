from sqlalchemy import select

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.models import (
    PersonModel,
)

from .person_repository import (
    PersonRepository,
)


class SQLitePersonRepository(
    PersonRepository
):

    def __init__(
        self,
        session_factory,
    ):
        self._session_factory = (
            session_factory
        )

    def save(
        self,
        person: Person,
    ) -> Person:

        with self._session_factory() as session:

            statement = select(
                PersonModel
            ).where(
                PersonModel.code
                == person.code
            )

            model = session.execute(
                statement
            ).scalar_one_or_none()

            if model is None:
                model = PersonModel(
                    code=person.code,
                    name=person.name,
                    position=person.position,
                    is_active=person.is_active,
                )

                session.add(model)

            else:
                model.name = person.name
                model.position = person.position
                model.is_active = (
                    person.is_active
                )

            session.commit()

        return person

    def get_by_code(
        self,
        code: str,
    ) -> Person | None:

        code = str(code).strip()

        with self._session_factory() as session:

            statement = select(
                PersonModel
            ).where(
                PersonModel.code == code
            )

            model = session.execute(
                statement
            ).scalar_one_or_none()

            if model is None:
                return None

            return self._to_entity(model)

    def list_all(
        self,
    ) -> list[Person]:

        with self._session_factory() as session:

            statement = select(
                PersonModel
            ).order_by(
                PersonModel.name
            )

            models = session.execute(
                statement
            ).scalars().all()

            return [
                self._to_entity(model)
                for model in models
            ]

    def delete(
        self,
        code: str,
    ) -> bool:

        code = str(code).strip()

        with self._session_factory() as session:

            statement = select(
                PersonModel
            ).where(
                PersonModel.code == code
            )

            model = session.execute(
                statement
            ).scalar_one_or_none()

            if model is None:
                return False

            session.delete(model)
            session.commit()

            return True

    @staticmethod
    def _to_entity(
        model: PersonModel,
    ) -> Person:

        return Person(
            code=model.code,
            name=model.name,
            position=model.position,
            is_active=model.is_active,
        )