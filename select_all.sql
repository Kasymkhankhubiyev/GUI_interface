DROP TABLE IF EXISTS recipe;
CREATE TABLE recipe(
id INTEGER PRIMARY KEY,
food_name TEXT,
mass_gr REAL,
product_id INTEGER,
FOREIGN KEY (product_id) REFERENCES items (id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (food_name) REFERENCES foods_cpfc (food_name) ON UPDATE CASCADE ON DELETE RESTRICT
)

INSERT INTO recipe(food_name, mass_gr, product_id)
VALUES
	('Кофе', 20.0, 1),
	('Вода', 250.0, 1),
	('Стакан 250', 100.0, 1),
	('Кофе', 20.0, 2),
	('Вода', 350.0, 2),
	('Стакан 350', 100.0, 2),
	('Кофе', 20.0, 3),
	('Вода', 60.0, 3),
	('Молоко', 130.0, 3),
	('Стакан 250', 100, 3),
	('Кофе', 20.0, 4),
	('Вода', 60.0, 4),
	('Молоко', 220.0, 4),
	('Стакан 350', 100, 4),
	('Кофе', 20.0, 5),
	('Вода', 60.0, 5),
	('Молоко', 150.0, 5),
	('Стакан 250', 100, 5),
	('Кофе', 20.0, 6),
	('Вода', 60.0, 6),
	('Молоко', 300.0, 6),
	('Стакан 400', 100, 6),
	('Кофе', 20.0, 7),
	('Вода', 60.0, 7),
	('Молоко', 180.0, 7),
	('Стакан 250', 100, 7),
	('Какао', 15.0, 8),
	('Молоко', 250.0, 8),
	('Сиров Ваниль', 15.0, 8),
	('Стакан 350', 100, 8),
	('Кофе', 20.0, 9),
	('Вода', 60.0, 9),
	('Сливки', 220.0, 9),
	('Cахар', 20.0, 9),
	('Стакан 350', 100, 9),
	('Кофе', 20.0, 10),
	('Вода', 60.0, 10),
	('Сливки', 220.0, 10),
	('Стакан 350', 100, 10),
	('Соус халва', 100, 10),
	('Кофе', 20.0, 11),
	('Вода', 60.0, 11),
	('Сливки', 110.0, 11),
	('Молоко', 110.0, 11),
	('Сироп Ваниль', 15.0, 11),
	('Сыр', 40.0, 11),
	('Стакан 350', 100, 11),
	('Кофе', 20.0, 12),
	('Вода', 60.0, 12),
	('Сливки', 220.0, 12),
	('Сахар', 20.0, 12),
	('Стакан 350', 100, 12),
	('Матча', 2.0, 13),
	('Вода', 50.0, 13),
	('Сливки', 250.0, 13),
	('Стакан 350', 100, 13),
	('Молоко', 125.0, 14),
	('Мороженное', 225.0, 14),
	('Взбитые сливки', 25.0, 14),
	('Стакан 350', 100, 15),
	('Молоко', 125.0, 15),
	('Мороженное', 160.0, 15),
	('Банан', 80.0, 15),
	('Взбитые сливки', 25.0, 15),
	('Стакан 350', 100, 15),
	('Молоко', 110.0, 16),
	('Мороженное', 170.0, 16),
	('Топпинг клубника', 30.0, 16),
	('Взбитые сливки', 25.0, 16),
	('Стакан 350', 100, 16),
	('Молоко', 130.0, 17),
	('Мороженное', 170.0, 17),
	('Топпинг шоколадный', 30.0, 17),
	('Взбитые сливки', 25.0, 17),
	('Стакан 350', 100, 17),
	('Цейлон ОР', 4.0, 18),
	('Вода', 300.0, 18),
	('Фильтр пакет', 1, 18),
	('Стакан 350', 100, 18),
	('Молочный улун', 3.0, 19),
	('Вода', 300, 19),
	('Фильтр пакет', 1, 19),
	('Стакан 350', 100, 19),
	('Ассам FBOP', 4.0, 20),
	('Вода', 300, 20),
	('Фильтр пакет', 1, 20),
	('Стакан 350', 100, 20),
	('Фрукт страсти', 5.0, 21),
	('Вода', 300, 21),
	('Фильтр пакет', 1, 21),
	('Стакан 350', 100, 21),
	('Малиновая Фантазия', 4.0, 22),
	('Вода', 300, 22),
	('Фильтр пакет', 1, 22),
	('Стакан 350', 100, 22),
	('Чабрец и мята', 3.0, 23),
	('Вода', 300, 23),
	('Фильтр пакет', 1, 23),
	('Стакан 350', 100, 23),
	('Кофе', 20.0, 24),
	('Вода', 60.0, 24),
	('Стакан 250', 100.0, 24);


cursor.execute("""SELECT item_name, ROUNd(SUM(cals), 2), ROUND(SUM(prots), 2), ROUND(SUM(fats), 2),
    ROUND(SUM(carbs), 2)
    FROM items
    JOIN (SELECT recipe.food_name as f_name, recipe.product_id as id, recipe.product_id,
    recipe.mass_gr * 0.01 * cal as cals, recipe.mass_gr * 0.01 * prot as prots, recipe.mass_gr * 0.01 * fat as
    fats, recipe.mass_gr * 0.01 * carb as carbs
    FROM recipe JOIN foods_cpfc on recipe.food_name = foods_cpfc.food_name)fee
    on items.id = fee.id GROUP BY items.id, item_name""")

    db_connection.commit()
    print(cursor.fetchall())

    print('')
    cursor.execute("""SELECT  item_name, ROUND(SUM(mass_gr * 0.01 * cal), 2), ROUND(SUM(mass_gr *0.01 * prot), 2),
    ROUND(SUM(mass_gr * 0.01 * fat), 2), ROUND(SUM(mass_gr * 0.01 * carb), 2) FROM items JOIN recipe on items.id =
    recipe.product_id JOIN foods_cpfc on recipe.food_name = foods_cpfc.food_name GROUP BY items.id, item_name;""")
    db_connection.commit()
    items = cursor.fetchall()
    for item in items:
        print(item)


CREATE TABLE order_history(
id INTEGER PRIMARY KEY,
customer_ip INTEGER,
)
