from src.saas.database.database import get_connection
from src.saas.models.user import User

def _map(row) -> User:
    return User(*row)

def create(name, surname, patronymic, login, password_hash, user_role, group):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO Users(name, surname, patronymic, login, password_hash, user_role, group)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, surname, patronymic, login, password_hash, user_role, group))

    conn.commit()
    conn.close()

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT userID, name, surname, patronymic, login, password_hash, user_role, group
    FROM Users
    WHERE login = ?
    """, login)

    row = cur.fetchone()
    conn.close()

    return _map(row) if row else None

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT userID, name, surname, patronymic, login, password_hash, user_role, group
    FROM Users
    WHERE userID = ?
    """, user_id)

    row = cur.fetchone()
    conn.close()

    return _map(row) if row else None
    
def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT userID, name, surname, patronymic, login, password_hash, user_role, group
    FROM Users
    ORDER BY surname, name
    """)

    rows = cur.fetchall()
    conn.close()

    return [_map(row) for row in rows]

