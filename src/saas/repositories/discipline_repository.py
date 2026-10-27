from src.saas.database.database import get_connection
from src.saas.models.disciplineList import DisciplineList


def create(name: str) -> DisciplineList:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO disciplineList(name)
        VALUES(?)
    """, (name,))

    inserted_id = cur.lastrowid

    conn.commit()
    conn.close()

    return DisciplineList(disciplineID=inserted_id, name=name)



def get_all() -> list[DisciplineList]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT disciplineID, name
        FROM disciplineList
        ORDER BY disciplineID
    """)

    rows = cur.fetchall()

    conn.close()

    return [
        DisciplineList(
            disciplineID=row[0],
            name=row[1]
        )
        for row in rows
    ]


def get_by_id(role_id: int) -> DisciplineList | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT disciplineID, name
        FROM disciplineList
        WHERE disciplineID=?
    """, (role_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return DisciplineList(
        disciplineID=row[0],
        name=row[1]
    )


def assign_to_prepod(prepod_id: int, discipline_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO MarkList(mark, avgmark, studentID, prepodID, disciplineID)
        VALUES(0, 0.0, ?, ?, ?)
    """, (None, prepod_id, discipline_id))

    conn.commit()
    conn.close()


def assign_to_student(discipline_id: int, student_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO MarkList(mark, avgmark, studentID, prepodID, disciplineID)
        VALUES(0, 0.0, ?, ?, ?)
    """, (student_id, None, discipline_id))

    conn.commit()
    conn.close()

