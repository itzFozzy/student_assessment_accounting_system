import hashlib

from src.saas.models import user, group
from src.saas.repositories import user_repository
from src.saas.models.user import User

STUDENT_ROLE_ID = 1
PREPOD_ROLE_ID = 2
ADMIN_ROLE_ID = 3


def hash_password(password: str):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def authenticate_user(login: str, password: str) -> User | None:
    user = user_repository.get_by_login(login)

    if not user:
        return None

    if user.password_hash != hash_password(password):
        return None

    return user


def register_student(
        name: str,
        surname: str,
        patronymic: str | None,
        login: str,
        password: str
    ):
    if user_repository.get_by_login(login):
        raise Exception('User already registered')

    user_repository.create(
        name=name,
        surname=surname,
        patronymic=patronymic,
        login=login,
        password_hash=hash_password(password),
        user_role=STUDENT_ROLE_ID,
        group = None
    )


def register_prepod(
        name: str,
        surname: str,
        patronymic: str | None,
        login: str,
        password: str
):
    if user_repository.get_by_login(login):
        raise Exception('User already registered')

    user_repository.create(
        name=name,
        surname=surname,
        patronymic=patronymic,
        login=login,
        password_hash=hash_password(password),
        user_role=PREPOD_ROLE_ID,
        group = None
    )


def create_admin():
    if user_repository.get_by_login("admin"):
        return

    user_repository.create(
        name="System",
        surname="Admin",
        patronymic=None,
        login="admin",
        password_hash=hash_password("123"),
        user_role=ADMIN_ROLE_ID,
        group = None
    )
