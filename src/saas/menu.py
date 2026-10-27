from src.saas.auth import register_prepod
from src.saas.repositories import mark_repository, discipline_repository, user_repository
from src.saas.services import mark_service, group_service, discipline_service, auth_service
from src.saas.services.auth_service import STUDENT_ROLE_ID

from src.saas.services.mark_service import (
    create_mark,
    get_all_marks,
    delete_mark,
    get_average
)

from src.saas.services.discipline_service import (
    create_discipline,
    get_discipline_by_id,
    get_all_disciplines,
    get_student_disciplines,
    assign_discipline_with_prepod,
    assign_discipline_with_student
)

from src.saas.services.group_service import (
    create_group,
    get_group_by_id,
    get_all_groups,
    delete_group,
    get_students_in_group
)

from src.saas.services import user_service

# =================
#       MENU
# =================

def prepod_menu(user):
    while True:
        print(f"\n---- Преподаватель ({user.login}) ----")
        print("1. Меню дисциплин")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            mark_update_menu()
        if choice == '0':
            break

def student_menu(user):
    while True:
        print(f"\n---- Студент ({user.login}) ----")
        print("1. Меню группы")
        print("2. Меню дисциплин")
        print("0. Выход")

        choice = input("Выберите действие: ")
        if choice == '1':
            if not user.group:
                print("\nОшибка, Вы не находитесь в группе")
                continue

            try:
                students = get_students_in_group(user.group)
                print(f"Список студентов вашей группы: ")
                for idx, student in enumerate(students, 1):
                    print(f"{idx}. {student.surname} {student.name} {student.patronymic}")

            except Exception as e:
                print(f"\nОшибка {e}")

        if choice == '2':
            discipline_menu(user.userID)
        if choice == '0':
            break

def discipline_menu(user):
    while True:
        disciplines = get_student_disciplines(user.userID)

        print("\n---- Ваши дисциплины ----")
        if not disciplines:
            print("У вас пока нет дисциплин с оценками")
            print("0. Назад")
            sub_choice = input("Выберите действие: ")
            if sub_choice == '0':
                break
            continue

        for idx, disc in enumerate(disciplines, 1):
            print(f"{idx}. {disc.name}")
        print("0. Назад")

        sub_choice = input("Выберите дисциплину: ")

        if sub_choice == '0':
            break
        if sub_choice.isdigit() and 1 <= int(sub_choice) <= len(disciplines):
            selected_disc = disciplines[int(sub_choice) - 1]
            all_marks = mark_repository.get_all()
            current_marks = [
                m for m in all_marks
                if m.studentID == user.userID and m.disciplineID == selected_disc.disciplineID
            ]

            print(f"\n---- {selected_disc.name} ----")

            scores = [str(m.mark) for m in current_marks]
            print(f"Ваши оценки: {', '.join(scores) if scores else 'Оценок нет'}")

            avg_score = mark_service.get_average(user.userID, selected_disc.disciplineID)
            print(f"Текущий средний балл: {avg_score:.2f}")

            input("\nНажмите Enter, чтобы вернуться к списку дисциплин...")
        else:
            print("\nОшибка: Неверный ввод. Выберете номер из списка.")

