from src.saas.database.database import get_connection
from src.saas.models.user import User


def _map(row) -> User:
    if not row:
        return None

    role_id = row[6]
    text_role = "Student"
    if role_id == 2:
        text_role = "Prepod"
    elif role_id == 3:
        text_role = "Admin"

    return User(
        userID=row[0],
        name=row[1],
        surname=row[2],
        patronymic=row[3],
        login=row[4],
        password_hash=row[5],
        userRole=row[6],
        group=row[7],
        group_name="Без группы",
        roleName=text_role
    )

def create(name, surname, patronymic, login, password_hash, user_role, group):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO Users(name, surname, patronymik, login, password_hash, userRole, [group])
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, surname, patronymic, login, password_hash, user_role, group))

    conn.commit()
    conn.close()


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT userID, name, surname, patronymik, login, password_hash, userRole, [group]
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
    SELECT userID, name, surname, patronymik, login, password_hash, userRole, [group]
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
    SELECT userID, name, surname, patronymik, login, password_hash, userRole, [group]
    FROM Users
    ORDER BY surname, name
    """)

    rows = cur.fetchall()
    conn.close()

    return [_map(row) for row in rows]


def update(user_id: int, user_role: int, group: int | None) -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE Users
    SET userRole = ?, [group] = ?
    WHERE userID = ?
    """, (user_role, group, user_id))

    conn.commit()
    conn.close()
