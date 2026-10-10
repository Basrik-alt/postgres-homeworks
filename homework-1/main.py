"""
Скрипт для заполнения таблиц базы данных north.
"""

import csv
import os

import psycopg2

# Параметры подключения к БД
DB_CONFIG = {
    "dbname": "north",
    "user": "postgres",
    "password": "postgres",  # замени на свой пароль
    "host": "localhost",
    "port": "5432",
}


def get_connection():
    """Возвращает подключение к БД."""
    return psycopg2.connect(**DB_CONFIG)


def load_employees(cursor, file_path: str) -> None:
    """
    Загружает сотрудников из CSV в таблицу employees.

    Аргументы:
        cursor: Курсор БД.
        file_path (str): Путь к CSV-файлу.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO employees
                (employee_id, first_name, last_name, title, birth_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (employee_id) DO NOTHING;
                """,
                (
                    int(row["employee_id"]),
                    row["first_name"],
                    row["last_name"],
                    row["title"],
                    row["birth_date"],
                    row["notes"],
                ),
            )
    print("Данные о сотрудниках загружены.")


def load_customers(cursor, file_path: str) -> None:
    """
    Загружает клиентов из CSV в таблицу customers.

    Аргументы:
        cursor: Курсор БД.
        file_path (str): Путь к CSV-файлу.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO customers
                (customer_id, company_name, contact_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (customer_id) DO NOTHING;
                """,
                (
                    row["customer_id"],
                    row["company_name"],
                    row["contact_name"],
                ),
            )
    print("Данные о клиентах загружены.")


def load_orders(cursor, file_path: str) -> None:
    """
    Загружает заказы из CSV в таблицу orders.

    Аргументы:
        cursor: Курсор БД.
        file_path (str): Путь к CSV-файлу.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO orders
                (order_id, customer_id, employee_id, order_date, ship_city)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING;
                """,
                (
                    int(row["order_id"]),
                    row["customer_id"],
                    int(row["employee_id"]),
                    row["order_date"],
                    row["ship_city"],
                ),
            )
    print("Данные о заказах загружены.")


def main() -> None:
    """Главная функция."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "north_data")

    try:
        conn = get_connection()
        conn.autocommit = False
        cursor = conn.cursor()

        load_employees(cursor, os.path.join(data_dir, "employees_data.csv"))
        load_customers(cursor, os.path.join(data_dir, "customers_data.csv"))
        load_orders(cursor, os.path.join(data_dir, "orders_data.csv"))

        conn.commit()
        cursor.close()
        conn.close()
        print("Все данные успешно загружены!")

    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
