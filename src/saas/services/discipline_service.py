from src.saas.models.disciplineList import DisciplineList
from src.saas.repositories import discipline_repository, user_repository, mark_repository


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

def get_student_disciplines(studentID: int) -> list[DisciplineList]:
    all_marks = mark_repository.get_all()
    student_marks = [m for m in all_marks if m.studentID == studentID]

    discipline_ids = {m.disciplineID for m in student_marks}

    student_disciplines = []
    for d_id in discipline_ids:
        disc = discipline_repository.get_by_id(d_id)
        if disc:
            student_disciplines.append(disc)

    return student_disciplines

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