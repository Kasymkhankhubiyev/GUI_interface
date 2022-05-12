SELECT item_name as "Позиция", sum(cals) as "Ккал", sum(prots) as "Белки(гр)", sum(fats) as "Жиры(гр)", sum(carbs) as "Углеводы(гр)"
FROM
    items
    JOIN (SELECT recipe.food_name as f_name, recipe.product_id as id, recipe.product_id, recipe.mass_gr/100 * cal as cals, recipe.mass_gr/100 * prot as prots, recipe.mass_gr/100 * fat as fats, recipe.mass_gr/100 * carb as carbs
        FROM recipe
        JOIN foods_cpfc on recipe.food_name = foods_cpfc.food_name)fee
        on items.id = fee.id
    GROUP BY items.id, item_name