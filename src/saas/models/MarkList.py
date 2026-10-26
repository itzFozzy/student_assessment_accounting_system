from dataclasses import dataclass

@dataclass
class MarkList:
    markID: int
    mark: int
    studentID: int
    disciplineID: int

    student_name: str | None = None
    discipline_name: str | None = None
