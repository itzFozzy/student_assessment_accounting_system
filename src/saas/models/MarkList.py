from dataclasses import dataclass

@dataclass
class MarkList:
    markID: int
    mark: int
    studentID: int
    prepodID: int
    disciplineID: int
    disciplineID: int

    student_name: str | None = None
    prepod_name: str | None = None
    discipline_name: str | None = None
