from src.saas.database.database import get_connection
from src.saas.models.userRole import UserRole

def get_all() -> list[UserRole]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT userRoleID, name
        FROM userRoles
        ORDER BY userRoleID
    """)

    rows = cur.fetchall()

    conn.close()

    return [
        UserRole(
            userRoleID=row[0],
            name=row[1]
        )
        for row in rows
    ]

def get_by_id(role_id: int) -> UserRole | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT userRoleID, name
        FROM userRoles
        WHERE userRoleID=?
    """)

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return UserRole(
        userRoleID=row[0],
        name=row[1]
    )
