from sqlalchemy import select

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.models import (
    UserModel,
)

from .user_repository import (
    UserRepository,
)


class SQLiteUserRepository(
    UserRepository
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
        user: User,
    ) -> User:

        with self._session_factory() as session:

            statement = select(
                UserModel
            ).where(
                UserModel.username
                == user.username
            )

            model = session.execute(
                statement
            ).scalar_one_or_none()

            if model is None:

                model = UserModel(
                    username=user.username,
                    password_hash=user.password_hash,
                    person_code=user.person_code,
                    role_code=user.role_code,
                    is_active=user.is_active,
                )

                session.add(model)

            else:

                model.password_hash = (
                    user.password_hash
                )

                model.person_code = (
                    user.person_code
                )

                model.role_code = (
                    user.role_code
                )

                model.is_active = (
                    user.is_active
                )

            session.commit()

        return user

    def get_by_username(
        self,
        username: str,
    ) -> User | None:

        normalized_username = str(
            username
        ).strip().lower()

        with self._session_factory() as session:

            statement = select(
                UserModel
            ).where(
                UserModel.username
                == normalized_username
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
    ) -> list[User]:

        with self._session_factory() as session:

            statement = select(
                UserModel
            ).order_by(
                UserModel.username
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
        username: str,
    ) -> bool:

        normalized_username = str(
            username
        ).strip().lower()

        with self._session_factory() as session:

            statement = select(
                UserModel
            ).where(
                UserModel.username
                == normalized_username
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
        model: UserModel,
    ) -> User:

        return User(
            username=model.username,
            password_hash=model.password_hash,
            person_code=model.person_code,
            role_code=model.role_code,
            is_active=model.is_active,
        )