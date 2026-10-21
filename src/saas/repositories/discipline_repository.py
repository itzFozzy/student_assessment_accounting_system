from src.saas.database.database import get_connection
from src.saas.models.disciplineList import DisciplineList


def create(disciplineID: int, name: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO disciplineList(
            disciplineID,
            name
        )
        VALUES(?,?)
    """, (disciplineID, name))

    conn.commit()
    conn.close()


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
    """)

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return DisciplineList(
        disciplineID=row[0],
        name=row[1]
    )
