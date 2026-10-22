from src.saas.repositories import mark_repository, user_repository
from src.saas.models.MarkList import MarkList


def create_mark(mark: int, avgmark: float, studentID: str, disciplineID: str):

    user = user_repository.get_by_id(studentID)

    if mark > 5:
        raise Exception('mark must be less than 5')

    if mark < 1:
        raise Exception('mark must be greater than 1')


    mark_repository.create(mark, avgmark, studentID, disciplineID)
