# Student assessment accounting system

from src.saas.database.database import init_db

from src.saas.auth import (
    login,
    register,
    register_prepod
)

from src.saas.menu import student_menu, prepod_menu, admin_menu

from src.saas.services.auth_service import create_admin

def main():
    init_db()
    create_admin()
    while True:
        print("\n---- Система учета оценок студентов ----")
        print("1. Вход")
        print("2. Регистрация")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            user = login()

            if not user:
                continue

            if user.userRole == 3:
                admin_menu(user)
            elif user.userRole == 2:
                prepod_menu(user)
            else:
                student_menu(user)

        elif choice == "2":
            register()

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()