def mark_update_menu(user):
    while True:
        all_marks = mark_repository.get_all()

        prepod_disciplines_ids = {m.disciplineID for m in all_marks}
        disciplines = []
        for d_id in prepod_disciplines_ids:
            disc = discipline_repository.get_by_id(d_id)
            if disc:
                disciplines.append(disc)

        print(f"\n---- Ваши дисциплиины ----")
        if not disciplines:
            print("У вас пока нет дисциплин.")
            print("0. Назад")
            if input("Выберите действие: ") == "0":
                break
            continue
        for idx, disc in enumerate(disciplines, 1):
            print(f"{idx}. {disc.name}")
        print("0. Назад")

        choice = input("Выберите номер для просмотра студентов: ")
        if choice == '0':
            break

        if choice.isdigit() and 1 <= int(choice) <= len(disciplines):
            selected_disc = disciplines[int(choice) - 1]

            while True:
                print(f"\n---- {selected_disc.name} ----")
                print("1. Просмотреть список студентов и выствить оценку")
                print("0. Назад")

                sub_choice = input("Выберите действие: ")
                if sub_choice == '0':
                    break
                if sub_choice == '1':
                    all_users = user_repository.get_all()
                    students = [u for u in all_users if u.userRole == STUDENT_ROLE_ID]

                    print(f"\n---- Список всех студентов ----")
                    if not students:
                        print("В системе пока нет студентов.")
                        input("\nНажмите Enter для возврата...")
                        continue

                    for s_idx, std in enumerate(students, 1):
                        avg = mark_service.get_average(std.userID, selected_disc.disciplineID)
                        print(f"{s_idx}. {std.name} {std.patronymic} [Текущий ср. балл: {avg:.2f}]")
                    print("0. Назад")

                    student_choice = input("Выберите номер студента для изменения оценок: ")
                    if student_choice == '0':
                        break

                    if student_choice.isdigit() and 1 <= int(student_choice) <= len(students):
                        target_student = students[int(student_choice) - 1]

                        while True:
                            all_marks = mark_repository.get_all()
                            current_marks = [
                                m for m in all_marks
                                if m.studentID == target_student.userID and m.disciplineID == selected_disc.disciplineID
                            ]

                            print(f"\n---- Управление оценками студента: {target_student.surname} {target_student.name} {target_student.patronymic} ----")
                            print(f"Дисциплина: {selected_disc.name}")

                            if not current_marks:
                                print("У студента нет оценок по этому предмету.")
                            else:
                                print("Текуще оценки: ")
                                for m_idx, m in enumerate(current_marks, 1):
                                    print(f"{m_idx}. {m.mark}")
                                    print("\nДоступные действия:")
                                    print("1. Добавить оценку")
                                    print("2. Изменить существующую оценку")
                                    print("3. Удалить оценку")
                                    print("0. Назад к выбору студента")

                                    action = input("Выберите действие: ")

                                    if action == '0':
                                        break

                                    #  --- ВЫСТАВЛЕНИЕ ОЦЕНКИ ---
                                    elif action == '1':
                                        score_input = input("Введите оценку (1-5): ")
                                        if score_input.isdigit() and 1 <= int(score_input) <= 5:
                                            mark_repository.create(
                                                mark=int(score_input),
                                                studentID=target_student.userID,
                                                disciplineID=selected_disc.disciplineID
                                            )
                                            print("\nОценка выставлена!")
                                        else:
                                            print("Оценка должна быть числом от 1 до 5.")
                                            input("\nНажмите Enter...")

                                    #  --- ИЗМЕНЕНИЕ ОЦЕНКИ ---
                                    elif action == '2':
                                        if not current_marks:
                                            print("Нет оценок для изменения.")
                                            input("\nНажмите Enter...")
                                            continue

                                        m_choice = input("Выберите номер оценки для изменения: ")
                                        if m_choice.isdigit() and 1 <= int(m_choice) <= len(current_marks):
                                            selected_mark = current_marks[int(m_choice) - 1]

                                            new_score = input(f"Введите новую оценку (1-5): ")
                                            if new_score.isdigit() and 1 <= int(new_score) <= 5:
                                                mark_service.update_mark(selected_mark.mark, int(new_score))
                                                print("Оценка изменена!")
                                            else:
                                                print("Ошибка оценка должна быть числом от 1 до 5.")
                                        else:
                                            print("Ошибка неверный номер оценки.")
                                        input("\nНажмите Enter...")

                                    #  --- УДАЛЕНИЕ ОЦЕНКИ ---
                                    elif action == '3':
                                        if not current_marks:
                                            print("Ошибка. Нет оценок для удаления.")
                                            input("\nНажмите Enter...")
                                            continue

                                        m_choice = input("Выберите номер оценки для удаления: ")
                                        if m_choice.isdigit() and 1 <= int(m_choice) <= len(current_marks):
                                            selected_mark = current_marks[int(m_choice) - 1]
                                            confirm = input(f"Вы уверены, что хотите удалить оценку? (y/n): ")
                                            if confirm.lower() == 'y':
                                                mark_service.delete_mark(selected_mark.markID)
                                                print("\nОценка удалена!")
                                            else:
                                                print("Удаление отменено.")
                                        else:
                                            print("Ошибка. Неверный номер оценки.")
                                        input("Нажмите Enter...")

                                    else:
                                        print("Ошибка. неверный выбор студента.")
                                else:
                                    print("Ошибка. Неверный ввод. Выберите номер из списка.")


