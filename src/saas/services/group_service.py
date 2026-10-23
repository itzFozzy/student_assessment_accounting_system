from src.saas.repositories import user_repository, group_repository
from src.saas.models import group


def create_group(name: str):
    if not name.strip():
        raise ValueError('Name cannot be empty')

    for group in group_repository.get_all():
        if group.name == name:
            raise ValueError('Group already exists')

    return group_repository.create(name=name)

def get_all_books() -> list[group.Group]:
    return group_repository.get_all()


def get_group_by_id(groupID: int) -> group.Group | None:
    return group_repository.get_by_id(groupID)


def delete_group(groupID: int):
    if not group_repository.get_by_id(groupID):
        raise ValueError('Group does not found')

    group_repository.delete(groupID)

def create_group(name: str):
    if not name.strip():
        raise ValueError('Name cannot be empty')

    for group in group_repository.get_all():
        if group.name == name:
            raise ValueError('Group already exists')

    return group_repository.create(name=name)

def get_all_books() -> list[group.Group]:
    return group_repository.get_all()


def get_group_by_id(groupID: int) -> group.Group | None:
    return group_repository.get_by_id(groupID)


def delete_group(groupID: int):
    if not group_repository.get_by_id(groupID):
        raise ValueError('Group does not found')

    group_repository.delete(groupID)
