from src.saas.database.database import get_connection
from src.saas.models.user import User

def _map(row) -> User:
    return User(*row)

def create(name, surname, patronymic, login, password_hash, user_role):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO Users(name, surname, patronymic, login, password_hash, user_role)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, surname, patronymic, login, password_hash, user_role))

    conn.commit()
    conn.close()

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT userID, name, surname, patronymic, login, password_hash, user_role
    FROM Users
    WHERE login = ?
    """, (login,))

    row = cur.fetchone()
    conn.close()

    return _map(row) if row else None

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT userID, name, surname, patronymic, login, password_hash, user_role
    FROM Users
    WHERE userID = ?
    """, (user_id,))

    row = cur.fetchone()
    conn.close()

    return _map(row) if row else None

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT userID, name, surname, patronymic, login, password_hash, user_role
    FROM Users
    ORDER BY surname, name
    """)

    rows = cur.fetchall()
    conn.close()

    return [_map(row) for row in rows]

