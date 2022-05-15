import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import ttk
import sqlite3 as db
from tkinter import messagebox


class Admin:
    def __init__(self, win, ttk_notebook, dbase):
        self.ttk_notebook = ttk_notebook
        self.admin_table = ttk.Frame(ttk_notebook)
        self.ttk_notebook.add(self.admin_table, text='Admin')
        self.window = win
        self.data_base = dbase
        self.pwd_db = db.connect('project.db')
        tk.Label(self.admin_table, text='login', font=('Arial', 14)).place(x=200, y=150)
        tk.Label(self.admin_table, text='password', font=('Arial', 14)).place(x=200, y=190)

        self.login = tk.Entry(self.admin_table, font=('Arial', 14))
        self.login.place(x=300, y=150)
        self.passwort = tk.Entry(self.admin_table, show='*', font=('Arial', 14))
        self.passwort.place(x=300, y=190)
        self.outprint = tk.Entry(self.admin_table, font=('Arial', 12))
        self.outprint.place(x=250, y=300, width=300)
        tk.Button(self.admin_table, command=self.enter_program, text='Enter', font=('Arial', 14)).place(x=350, y=250)

        self.button_list=[]
        self.label_list=[]

    def enter_program(self):
        value1 = self.login.get()
        value2 = self.passwort.get()

        print(value1)

        sql = '''SELECT passwd FROM login_passwd
              WHERE login = ?'''
        cursor = self.pwd_db.cursor()
        cursor.execute(sql, [value1])
        self.pwd_db.commit()
        passwd = cursor.fetchall()
        # print(passwd[0][0]) # - надо раскоментить потом

        if '' == passwd:  # value2 != passwd[0][0]:  # fetchall returns [(value,)]
            self.outprint.delete(0, tk.END)
            print('Incorrect password')
            self.outprint.insert(0, "Incorrect password or login")
            self.login.delete(0, tk.END)
            self.passwort.delete(0, tk.END)
        else:
            print("Success!")
            list = self.admin_table.place_slaves()
            for i in list:
                i.destroy()
            self.manage_window()
        self.window.update()
        cursor.close()

    def manage_window(self):
        self.change_price_module()
        self.add_item_module()
        self.delete_item_module()

    def change_price_module(self):
        tk.Label(self.admin_table, text='Изменить цену товара', font=('Arial', 12)).grid(row=0, column=1, pady=5)
        item_list = self.get_items_name()
        self.change_price_combobox = ttk.Combobox(self.admin_table, values=item_list, font=('Arial', 12), state='readonly')
        self.change_price_combobox.grid(row=1, column=0, pady=5)
        self.change_price_combobox.bind("<<ComboboxSelected>>", self.get_item_price)
        self.change_price_txt = tk.StringVar(value='')
        self.change_price_Lable = tk.Label(self.admin_table, width=10, textvariable=self.change_price_txt, font=('Arial', 12), relief='sunken').grid(row=1, column=1, pady=5)
        self.change_price_entry = tk.Entry(self.admin_table, font=('Arial', 12), width=10)
        self.change_price_entry.grid(row=1, column=2, pady=5)
        tk.Button(self.admin_table, command=self.update_product_cost, text='сохранить', font=('Arial', 12)).grid(row=1, column=3, pady=5)

    def add_item_module(self):
        tk.Label(self.admin_table, text='Добавить товар', font=('Arial', 12)).grid(row=2, column=1, pady=10)
        tk.Label(self.admin_table, text='Наименование', font=('Arial', 12)).grid(row=3, column=0, pady=5)
        self.add_item_name = tk.Entry(self.admin_table, font=('Arial', 12), width=25)
        self.add_item_name.grid(row=4, column=0, pady=5, padx=5, sticky='w')
        tk.Label(self.admin_table, text='Объем\масса', font=('Arial', 12)).grid(row=3, column=1, padx=10, pady=5)
        self.add_item_amount = tk.Entry(self.admin_table, width=10, font=('Arial',12))
        self.add_item_amount.grid(row=4, column=1, pady=5)
        tk.Label(self.admin_table, text='Тип товара', font=('Arial', 12)).grid(row=3, column=2, pady=5)
        self.add_item_type = ttk.Combobox(self.admin_table, values=['кофе', 'чай', 'авторский', 'коктейл', 'выпечка'], font=('Arial', 12), width=10, state='readonly')
        self.add_item_type.grid(row=4, column=2, pady=5)
        tk.Label(self.admin_table, text='Цена', font=('Arial', 12)).grid(row=3, column=3, pady=5)
        self.add_item_cost = tk.Entry(self.admin_table, width=10, font=('Arial', 12))
        self.add_item_cost.grid(row=4, column=3, pady=5, padx=10)
        tk.Button(self.admin_table, command=self.add_new_product, text='сохранить', font=('Arial', 12)).grid(row=4, column=4, pady=5, padx=10)

    def delete_item_module(self):
        tk.Label(self.admin_table, text='Удалить товар', font=('Arial', 12)).grid(row=5, column=1, padx=10, pady=5)
        values = self.get_items_name()
        self.delete_item_name = ttk.Combobox(self.admin_table, values=values, width=30, state='readonly')
        self.delete_item_name.grid(row=6, column=0, padx=5, pady=5)
        tk.Button(self.admin_table, command=self.delete_product, text='удалить', font=('Arial, 12')).grid(row=6, column=2, pady=5, padx=10)

    def get_item_price(self, event="<Button>"):
        sql = ("""SELECT cost FROM items where item_name = ?""")
        item_list = []
        cursor = self.data_base.cursor()
        cursor.execute(sql, [self.change_price_combobox.get()])
        self.data_base.commit()
        price = cursor.fetchall()
        cursor.close()
        self.change_price_txt.set(price[0][0])
        self.window.update()

    def get_items_name(self):
        sql=("""SELECT item_name FROM items""")
        item_list = []
        cursor = self.data_base.cursor()
        cursor.execute(sql)
        self.data_base.commit()
        lists = cursor.fetchall()
        for item in lists:
            item_list.append(item[0])
        return item_list

    def add_new_product(self):
        if self.add_item_name.get() != '':  # cheking whether name in empty or not
            if check_str(self.add_item_name.get()):
                if self.add_item_amount.get() != '':
                    if self.add_item_amount.get().isdigit():
                        if self.add_item_type.get() != '':
                            if self.add_item_cost.get() != '':
                                if self.add_item_cost.get().isdigit():
                                    sql = ("""INSERT INTO items(item_name, type_id, cost)
                                                Values (?, ?, ?)""")
                                    name = self.add_item_name.get() + ' ' + self.add_item_amount.get()
                                    cursor = self.data_base.cursor()
                                    cursor.execute(sql, [name, item_type_case(self.add_item_type.get()), int(self.add_item_cost.get())])
                                    self.data_base.commit()
                                    cursor.close()
                                    self.window.update()
                                else:
                                    messagebox.showerror(title='Упс... Ошибка',
                                                     message='Цена должна быть целым числом, например 270.')
                            else:
                                messagebox.showerror(title='Упс... Ошибка',
                                                     message='Введите цену товара, хотя бы примерную, позже можно будет изменить. Например: 180')
                        else:
                            messagebox.showerror(title='Упс... Ошибка', message='Выберите тип продукта!')
                    else:
                        messagebox.showerror(title='Упс... Ошибка',
                                             message='масса или объем должны быть целочисленными, Например: 250')
                else:
                    messagebox.showerror(title='Упс... Ошибка',
                                         message='Пустое поле кол-ва: масса в гр, объем в мл., например: 250')
            else:
                messagebox.showerror(title='Упс... Ошибка', message='Название не может быть числом или математическим выражением! Пример: Капучино.')
        else:
            print('Item name is empty')
            messagebox.showerror(title='Упс... Ошибка', message='Пустое поле названия товара!')


    def add_recepe(self):
        pass

    def delete_product(self):
        if messagebox.askyesno(title='Удаление позиции', message='Вы уверены, что хотите удалить этот товар?'):
            sql = ("""DELETE FROM items where item_name = ?""")
            cursor = self.data_base.cursor()
            cursor.execute(sql, [self.delete_item_name.get()])
            self.data_base.commit()
            cursor.close()
            self.window.update()
        else:
            pass

    def update_recipe(self):
        pass

    def update_product_cost(self):
        item = self.change_price_combobox.get()
        if item != '':
            sql = ("""UPDATE items SET cost = ? WHERE item_name = ?""")
            cursor = self.data_base.cursor()
            cursor.execute(sql, [self.change_price_entry.get(), self.change_price_combobox.get()])
            self.data_base.commit()
            cursor.close()
            self.get_item_price()
            self.window.update()
        else: pass


def check_str(str):
    if str.replace('.', '', 1).isdigit():
        return False
    elif str.replace(',', '', 1).isdigit():
        return False
    elif str.replace('/', '', 1).isdigit():
        return False
    elif str.replace('^', '', 1).isdigit():
        return False
    elif str.replace('*', '', 1).isdigit():
        return False
    elif str.replace(':', '', 1).isdigit():
        return False
    else:
        return True

def item_type_case(str):
    if str == 'кофе':
        return 1
    elif str == 'авторский':
        return 2
    elif str == 'коктейл':
        return 3
    elif str == 'чай':
        return 4