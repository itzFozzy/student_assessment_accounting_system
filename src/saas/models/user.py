from dataclasses import dataclass

@dataclass
class User:
    userID: int
    name: str
    surname: str
    patronymic: str | None
    login: str
    password_hash: str
    userRole: int
    group: int

    group_name: str
    roleName: str | None = None
