import csv
import json
import os
import sys
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import yaml

# Настраиваем пути поиска Python для корректной работы пакетов
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # repositories
REPOSITORIES_DIR = CURRENT_DIR
SAAS_DIR = os.path.dirname(REPOSITORIES_DIR)  # saas
SRC_DIR = os.path.dirname(SAAS_DIR)  # src

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Импортируем get_connection и модуль database
from saas.database import database
from saas.database.database import get_connection

# Указываем абсолютный путь к вашей рабочей базе данных saas.db
database.DB_NAME = os.path.join(SAAS_DIR, "saas.db")

# Настраиваем путь к папке out внутри repositories
OUTPUT_DIR = os.path.join(REPOSITORIES_DIR, "out")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_marks_with_users():
    print(f"Подключение к базе данных по пути: {database.DB_NAME}")

    conn = get_connection()
    cursor = conn.cursor()

    # Явный SQL-запрос с присвоением уникальных алиасов всем полям
    query = """
    SELECT 
        m.markID          AS m_markID, 
        m.mark            AS m_mark, 
        m.avgmark         AS m_avgmark, 
        m.studentID       AS m_studentID, 
        m.prepodID        AS m_prepodID, 
        m.disciplineID    AS m_disciplineID,
        u.userID          AS u_userID, 
        u.name            AS u_name, 
        u.surname         AS u_surname, 
        u.patronymik      AS u_patronymik, 
        u.login           AS u_login, 
        u.password_hash   AS u_password_hash, 
        u.userRole        AS u_userRole, 
        u.[group]         AS u_group
    FROM MarkList m
    LEFT JOIN Users u ON m.studentID = u.userID
    """
    cursor.execute(query)

    # Получаем имена колонок из описания курсора
    columns = [col[0] for col in cursor.description]

    marks_list = []
    for row in cursor.fetchall():
        row_dict = dict(zip(columns, row))

        # Собираем вложенную структуру студента, если он привязан к оценке
        if row_dict["u_userID"] is not None:
            student_data = {
                "userID": row_dict["u_userID"],
                "name": row_dict["u_name"],
                "surname": row_dict["u_surname"],
                "patronymik": row_dict["u_patronymik"],
                "login": row_dict["u_login"],
                "password_hash": row_dict["u_password_hash"],
                "userRole": row_dict["u_userRole"],
                "group": row_dict["u_group"],
            }
        else:
            student_data = None

        # Формируем итоговый объект оценки
        mark_entry = {
            "markID": row_dict["m_markID"],
            "mark": row_dict["m_mark"],
            "avgmark": row_dict["m_avgmark"],
            "studentID": row_dict["m_studentID"],
            "prepodID": row_dict["m_prepodID"],
            "disciplineID": row_dict["m_disciplineID"],
            "student": student_data,
        }
        marks_list.append(mark_entry)

    conn.close()

    if not marks_list:
        print(
            "Экспорт отменен: таблицы найдены, но в MarkList нет ни одной записи."
        )
        return

    # =====================================================================
    # СОХРАНЕНИЕ В ФАЙЛЫ
    # =====================================================================

    # 1. JSON
    json_path = os.path.join(OUTPUT_DIR, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(marks_list, f, ensure_ascii=False, indent=4)

    # 2. YAML
    yaml_path = os.path.join(OUTPUT_DIR, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(
            marks_list,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )

    # 3. CSV (Разворачиваем вложенность в плоскую строку)
    csv_path = os.path.join(OUTPUT_DIR, "data.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "markID",
                "mark",
                "avgmark",
                "studentID",
                "prepodID",
                "disciplineID",
                "student_userID",
                "student_name",
                "student_surname",
                "student_patronymik",
                "student_login",
                "student_password_hash",
                "student_userRole",
                "student_group",
            ]
        )
        for item in marks_list:
            s = item["student"]
            writer.writerow(
                [
                    item["markID"],
                    item["mark"],
                    item["avgmark"],
                    item["studentID"],
                    item["prepodID"],
                    item["disciplineID"],
                    s["userID"] if s else "",
                    s["name"] if s else "",
                    s["surname"] if s else "",
                    s["patronymik"] if s else "",
                    s["login"] if s else "",
                    s["password_hash"] if s else "",
                    s["userRole"] if s else "",
                    s["group"] if s else "",
                ]
            )

    # 4. XML
    root = ET.Element("markLists")
    for item in marks_list:
        ml_el = ET.SubElement(root, "markList")
        ET.SubElement(ml_el, "markID").text = str(item["markID"])
        ET.SubElement(ml_el, "mark").text = str(item["mark"])
        ET.SubElement(ml_el, "avgmark").text = str(item["avgmark"])
        ET.SubElement(ml_el, "studentID").text = str(item["studentID"])
        ET.SubElement(ml_el, "prepodID").text = str(item["prepodID"])
        ET.SubElement(ml_el, "disciplineID").text = str(item["disciplineID"])

        student_el = ET.SubElement(ml_el, "student")
        s = item["student"]
        if s:
            ET.SubElement(student_el, "userID").text = str(s["userID"])
            ET.SubElement(student_el, "name").text = s["name"]
            ET.SubElement(student_el, "surname").text = s["surname"]
            ET.SubElement(student_el, "patronymik").text = s["patronymik"]
            ET.SubElement(student_el, "login").text = s["login"]
            ET.SubElement(student_el, "password_hash").text = s["password_hash"]
            ET.SubElement(student_el, "userRole").text = str(s["userRole"])
            ET.SubElement(student_el, "group").text = str(s["group"])
        else:
            student_el.set("nil", "true")

    xml_path = os.path.join(OUTPUT_DIR, "data.xml")
    xml_str = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(
        indent="    ", encoding="utf-8"
    )
    with open(xml_path, "wb") as f:
        f.write(pretty_xml)

    print(f"\n[УСПЕХ] Все 4 файла успешно созданы в папке: {OUTPUT_DIR}")


if __name__ == "__main__":
    export_marks_with_users()
