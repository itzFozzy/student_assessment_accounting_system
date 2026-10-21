from dataclasses import dataclass

@dataclass
class MarkList:
    markID: int
    mark: int
    avgmark: float
    studentID: int
    DisciplineID: int

    student_name: str | None = None
    discipline_name: str | None = None