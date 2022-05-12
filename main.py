import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3 as db


# sql_query = '''INSERT INTO login_passwd(login, passwd)
#                 VALUES
#                     ('k.khubiev','12345'),
#                     ('m.solomin', '12345');'''
# cursor = db_connection.cursor()
# cursor.execute(sql_query)
# db_connection.commit()

# with open('select_all.sql', 'r') as sql_file:
#     sql_script = sql_file.read()
#
# sql = '''SELECT * FROM login_passwd'''
# cursor = db_connection.cursor()
# cursor.execute(sql)
# print(cursor.fetchall())

# for row in cursor.execute(sql):
#     print(row)
# cursor.close()

# def enter_program():
#     value1 = login.get()
#     value2 = passwort.get()
#
#     print(value1)
#
#     db_connection = db.connect('project.db')
#
#     sql = '''SELECT passwd FROM login_passwd
#           WHERE login = ?'''
#     cursor = db_connection.cursor()
#     cursor.execute(sql, [value1])
#     passwd = cursor.fetchall()
#     print(passwd)
#
#     if value2 != passwd:
#         outprint.delete(0, tk.END)
#         outprint.insert(0, "Incorrect password or login")
#         login.delete(0, tk.END)
#         passwort.delete(0, tk.END)
#     else:
#         print("Success!")
#         list = win.place_slaves()
#         for i in list:
#             i.destroy()
#         tk.Label(win, image=rnb_image).grid(row=0, column=0, stick='w')
#         win.update()
#     cursor.close()
#     db_connection.close()
#
# def move_to_admin_window():
#     list = win.place_slaves()
#     for i in list:
#         i.destroy()
#
#     tk.Label(win, text='login', font=('Arial', 14)).place(x=200, y=150)
#     tk.Label(win, text='password', font=('Arial', 14)).place(x=200, y=190)
#
#     login = tk.Entry(win, font=('Arial', 14))
#     # login.grid(row=0, column=1, padx=100)
#     login.place(x=300, y=150)
#     passwort = tk.Entry(win, show='*', font=('Arial', 14))
#     # passwort.grid(row=1, column=1)
#     passwort.place(x=300, y=190)
#     outprint = tk.Entry(win, font=('Arial', 12))
#     outprint.place(x=250, y=300, width=300)
#     tk.Button(win, text='Enter', command=enter_program, font=('Arial', 14)).place(x=350, y=250)
#
#     win.update()

def get_items(item_id):
    labls = []
    sql = """SELECT item_name FROM items WHERE type_id = ?"""
    cursor.execute(sql, [item_id])
    db_connection.commit()
    lists = cursor.fetchall()
    for item in lists:
        labls.append(item[0])
        print(item)
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


def add_to_basket(button):
    item_id = button.get_button_id()
    value = spinbox_list[item_id].get()
    item_name = item_list[item_id].get_item_name()
    sql = """SELECT cost FROM items WHERE item_name = ?"""
    cursor.execute(sql, [item_name])
    cost = cursor.fetchall()
    items = [item_name, str(value), int(cost[0][0]) * int(value)]
    names = []
    if value != '0':
        if len(basket_list) != 0:
            for i in range(len(basket_list)):
                i_name = basket_list[i][0]
                names.append(i_name)
            if item_name in names:
                k = names.index(item_name)
                basket_list[k][1] = value
                basket_list[k][2] *= int(value)
            else:
                basket_list.append(items)
        else:
            basket_list.append(items)
    fill_basket()
    win.update()
#возможно нужно добавить, что если value = 0 нужно удалить из списка


class Item_label(tk.Label):
    def __init__(self, master, item_name, *args, **kwargs):
        super(Item_label, self).__init__(master, *args, **kwargs)
        self.item_name = item_name

    def get_item_name(self):
        return self.item_name


class Mybutton(tk.Button):
    def __init__(self, master, drink_id, *args, **kwargs):
        super(Mybutton, self).__init__(master, *args, **kwargs)
        self.drink_id = drink_id

    def get_button_id(self):
        return self.drink_id

def sum_calories():
    return 0


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


    tk.Button(basket_table, text='Рассчитать КБЖУ и Стоимость', command=calculate_calories, font=('Arial', 12)).grid(
        row=1, column=0, padx=10, pady=5)

    columns = (1, 2)
    caltree = ttk.Treeview(basket_table, show="headings", column=columns, height=7)
    tree.column('#0', minwidth=20, width=100, stretch=False)
    caltree.heading(1, text='Наименование')
    caltree.heading(2, text='калории - белки - жиры - углеводы')
    tree.column(2, minwidth=10, width=100, stretch=False)
    print('column 2 is done')
    scrollbar = tk.Scrollbar(basket_table, orient=tk.VERTICAL, command=tree.yview)
    caltree.configure(yscroll=scrollbar.set)

    for i in range(len(basket_list)):
        arr = [basket_list[i][0], str(calories_list[i][0])+' - '+str(calories_list[i][1])+' - '+str(calories_list[i][2])+' - '+str(calories_list[i][3])]
        caltree.insert("", tk.END, values=arr)
    caltree.grid(row=2, column=0, sticky=tk.W+tk.E)
    scrollbar.grid(row=2, column=1, sticky=tk.N + tk.S)
    tk.Button(basket_table, text='ИТОГО', font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=5)
    win.update()

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
    tk.Button(basket_table, text='Рассчитать КБЖУ и Стоимость', command=calculate_calories, font=('Arial', 12)).grid(row=len(basket_list) + 1,
                                                                                         column=0, padx=10, pady=5)

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


