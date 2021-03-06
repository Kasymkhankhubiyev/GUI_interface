import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3 as db
import random

import button
import mylabel
import admin
import MySpinBox
import customer
import customercabinet


# sql_query = '''INSERT INTO login_passwd(login, passwd)
#                 VALUES
#                     ('k.khubiev','12345'),
#                     ('m.solomin', '12345');'''


def get_items(item_id):
    labls = []
    sql = """SELECT item_name FROM items WHERE type_id = ?"""
    cursor.execute(sql, [item_id])
    db_connection.commit()
    lists = cursor.fetchall()
    for item in lists:
        labls.append(item[0])
        # print(item)
    return labls


def on_closing():
    if messagebox.askokcancel('Выход из приложения', 'Хотите выйти?'):
        win.destroy()
        db_connection.close()


def create_window():
    window = tk.Tk()
    window.title("RNBCoffee")
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    w //= 2  # центрируем
    h //= 2
    w -= 350  # переносим левый верхний угол
    h -= 250
    window.geometry("700x500+{}+{}".format(w, h))
    icon = tk.PhotoImage(file='rnb.png')
    window.iconphoto(False, icon)
    return window


def add_to_basket(spin):  #(button):
    item_id = spin.get_spinbox_id()     #button.get_button_id()
    value = spinbox_list[item_id].get()
    item_type_id = spin.get_item_type()
    item_name = item_list[item_id].get_item_name()
    sql = """SELECT cost FROM items WHERE type_id = ? and item_name = ?"""  # хорошо бы делать выборку по типу товара, а потом по имени.
    cursor.execute(sql, [item_type_id, item_name])
    cost = cursor.fetchall()
    items = [item_name, str(value), int(cost[0][0]) * int(value)]
    names = []
    if value != '0':  # если выбрано больше 0 единиц товара
        if len(basket_list) != 0:
            for i in range(len(basket_list)):
                i_name = basket_list[i][0]
                names.append(i_name)
            if item_name in names:
                k = names.index(item_name)
                basket_list[k][1] = value
                basket_list[k][2] =items[2]  # int(basket_list[k][2]) * int(value)
            else:
                basket_list.append(items)
        else:
            basket_list.append(items)
    else:  # выбрали 0 единиц товара
        if len(basket_list) != 0:
            for i in range(len(basket_list)):
                i_name = basket_list[i][0]
                names.append(i_name)
            if item_name in names:
                k = names.index(item_name)
                basket_list.pop(k)  # удаляем из списка т.к. нулевое кол-во
        else:
            pass
    fill_basket()
    win.update()


def sum_calories(calories):
    calories_amount = 0
    for item in calories:
        calories_amount += item[0]
    return calories_amount

def order_coast(items):
    cost = 0
    for i in range(len(items)):
        cost += items[i][2]
        print(items[i])
    return cost


def basket_with_calories():
    rows = 0
    lists = basket_table.grid_slaves()
    for j in lists:
        j.destroy()

    columns = (1, 2, 3)
    tree = ttk.Treeview(basket_table, show="headings", column=columns, height=7)
    tree.heading(1, text='Наименование')
    tree.heading(2, text='кол-во')
    tree.column(2, minwidth=60, width=100, stretch=False)
    tree.heading(3, text='стоимость')
    ysb = ttk.Scrollbar(basket_table, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=ysb.set)

    for item in basket_list:
        tree.insert("", tk.END, values=item)
        rows += 1

    tree.grid(row=0, column=0, sticky=tk.W+tk.E)
    ysb.grid(row=0, column=1, sticky=tk.N + tk.S)

    tk.Label(basket_table, text="Расчет КБЖУ и Стоимости", font=('Arial', 15)).grid(row=1, column=0, padx=10, pady=5)
    # tk.Button(basket_table, text='Рассчитать КБЖУ и Стоимость', command=calculate_calories, font=('Arial', 12)).grid(
    #     row=1, column=0, padx=10, pady=5)

    columns = (1, 2)
    caltree = ttk.Treeview(basket_table, show="headings", column=columns, height=7)
    tree.column('#0', minwidth=20, width=100, stretch=False)
    caltree.heading(1, text='Наименование')
    caltree.heading(2, text='калории - белки - жиры - углеводы')
    tree.column(2, minwidth=10, width=100, stretch=False)
    scrollbar = tk.Scrollbar(basket_table, orient=tk.VERTICAL, command=tree.yview)
    caltree.configure(yscroll=scrollbar.set)

    for i in range(len(basket_list)):
        arr = [basket_list[i][0], str(calories_list[i][0])+' - '+str(calories_list[i][1])+' - '+str(calories_list[i][2])+' - '+str(calories_list[i][3])]
        caltree.insert("", tk.END, values=arr)
    caltree.grid(row=2, column=0, sticky=tk.W+tk.E)
    scrollbar.grid(row=2, column=1, sticky=tk.N + tk.S)

    sum_cal = sum_calories(calories_list)
    final_cost = order_coast(basket_list)

    tk.Label(basket_table, text=('Всего каллорий:   ' + str(sum_cal)), font=('Aria', 12)).grid(row=3, column=0, padx=10, pady=5)
    tk.Label(basket_table, text=('Стоимость заказа: ' + str(final_cost)), font=('Aria', 12)).grid(row=4, column=0, padx=10, pady=5)

    tk.Button(basket_table, text='Подтвердить заказ', font=('Arial', 12), command=insetr_order).grid(row=5, column=0, padx=10, pady=5)
    win.update()

