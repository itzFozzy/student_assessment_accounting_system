from src.saas.repositories import mark_repository, user_repository, discipline_repository
from src.saas.models.MarkList import MarkList


def create_mark(mark: int, studentID: int, prepodID: int, disciplineID) -> None:
    if not mark:
        raise Exception('Mark cannot be empty')
    if mark > 5:
        raise Exception('Mark cannot be greater than 5')
    if mark < 1:
        raise Exception('Mark cannot be less than 1')
    if not user_repository.get_by_id(studentID):
        raise Exception('Student does not exist')
    if not user_repository.get_by_id(prepodID):
        raise Exception('Prepod does not exist')
    if not discipline_repository.get_by_id(disciplineID):
        raise Exception('Discipline does not exist')

    mark_repository.create(mark, studentID, prepodID, disciplineID)


def get_all_marks(studentID: int, disciplineID: int):
    if not user_repository.get_by_id(studentID):
        raise Exception('Student does not exist')
    if not discipline_repository.get_by_id(disciplineID):
        raise Exception('Discipline does not exist')
    return mark_repository.get_all()

def delete_mark(markID: int, studentID: int, prepodID: int, disciplineID: int):
    if not mark_repository.get_by_id(markID):
        raise Exception('Mark does not exist')

    mark_repository.delete(markID)

def get_average(studentID: int, disciplineID: int) -> float | int:
    marks = mark_repository.get_all()

    filtered_marks = [
        m.mark for m in marks
        if m.studentID == studentID and m.disciplineID == disciplineID
    ]

    if not filtered_marks:
        return 0.0

    return sum(filtered_marks) / len(filtered_marks)


