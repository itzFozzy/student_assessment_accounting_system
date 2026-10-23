from src.saas.repositories import user_repository


def authenticate(login, password_hash):
    return user_repository.get_by_credentials(login, password_hash)