from src.saas.repositories import user_repository, group_repository
from src.saas.services import group_service, user_service


def _admin_add_student_to_group(selected_group):
    all_users = user_repository.get_all()

    available_students = [
        u for u in all_users
        if u.userRole == STUDENT_ROLE_ID and u.group != selected_group.groupID
    ]

    print(f"\n--- Добавление студентов в группу {selected_group.name} ---")
    if not available_students:
        print("В системе нет свободных студентов для добавления.")
        return

    for idx, std in enumerate(available_students, 1):
        current_group_name = "Нет группы"
        if std.group:
            g = group_repository.get_by_id(std.group)
            if g: current_group_name = g.name
        print(f"{idx}. {std.surname} {std.name} (Текущая группа: {current_group_name})")
    print("0. Назад")

    std_choice = input("Выберите номер студента для добавления в группу: ")
    if std_choice == '0':
        return

    if std_choice.isdigit() and 1 <= int(std_choice) <= len(available_students):
        target_student = available_students[int(std_choice) - 1]

        try:
            user_service.change_user_group(target_student.userID, selected_group.groupID)
            print(f"\n[Успешно] Студент {target_student.surname} переведен в группу {selected_group.name}!")
        except Exception as e:
            print(f"\n[Ошибка] {e}")
    else:
        print("[Ошибка] Неверный выбор.")


def _admin_group_management_menu():
    while True:
        print("\n---- Управление группами ----")
        print("1. Создать новую группу")
        print("2. Посмотреть список групп / Добавить студента в группу")
        print("3. Удалить группу")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == '0':
            break

        elif choice == '1':
            group_name = input("Введите название новой группы (например, 26-ИВТ-2-2): ")
            try:
                new_group = group_service.create_group(name=group_name)
                print(f"\nГруппа '{new_group.name}' создана с ID: {new_group.groupID}")
            except ValueError as e:
                print(f"\nОшибка {e}")
            input("\nНажмите Enter...")

        elif choice == '2':
            groups = group_service.get_all_groups()
            if not groups:
                print("\nВ системе пока нет созданных групп.")
                input("\nНажмите Enter...")
                continue

            print("\nСписок существующих групп:")
            for idx, gr in enumerate(groups, 1):
                print(f"{idx}. {gr.name} (ID: {gr.groupID})")
            print("0. Назад")

            g_choice = input("Выберите номер группы для управления её составом: ")
            if g_choice == '0':
                continue

            if g_choice.isdigit() and 1 <= int(g_choice) <= len(groups):
                selected_group = groups[int(g_choice) - 1]
                _admin_add_student_to_group(selected_group)
            else:
                print("[Ошибка] Неверный номер группы.")
            input("\nНажмите Enter...")

        elif choice == '3':
            groups = group_service.get_all_groups()
            if not groups:
                print("\nВ системе нет групп для удаления.")
                input("\nНажмите Enter...")
                continue

            print("\nВыберите группу для УДАЛЕНИЯ:")
            for idx, gr in enumerate(groups, 1):
                print(f"{idx}. {gr.name}")
            print("0. Назад")

            g_choice = input("Введите номер группы для удаления: ")
            if g_choice == '0':
                continue

            if g_choice.isdigit() and 1 <= int(g_choice) <= len(groups):
                selected_group = groups[int(g_choice) - 1]
                confirm = input(f"Вы уверены, что хотите БЕЗВОЗВРАТНО удалить группу {selected_group.name}? (y/n): ")

                if confirm.lower() == 'y':
                    try:
                        group_service.delete_group(selected_group.groupID)
                        print(f"\nГруппа {selected_group.name} была удалена.")
                    except ValueError as e:
                        print(f"\nОшибка {e}")
                else:
                    print("Удаление отменено.")
            else:
                print("[Ошибка] Неверный номер.")
            input("\nНажмите Enter...")