def insetr_order():
    for i in basket_list:
        print(i)
    customer= customer_table.return_customer()
    if customer.return_uid() is not None:
        sql = """INSERT INTO order_history(customer_id, order_date, order_status)
        VALUES (?, datetime('now'), 'ГОТОВИТСЯ')"""
        cursor.execute(sql, [customer.return_uid()])
        sql = """SELECT id FROM order_history ORDER BY id DESC LIMIT 1"""
        cursor.execute(sql)
        db_connection.commit()
        number = cursor.fetchall()
        print(number[0][0])
        for item in basket_list:
            sql = "SELECT type_id FROM items WHERE item_name = ?"
            cursor.execute(sql, [item[0]])
            db_connection.commit()
            type_id = cursor.fetchall()
    else:
        messagebox.showerror(title='Error', message='Для заказа нужно войти в систему!')


def fill_basket():  # basket_list, basket_table):
    lists = basket_table.grid_slaves()
    for j in lists:
        j.destroy()

    columns = (1, 2, 3)
    tree = ttk.Treeview(basket_table, show="headings", column=columns, height=7)
    #tree.column('#0', minwidth=20, width=100, stretch=False)
    tree.heading(1, text='Наименование')
    tree.heading(2, text='кол-во')
    tree.column(2, minwidth=30, width=100, stretch=False)
    tree.heading(3, text='стоимость')
    tree.column(3, minwidth=90, width=150, stretch=False)
    ysb = ttk.Scrollbar(basket_table, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=ysb.set)

    for item in basket_list:
        tree.insert("", tk.END, values=item)

    tree.grid(row=0, column=0)
    ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
    tk.Label(basket_table, text="Расчет КБЖУ и Стоимости", font=('Atial', 17)).grid(row=len(basket_list) + 1, column=0, padx=10, pady=5)
    #tk.Button(basket_table, text='Рассчитать КБЖУ и Стоимость', command=calculate_calories, font=('Arial', 12)).grid(row=len(basket_list) + 1,
    #                                                                                     column=0, padx=10, pady=5)
    calculate_calories()

def calculate_calories():
    calories_list.clear()
    items = []
    result = []
    amount = []
    total_cal = 0

    if len(basket_list) != 0:
        for i in range(len(basket_list)):
            item = basket_list[i][0]
            items.append(item)  # got list of items
            number = int(basket_list[i][1])
            amount.append(number)

        sql = ("""SELECT item_name, ROUNd(SUM(cals), 2), ROUND(SUM(prots), 2), ROUND(SUM(fats), 2), 
        ROUND(SUM(carbs), 2) 
        FROM items 
        JOIN (SELECT recipe.food_name as f_name, recipe.product_id as id, recipe.product_id, 
            recipe.mass_gr * 0.01 * cal as cals, recipe.mass_gr * 0.01 * prot as prots, recipe.mass_gr * 0.01 * fat as 
            fats, recipe.mass_gr * 0.01 * carb as carbs 
            FROM recipe JOIN foods_cpfc on recipe.food_name = foods_cpfc.food_name)fee 
        on items.id = fee.id WHERE item_name = ? 
        GROUP BY items.id, item_name""")

        for item in items:
            cursor.execute(sql, [item])
            db_connection.commit()
            lists = cursor.fetchall()
            print(lists)
            result.append(lists)
        for i in range(len(result)):
            res = [amount[i] * result[i][0][1], amount[i] * result[i][0][2], amount[i] * result[i][0][3],
                   amount[i] * result[i][0][4]]
            calories_list.append(res)
            total_cal += amount[i] * result[i][0][1]
            print(res)
        basket_with_calories()
    else:
        pass

def clear_basket(button):
    item_id = button.get_button_id()
    item_name = item_list[item_id].get_item_name()
    names = []
    if len(basket_list) != 0:
        for i in range(len(basket_list)):
            i_name = basket_list[i][0]
            names.append(i_name)
        if item_name in names:
            k = names.index(item_name)
            basket_list.pop(k)  # удаляем из списка т.к. нулевое кол-во
            spinbox_list[item_id].delete(0, 1)
            spinbox_list[item_id].insert(0, 0)
            add_to_basket(spinbox_list[item_id])
    else:
        pass

