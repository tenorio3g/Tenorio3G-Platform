from app.foundation.database import SessionLocal

from app.domains.identity.people.repositories import (
    SQLitePersonRepository,
)

from app.domains.identity.people.use_cases import (
    CreatePerson,
    DeletePerson,
    GetPerson,
    ListPeople,
    UpdatePerson,
)


person_repository = SQLitePersonRepository(
    SessionLocal
)

create_person = CreatePerson(
    person_repository
)

get_person = GetPerson(
    person_repository
)

list_people = ListPeople(
    person_repository
)

update_person = UpdatePerson(
    person_repository
)

delete_person = DeletePerson(
    person_repository
)