def _admin_assign_discipline_to_student(selected_disc):
    all_users = user_repository.get_all()

    students = [u for u in all_users if u.roleName == 'Student']

    print(f"\n--- Привязка дисциплины '{selected_disc.name}' студенту ---")
    if not students:
        print("В системе пока нет зарегистрированных студентов.")
        return

    for idx, std in enumerate(students, 1):
        print(f"{idx}. {std.surname} {std.name} {std.patronymic if std.patronymic else ''}")
    print("0. Назад")

    std_choice = input("Выберите номер студента для привязки предмета: ")
    if std_choice == '0':
        return

    if std_choice.isdigit() and 1 <= int(std_choice) <= len(students):
        target_student = students[int(std_choice) - 1]

        try:
            discipline_service.assign_discipline_with_student(
                disciplineID=selected_disc.disciplineID,
                studentID=target_student.userID
            )
            print(f"\n[Успешно] Дисциплина '{selected_disc.name}' успешно привязана студенту {target_student.surname}!")
        except ValueError as e:
            print(f"\n[Ошибка валидации] {e}")
        except Exception as e:
            print(f"\n[Ошибка] {e}")
    else:
        print("[Ошибка] Неверный выбор.")


def _admin_assign_discipline_to_prepod(selected_disc):
    all_users = user_repository.get_all()

    prepods = [u for u in all_users if u.roleName == 'Prepod']

    print(f"\n--- Назначение дисциплины '{selected_disc.name}' преподавателю ---")
    if not prepods:
        print("В системе пока нет зарегистрированных преподавателей.")
        return

    for idx, pr in enumerate(prepods, 1):
        print(f"{idx}. {pr.surname} {pr.name}")
    print("0. Назад")

    pr_choice = input("Выберите номер преподавателя для закрепления предмета: ")
    if pr_choice == '0':
        return

    if pr_choice.isdigit() and 1 <= int(pr_choice) <= len(prepods):
        target_prepod = prepods[int(pr_choice) - 1]

        try:
            discipline_service.assign_discipline_with_prepod(
                disciplineID=selected_disc.disciplineID,
                prepodID=target_prepod.userID
            )
            print(
                f"\nДисциплина '{selected_disc.name}' закреплена за преподавателем {target_prepod.surname}!")
        except Exception as e:
            print(f"\nОшибка {e}")
    else:
        print("Ошибка Неверный выбор.")

