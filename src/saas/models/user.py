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
    roleName: str | None = None
