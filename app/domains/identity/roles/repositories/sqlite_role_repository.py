from sqlalchemy import select

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.models import (
    RoleModel,
)

from .role_repository import (
    RoleRepository,
)


class SQLiteRoleRepository(
    RoleRepository
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
        role: Role,
    ) -> Role:

        with self._session_factory() as session:

            statement = select(
                RoleModel
            ).where(
                RoleModel.code
                == role.code
            )

            model = session.execute(
                statement
            ).scalar_one_or_none()

            if model is None:

                model = RoleModel(
                    code=role.code,
                    name=role.name,
                    description=role.description,
                    is_active=role.is_active,
                )

                session.add(model)

            else:

                model.name = role.name
                model.description = (
                    role.description
                )
                model.is_active = (
                    role.is_active
                )

            session.commit()

        return role

    def get_by_code(
        self,
        code: str,
    ) -> Role | None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            statement = select(
                RoleModel
            ).where(
                RoleModel.code
                == normalized_code
            )

            model = session.execute(
                statement
            ).scalar_one_or_none()

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_all(
        self,
    ) -> list[Role]:

        with self._session_factory() as session:

            statement = select(
                RoleModel
            ).order_by(
                RoleModel.name
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

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            statement = select(
                RoleModel
            ).where(
                RoleModel.code
                == normalized_code
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
        model: RoleModel,
    ) -> Role:

        return Role(
            code=model.code,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
        )