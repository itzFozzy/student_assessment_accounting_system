from src.saas.models.disciplineList import DisciplineList
from src.saas.repositories import discipline_repository, user_repository


def create_discipline(name: str):
    if not name.strip():
        raise ValueError("Discipline name cannot be empty")

    for d in discipline_repository.get_all():
        raise ValueError("Discipline already exists")

    return discipline_repository.create(name)

def get_discipline_by_id(disciplineID: int) -> DisciplineList | None:
    return discipline_repository.get_by_id(disciplineID)

def get_all_disciplines() -> list[DisciplineList]:
    return discipline_repository.get_all()

def assign_discipline_with_prepod(disciplineID: int, prepodID: int) -> None:
    prepod = user_repository.get_by_id(prepodID)
    if not prepod:
        raise ValueError("User does not exist")
    if prepod.roleName != 'Prepod':
        raise ValueError("User is not a prepod")
    disciplne = discipline_repository.get_by_id(disciplineID)
    if not disciplne:
        raise ValueError("Discipline does not exist")

    discipline_repository.assign_to_prepod(prepodID, disciplineID)

def assign_discipline_with_student(disciplineID: int, studentID: int) -> None:
    student = user_repository.get_by_id(studentID)
    if not student:
        raise ValueError("User does not exist")
    if student.roleName != 'Student':
        raise ValueError("User is not a student")
    discipline = discipline_repository.get_by_id(disciplineID)
    if not discipline:
        raise ValueError("Discipline does not exist")

    discipline_repository.assign_to_student(disciplineID, studentID)