try:
    db_connection = db.connect('coffee.db')
    cursor = db_connection.cursor()

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
    basket_table = ttk.Frame(tab_control)
    raf_table = ttk.Frame(tab_control)
    tea_table = ttk.Frame(tab_control)
    milk_shake_table = ttk.Frame(tab_control)
    tab_control.add(coffee_table, text='Кофе')
    tab_control.add(raf_table, text='Авторский кофе')
    tab_control.add(tea_table, text='Чай')
    tab_control.add(milk_shake_table, text='Милк Шейки')
    tab_control.add(basket_table, text='КОРЗИНА')

    product_list = get_items(1)

    for row in range(len(product_list)):
            # item_list = get_items(1)
        lbl = Item_label(coffee_table, text=product_list[row], item_name=product_list[row], font=('Arial', 12))
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        item_list.append(lbl)
        tk.Label(coffee_table, text='кол-во', font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)
        spin = tk.Spinbox(coffee_table, from_=0, to=100, width=5, font=('Arial', 12))
        spin.grid(row=row, column=2, padx=10, pady=5)
        spinbox_list.append(spin)
        btn = Mybutton(coffee_table, drink_id=row, text='🛒', fg='GREEN', font=('Aril', 11))
        btn.config(command=lambda button=btn: add_to_basket(button))
        button_list.append(btn)
        btn.grid(row=row, column=3, padx=10, pady=5)

    row_counter = len(product_list)
    product_list.clear()
    product_list = get_items(2)

    for row in range(len(product_list)):
            # item_list = get_items(1)
        lbl = Item_label(raf_table, text=product_list[row], item_name=product_list[row], font=('Arial', 12))
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        item_list.append(lbl)
        tk.Label(raf_table, text='кол-во', font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)
        spin = tk.Spinbox(raf_table, from_=0, to=100, width=5, font=('Arial', 12))
        spin.grid(row=row, column=2, padx=10, pady=5)
        spinbox_list.append(spin)
        btn = Mybutton(raf_table, drink_id=row + row_counter, text='🛒', fg='GREEN', font=('Aril', 11))
        btn.config(command=lambda button=btn: add_to_basket(button))
        button_list.append(btn)
        btn.grid(row=row, column=3, padx=10, pady=5)

    row_counter += len(product_list)
    product_list.clear()
    product_list = get_items(3)

    for row in range(len(product_list)):
        # item_list = get_items(1)
        lbl = Item_label(milk_shake_table, text=product_list[row], item_name=product_list[row], font=('Arial', 12))
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        item_list.append(lbl)
        tk.Label(milk_shake_table, text='кол-во', font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)
        spin = tk.Spinbox(milk_shake_table, from_=0, to=100, width=5, font=('Arial', 12))
        spin.grid(row=row, column=2, padx=10, pady=5)
        spinbox_list.append(spin)
        btn = Mybutton(milk_shake_table, drink_id=row + row_counter, text='🛒', fg='GREEN', font=('Aril', 11))
        btn.config(command=lambda button=btn: add_to_basket(button))
        button_list.append(btn)
        btn.grid(row=row, column=3, padx=10, pady=5)

    row_counter += len(product_list)
    product_list.clear()
    product_list = get_items(4)

    for row in range(len(product_list)):
        # item_list = get_items(1)
        lbl = Item_label(tea_table, text=product_list[row], item_name=product_list[row], font=('Arial', 12))
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        item_list.append(lbl)
        tk.Label(tea_table, text='кол-во', font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)
        spin = tk.Spinbox(tea_table, from_=0, to=100, width=5, font=('Arial', 12))
        spin.grid(row=row, column=2, padx=10, pady=5)
        spinbox_list.append(spin)
        btn = Mybutton(tea_table, drink_id=row + row_counter, text='🛒', fg='GREEN', font=('Aril', 11))
        btn.config(command=lambda button=btn: add_to_basket(button))
        button_list.append(btn)
        btn.grid(row=row, column=3, padx=10, pady=5)


    for row in range(len(basket_list)):
        tk.Label(basket_table, text=basket_list[row][0], font=('Arial', 12)).grid(row=row, column=0, padx=10, pady=5)
        tk.Label(basket_table, text=basket_list[row][1], font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)

    tab_control.pack(expand=1, fill='both')
    # tk.Button(win, text='admin', command=move_to_admin_window).place(x=200, y=300)

    win.mainloop()

except db.Error as error:
    print('Connection error occurred')
finally:
    if db_connection:
        db_connection.close()
        print('Connection with SQL is closed')


# def new_window():
#     tk.Label(win1, image=rnb_image).grid(row=0, column=0, stick='w')
#     win1.update()
#
#
# win1 = create_window()
# rnb_image = tk.PhotoImage(file='rnb.png')
# rnb_image = rnb_image.subsample(5, 5)
#
# tk.Button(win1, text='new window', command=new_window).grid(row=0, column=0, stick='w')
# win1.update()
#
# win1.mainloop()


