from src.saas.services.auth_service import (
    authenticate_user,
    register_student,
    register_prepod,
    create_admin
)


def login():
    print("\n--- Вход в систему ---")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    user = authenticate_user(login_value, password_value)

    if not user:
        print("\nНеверный логин или пароль")
        return None

    print(f"\nДобро пожаловать, {user.name} {user.surname}")
    return user

def register():
    print("\n--- Регистрация студента ---")

    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество: ")

    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    try:
        register_student(name, surname, patronymic, login_value, password_value)
        print("\nРегистрация завершена")
    except Exception as e:
        print(f"Ошибка: {e}")

def register_prepod():
    print("\n--- Регистрация преподавателя ---")

    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество: ")

    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    try:
        register_prepod(name, surname, patronymic, login_value, password_value)
        print("\nРегистрация завершена")
    except Exception as e:
        print(f"Ошибка: {e}")