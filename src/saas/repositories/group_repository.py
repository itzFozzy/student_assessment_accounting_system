from src.saas.database.database import get_connection
from src.saas.models.group import Group

def create(name: str) -> Group:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO GroupList(name)
        VALUES(?)
    """, (name,)) # Обязательно в кортеже!
    inserted_id = cur.lastrowid
    conn.commit()
    conn.close()
    return Group(groupID=inserted_id, name=name)

def get_all() -> list[Group]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT groupID, name
        FROM GroupList
        ORDER BY groupID
    """)
    rows = cur.fetchall()
    conn.close()
    return [Group(groupID=row[0], name=row[1]) for row in rows]

def get_by_id(groupID: int) -> Group | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT groupID, name
        FROM GroupList
        WHERE groupID=?
    """, (groupID,)) # Обязательно в кортеже!
    row = cur.fetchone()
    conn.close()
    if not row: return None
    return Group(groupID=row[0], name=row[1])

def delete(groupID: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM GroupList
        WHERE groupID=?
    """, (groupID,))
    conn.commit()
    conn.close()
