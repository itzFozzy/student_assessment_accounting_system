from src.saas.repositories import user_repository, group_repository
from src.saas.models import group, user
from src.saas.services.auth_service import STUDENT_ROLE_ID


def create_group(name: str):
    if not name.strip():
        raise ValueError('Name cannot be empty')

    for group in group_repository.get_all():
        if group.name == name:
            raise ValueError('Group already exists')

    return group_repository.create(name=name)

def get_all_groups() -> list[group.Group]:
    return group_repository.get_all()


def get_group_by_id(groupID: int) -> group.Group | None:
    return group_repository.get_by_id(groupID)

def get_group_by_user(userID: int) -> group.Group | None:
    target_user = user_repository.get_by_id(userID)
    if not target_user or not target_user.group:
        raise ValueError('User does not in group')
    return group_repository.get_by_id(target_user.group)


def get_students_in_group(groupID: int) -> list[user.User]:
    if not group_repository.get_by_id(groupID):
        raise ValueError('Group does not found')

    all_users = user_repository.get_all()

    students = [
        u for u in all_users
        if u.group == groupID and u.userRole == STUDENT_ROLE_ID
    ]

    return students

def delete_group(groupID: int):
    if not group_repository.get_by_id(groupID):
        raise ValueError('Group does not found')

    group_repository.delete(groupID)
