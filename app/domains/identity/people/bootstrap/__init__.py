from .people_container import (
    create_person,
    delete_person,
    get_person,
    list_people,
    person_repository,
    update_person,
)

__all__ = [
    "person_repository",
    "create_person",
    "get_person",
    "list_people",
    "update_person",
    "delete_person",
]