def prod_win_construct(table, prod_list, items_list, spinboxs_list, buttons_list, row_counter, item_type):
    for row in range(len(prod_list)):
        lbl = mylabel.ItemLabel(table, text=prod_list[row], item_name=prod_list[row], font=('Arial', 12))
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        items_list.append(lbl)
        tk.Label(table, text='кол-во', font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)
        #spin = tk.Spinbox(table, from_=0, to=100, width=5, font=('Arial', 12))
        spin = MySpinBox.MySpinbox(table, from_=0, to=100, width=5, font=('Arial', 12), item_id=row+row_counter, item_type_id=item_type)
        spin.config(command=lambda spn=spin: add_to_basket(spn))
        spin.grid(row=row, column=2, padx=10, pady=5)
        spinboxs_list.append(spin)
        #spin.bind("<<>>")
        btn = button.Mybutton(table, drink_id=row+row_counter, text='❌', fg='RED', font=('Aril', 11))
        btn.config(command=lambda button=btn: clear_basket(button))
        buttons_list.append(btn)
        btn.grid(row=row, column=3, padx=10, pady=5)

def get_type_numbers():
    sql = """SELECT * FROM item_types"""
    cursor.execute(sql)
    db_connection.commit()
    array = cursor.fetchall()
    numbers = []
    for arr in array:
        print(arr)
        numbers.append(arr)
    return numbers


def make_main_window(table_control, item_list, spinbox_list, button_list):  # , row_counter
    numbers = get_type_numbers()
    tables = []
    rows = 0
    for i in range(len(numbers)):
        table = ttk.Frame(tab_control)
        table_control.add(table, text=numbers[i][1])
        tables.append(table)
        prod_list = get_items(int(numbers[i][0]))  # gets items for the coffee table
        prod_win_construct(table, prod_list, item_list, spinbox_list, button_list, rows,
                           item_type=1)  # fills in
        rows += len(prod_list)
    return tables


try:
    db_connection = db.connect('coffee.db')
    cursor = db_connection.cursor()

    customer = customer.Customer()

    win = create_window()
    win.protocol('WM_DELETE_WINDOW', on_closing)
    rnb_image = tk.PhotoImage(file='rnb.png')
    rnb_image = rnb_image.subsample(5, 5)
    row_counter = 0

    button_list = []
    spinbox_list = []
    item_list = []
    basket_list = []
    calories_list = []

    tab_control = ttk.Notebook(win)
    coffee_table = ttk.Frame(tab_control)
    raf_table = ttk.Frame(tab_control)
    tea_table = ttk.Frame(tab_control)
    milk_shake_table = ttk.Frame(tab_control)
    tab_control.add(coffee_table, text='Кофе')
    tab_control.add(raf_table, text='Авторский кофе')
    tab_control.add(tea_table, text='Чай')
    tab_control.add(milk_shake_table, text='Милк Шейки')
    basket_table = ttk.Frame(tab_control)
    tab_control.add(basket_table, text='КОРЗИНА')
    # cabin = ttk.Frame(tab_control)
    # tab_control.add(cabin, text='АККАУНТ ⎆')

    #get_type_numbers()
    #table_list = make_main_window(tab_control, item_list, spinbox_list, button_list)

    product_list = get_items(1)  # gets items for the coffee table
    prod_win_construct(coffee_table, product_list, item_list, spinbox_list, button_list, row_counter, item_type=1)  # fills in
    row_counter += len(product_list)  # increase the item counter for a button list
    product_list.clear()

    product_list = get_items(2)
    prod_win_construct(raf_table, product_list, item_list, spinbox_list, button_list, row_counter, item_type=2)
    row_counter += len(product_list)
    product_list.clear()

    product_list = get_items(3)
    prod_win_construct(milk_shake_table, product_list, item_list, spinbox_list, button_list, row_counter, item_type=3)
    row_counter += len(product_list)
    product_list.clear()

    product_list = get_items(4)
    prod_win_construct(tea_table, product_list, item_list, spinbox_list, button_list, row_counter, item_type=4)
    row_counter += len(product_list)
    product_list.clear()

    for row in range(len(basket_list)):
        tk.Label(basket_table, text=basket_list[row][0], font=('Arial', 12)).grid(row=row, column=0, padx=10, pady=5)
        tk.Label(basket_table, text=basket_list[row][1], font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)

    admin_table = admin.Admin(win, tab_control, db_connection)
    customer_table = customercabinet.CustomerCabinet(win, tab_control, db_connection, customer)

    tab_control.pack(expand=1, fill='both')

    win.mainloop()

except db.Error as error:
    print('Connection error occurred')
finally:
    if db_connection:
        db_connection.close()
        print('Connection with SQL is closed')
