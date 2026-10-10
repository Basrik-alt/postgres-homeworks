-- SQL-команды для создания таблиц
-- Создание таблицы сотрудников
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    notes TEXT
);

-- Создание таблицы клиентов
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100) NOT NULL
);

-- Создание таблицы заказов
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    employee_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    ship_city VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
