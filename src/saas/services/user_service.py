from src.saas.repositories import user_repository

from src.saas.services.auth_service import register_prepod, register_student

def register_user(name: str, surname: str, patronymic: str | None, login: str, password: str, is_prepod: bool = True) -> None:
    if is_prepod:
        register_prepod(name, surname, patronymic, login, password)
    else:
        register_student(name, surname, patronymic, login, password)


def change_user_group(user_id: int, group_id: int | None) -> None:

    user = user_repository.get_by_id(user_id)
    if not user:
        raise ValueError('User not found')

    user_repository.update(user_id=user_id, user_role=user.userRole, group=group_id)

