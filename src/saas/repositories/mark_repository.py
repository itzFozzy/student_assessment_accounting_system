from src.saas.database.database import get_connection
from src.saas.models.MarkList import MarkList


def create(mark:int, studentID: int, disciplineID: int) -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO MarkList(
            mark,
            studentID,
            disciplineID
        )
        VALUES(?,?,?)
    """, (mark, studentID, disciplineID))

    conn.commit()
    conn.close()

def get_all() -> list[MarkList]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT markID, mark, studentID, disciplineID
        FROM MarkList
        ORDER BY markID
    """)

    rows = cur.fetchall()

    conn.close()

    return [
        MarkList(
            markID=row[0],
            mark=row[1],
            studentID=row[2],
            disciplineID=row[3],
        )
        for row in rows
    ]

def get_by_id(markID: int) -> MarkList | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT markID, mark, studentID, disciplineID
        FROM MarkList
        WHERE markID=?
    """, (markID,))

    row = cur.fetchone()

    if not row:
        return None

    return MarkList(
        markID=row[0],
        mark=row[1],
        studentID=row[2],
        disciplineID=row[3],
    )

def update_mark(markID: int, new_mark:int) -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE MarkList
        SET mark=?,
        WHERE markID = ?
    """, (new_mark, markID))

    conn.commit()
    conn.close()


def delete(markID: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM MarkList
        WHERE markID=?
    """, markID)

    conn.commit()
    conn.close()
