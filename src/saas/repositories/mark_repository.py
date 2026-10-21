from src.saas.database.database import get_connection
from src.saas.models.MarkList import MarkList


def create(markID: int, name: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO MarkList(
            markID,
            mark,
            avgmark,
            studentID,
            disciplineID,
        )
        VALUES(?,?,?,?,?)
    """, (markID, name))

    conn.commit()
    conn.close()

def get_all() -> list[MarkList]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT markID, mark, avgmark, studentID, disciplineID
        FROM MarkList
        ORDER BY markID
    """)

    rows = cur.fetchall()

    conn.close()

    return [
        MarkList(
            markID=row[0],
            mark=row[1],
            avgmark=row[2],
            studentID=row[3],
            disciplineID=row[4],
        )
        for row in rows
    ]

def get_by_id(markID: int) -> MarkList | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT markID, mark, avgmark, studentID, disciplineID
        FROM MarkList
        WHERE markID=?
    """, (markID,))

    row = cur.fetchone()

    if not row:
        return None

    return MarkList(
        markID=row[0],
        mark=row[1],
        avgmark=row[2],
        studentID=row[3],
        disciplineID=row[4],
    )


def delete(markID: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM MarkList
        WHERE markID=?
    """, (markID,))

    conn.commit()
    conn.close()