def _admin_discipline_management_menu():
    while True:
        print("\n---- Управление дисциплинами ----")
        print("1. Создать новую дисциплину")
        print("2. Привязать дисциплину студенту")
        print("3. Назначить дисциплину преподавателю")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == '0':
            break

        elif choice == '1':
            disc_name = input("Введите название новой дисциплины: ")
            try:
                new_disc = discipline_service.create_discipline(name=disc_name)
                print(f"\nДисциплина '{new_disc.name}' добавлена в систему.")
            except ValueError as e:
                print(f"\nОшибка {e}")
            input("\nНажмите Enter...")

        elif choice == '2':
            disciplines = discipline_repository.get_all()
            if not disciplines:
                print("\nВ системе пока нет созданных дисциплин.")
                input("\nНажмите Enter...")
                continue

            print("\nДоступные дисциплины:")
            for idx, d in enumerate(disciplines, 1):
                print(f"{idx}. {d.name}")
            print("0. Назад")

            d_choice = input("Выберите номер дисциплины: ")
            if d_choice == '0':
                continue

            if d_choice.isdigit() and 1 <= int(d_choice) <= len(disciplines):
                _admin_assign_discipline_to_student(disciplines[int(d_choice) - 1])
            else:
                print("Ошибка Неверный выбор.")
            input("\nНажмите Enter...")

        elif choice == '3':
            disciplines = discipline_repository.get_all()
            if not disciplines:
                print("\nВ системе пока нет созданных дисциплин.")
                input("\nНажмите Enter...")
                continue

            print("\nДоступные дисциплины:")
            for idx, d in enumerate(disciplines, 1):
                print(f"{idx}. {d.name}")
            print("0. Назад")

            d_choice = input("Выберите номер дисциплины: ")
            if d_choice == '0':
                continue

            if d_choice.isdigit() and 1 <= int(d_choice) <= len(disciplines):
                _admin_assign_discipline_to_prepod(disciplines[int(d_choice) - 1])
            else:
                print("[Ошибка] Неверный выбор.")
            input("\nНажмите Enter...")


def _admin_register_user_menu():
    print("\nКого вы хотите зарегистрировать?")
    print("1. Преподавателя")
    print("2. Студента")
    print("0. Назад")

    role_choice = input("Выберите тип пользователя: ")
    if role_choice == '0' or role_choice not in ['1', '2']:
        if role_choice not in ['0', '1', '2']:
            print("Ошибка Неверный выбор.")
        return

    surname = input("Введите фамилию: ")
    name = input("Введите имя: ")
    patronimik = input("Введите отчество (если нет, нажмите Enter): ")
    patronimik = patronimik.strip() if patronimik.strip() else None
    login = input("Введите логин для входа: ")
    password = input("Введите пароль: ")

    if role_choice == '1':
        try:
            user_service.register_user(
                name=name, surname=surname, patronymic=patronimik,
                login=login, password=password, is_prepod=True
            )
            print(f"\nПреподаватель {surname} зарегистрирован!")
        except Exception as e:
            print(f"\nОшибка {e}")

    elif role_choice == '2':
        groups = group_service.get_all_groups()
        if not groups:
            print("\nОшибка В системе нет ни одной группы! Сначала создайте группу.")
            return

        print("\nДоступные группы:")
        for idx, gr in enumerate(groups, 1):
            print(f"{idx}. {gr.name}")

        g_choice = input("Выберите номер группы для студента: ")
        if g_choice.isdigit() and 1 <= int(g_choice) <= len(groups):
            selected_group = groups[int(g_choice) - 1]

            try:
                user_service.register_user(
                    name=name, surname=surname, patronymic=patronimik,
                    login=login, password=password, is_prepod=False
                )

                created_user = user_repository.get_by_login(login)
                if created_user:
                    user_service.change_user_group(created_user.userID, selected_group.groupID)
                    print(f"\n Студент {surname} зарегистрирован и зачислен в группу {selected_group.name}!")
                else:
                    print("\nОшибка Не удалось привязать группу: пользователь не найден после регистрации.")
            except Exception as e:
                print(f"\nОшибка {e}")
        else:
            print("Ошибка Неверный выбор группы.")


def admin_menu(user):
    while True:
        print(f"\n---- Панель Администратора ({user.login}) ----")
        print("1. Создать учебную группу")
        print("2. Создать новую дисциплину")
        print("3. Зарегистрировать пользователя (Студента / Преподавателя)")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            _admin_group_management_menu()
            input("\nНажмите Enter...")

        elif choice == '2':
            _admin_discipline_management_menu()
            input("\nНажмите Enter...")

        elif choice == '3':
            _admin_register_user_menu()
            input("\nНажмите Enter...")

        elif choice == '0':
            print("Выход из панели администратора.")
            break

        else:
            print("Неверный выбор действия. Попробуйте снова.")

