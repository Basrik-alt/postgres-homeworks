-- Подключиться к БД Northwind и сделать следующие изменения:

-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products
ADD CONSTRAINT check_unit_price CHECK (unit_price > 0);

-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
ALTER TABLE products
ADD CONSTRAINT check_discontinued CHECK (discontinued IN (0, 1));

-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
CREATE TABLE discontinued_products AS
SELECT * FROM products
WHERE discontinued = 1;

-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Чтобы не нарушить foreign key в order_details, мы временно меняем поведение ключа или удаляем связи.
-- Самый безопасный вариант для учебной БД: удалить связанные записи из order_details, а затем из products.
-- Но если нужно сохранить order_details, то используем ON DELETE CASCADE (в условии сказано "Подумайте, как это можно решить").
-- Так как мы создали копию discontinued_products, мы можем безопасно удалить из order_details те записи,
-- которые ссылаются на удаляемые продукты, иначе база выдаст ошибку.
DELETE FROM order_details
WHERE product_id IN (SELECT product_id FROM products WHERE discontinued = 1);

DELETE FROM products
WHERE discontinued = 1;