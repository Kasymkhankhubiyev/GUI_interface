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

        self.button_list = []
        self.label_list = []
        self.row_counter = 0

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
        self.admin_intro()
        # self.change_price_module()
        # self.add_item_module()
        # self.delete_item_module()
        # self.update_recipe_module()
        # self.add_recipe_module()

    def admin_intro(self, default='Не выбрано'):
        slaves = self.admin_table.grid_slaves()
        for s in slaves:
            s.destroy()
        self.row_counter = 0
        tk.Label(self.admin_table, text='Выберите операцию:  ', font=('Arial', 14)).grid(row=self.row_counter, column=0, padx=10, pady=5)
        values = ['Изменить цену товара', 'Добавить товар', 'Удалить товар', 'Изменить/удалить рецепт', 'Добавить рецепт']
        self.admin_combobox = ttk.Combobox(self.admin_table, values=values, font=('Arial', 12), state='readonly', width=25)
        self.admin_combobox.grid(row=self.row_counter, column=1, padx=5, pady=5)
        self.admin_combobox.set(default)
        self.admin_combobox.bind("<<ComboboxSelected>>", self.choose_admin_module)
        self.window.update()
        self.row_counter += 1

    def choose_admin_module(self, event):
        default = self.admin_combobox.get()
        if self.admin_combobox.get() == 'Изменить цену товара':
            self.admin_intro(default)
            self.change_price_module()
        if self.admin_combobox.get() == 'Добавить товар':
            self.admin_intro(default)
            self.add_item_module()
        if self.admin_combobox.get() == 'Удалить товар':
            self.admin_intro(default)
            self.delete_item_module()
        if self.admin_combobox.get() == 'Изменить/удалить рецепт':
            self.admin_intro(default)
            self.update_recipe_module()
        if self.admin_combobox.get() == 'Добавить рецепт':
            self.admin_intro(default)
            self.add_recipe_module()

    def change_price_module(self):
        tk.Label(self.admin_table, text='Изменить цену товара', font=('Arial', 12)).grid(row=self.row_counter, column=1, pady=5)
        item_list = self.get_items_name()
        self.change_price_combobox = ttk.Combobox(self.admin_table, values=item_list, font=('Arial', 12), state='readonly')
        self.change_price_combobox.grid(row=self.row_counter+1, column=0, pady=5)
        self.change_price_combobox.bind("<<ComboboxSelected>>", self.get_item_price)
        self.change_price_txt = tk.StringVar(value='')
        self.change_price_Lable = tk.Label(self.admin_table, width=10, textvariable=self.change_price_txt, font=('Arial', 12), relief='sunken').grid(row=self.row_counter+1, column=1, pady=5)
        self.change_price_entry = tk.Entry(self.admin_table, font=('Arial', 12), width=10)
        self.change_price_entry.grid(row=self.row_counter+1, column=2, pady=5)
        tk.Button(self.admin_table, command=self.update_product_cost, text='сохранить', font=('Arial', 12)).grid(row=self.row_counter+1, column=3, pady=5)
        self.row_counter += 2

    def add_item_module(self):
        tk.Label(self.admin_table, text='Добавить товар', font=('Arial', 12)).grid(row=self.row_counter, column=1, pady=10)
        tk.Label(self.admin_table, text='Наименование', font=('Arial', 12)).grid(row=self.row_counter+1, column=0, pady=5)
        self.add_item_name = tk.Entry(self.admin_table, font=('Arial', 12), width=25)
        self.add_item_name.grid(row=self.row_counter+2, column=0, pady=5, padx=5, sticky='w')
        tk.Label(self.admin_table, text='Объем\масса', font=('Arial', 12)).grid(row=self.row_counter+1, column=1, padx=10, pady=5)
        self.add_item_amount = tk.Entry(self.admin_table, width=10, font=('Arial', 12))
        self.add_item_amount.grid(row=self.row_counter+2, column=1, pady=5)
        tk.Label(self.admin_table, text='Тип товара', font=('Arial', 12)).grid(row=self.row_counter+1, column=2, pady=5)
        self.add_item_type = ttk.Combobox(self.admin_table, values=['кофе', 'чай', 'авторский', 'коктейл', 'выпечка'], font=('Arial', 12), width=10, state='readonly')
        self.add_item_type.grid(row=self.row_counter+2, column=2, pady=5)
        tk.Label(self.admin_table, text='Цена', font=('Arial', 12)).grid(row=self.row_counter+1, column=3, pady=5)
        self.add_item_cost = tk.Entry(self.admin_table, width=10, font=('Arial', 12))
        self.add_item_cost.grid(row=self.row_counter+2, column=3, pady=5, padx=10)
        tk.Button(self.admin_table, command=self.add_new_product, text='сохранить', font=('Arial', 12)).grid(row=self.row_counter+2, column=4, pady=5, padx=10)
        self.row_counter+=3

    def delete_item_module(self):
        tk.Label(self.admin_table, text='Удалить товар', font=('Arial', 12)).grid(row=self.row_counter, column=1, padx=10, pady=5)
        values = self.get_items_name()
        self.delete_item_name = ttk.Combobox(self.admin_table, values=values, width=30, state='readonly')
        self.delete_item_name.grid(row=self.row_counter+1, column=0, padx=5, pady=5)
        tk.Button(self.admin_table, command=self.delete_product, text='удалить', font=('Arial, 12')).grid(row=self.row_counter+1, column=2, pady=5, padx=10)
        self.row_counter += 2

    def add_recipe_module(self):
        self.add_recipe_row_counter = 1
        self.add_recipe_product_list = []
        self.add_recipe_amount_list = []
        tk.Label(self.admin_table, text='Добавить рецепт', font=('Arial', 12)).grid(row=self.row_counter, column=1, padx=10, pady=5)
        tk.Label(self.admin_table, text='Наименование товара', font=('Arial', 12)).grid(row=self.row_counter+1, column=0, padx=10, pady=5)
        values = self.get_items_name()
        self.add_recipe_item = ttk.Combobox(self.admin_table, values=values, width=25, font=('Arial', 12), state='readonly')
        self.add_recipe_item.grid(row=self.row_counter+1, column=1, padx=5, pady=5)
        tk.Button(self.admin_table, text='Добавить строку', font=('Arial', 12), command=self.create_recipe_line).grid(row=self.row_counter+1, column=2, pady=5, padx=5)
        tk.Label(self.admin_table, text='Продукт', font=('Arial', 12)).grid(row=self.row_counter+2, column=0, padx=10, pady=5)
        tk.Label(self.admin_table, text='Объем/масса', font=('Arial', 12)).grid(row=self.row_counter+2, column=1, padx=5, pady=5)
        self.row_counter += 3
        self.create_recipe_line()
        pass

    def get_products_name(self):
        sql = """SELECT food_name FROM foods_cpfc"""
        cursor = self.data_base.cursor()
        cursor.execute(sql)
        self.data_base.commit()
        array = cursor.fetchall()
        lists = []
        cursor.close()
        for arr in array:
            lists.append(arr[0])
        return lists


    def create_recipe_line(self):
        if self.add_recipe_row_counter < 15:
            self.add_recipe_row_counter += 1  # отслеживаем максимальное кол-во строк за один раз
            values = self.get_products_name()
            combox = ttk.Combobox(self.admin_table, values=values, font=('Arial', 12), state='readonly', width=25)
            combox.grid(row=self.row_counter, column=0, padx=10, pady=5)
            self.add_recipe_product_list.append(combox)
            amountentry = tk.Entry(self.admin_table, width=10, font=('Arial', 12))
            amountentry.grid(row=self.row_counter, column=1, padx=5, pady=5)
            self.add_recipe_amount_list.append(amountentry)
            self.row_counter += 1
            self.window.update()
        else:
            messagebox.showerror(title='Упс... Ошибочка', message=f'Вы достигли максимума возмоных строк {self.add_recipe_row_counter}')

    def update_recipe_module(self):
        tk.Label(self.admin_table, text='Обновить рецептуру', font=('Arial', 12)).grid(row=self.row_counter, column=1, padx=10, pady=5)
        tk.Label(self.admin_table, text='Наименование товара', font=('Arial', 12)).grid(row=self.row_counter+1, column=0, padx=10, pady=5)
        self.update_recipe_item = ttk.Combobox(self.admin_table, values=self.get_items_name(), font=('Arial', 12), state='readonly')
        self.update_recipe_item.grid(row=self.row_counter+2, column=0, padx=10, pady=5)
        self.update_recipe_item.bind("<<ComboboxSelected>>", self.get_recipe_list)
        self.update_recipe_row = self.row_counter+2
        self.update_recipe_items = []
        tk.Label(self.admin_table, text='Компонент', font=('Arial', 12)).grid(row=self.row_counter+1, column=1, padx=5, pady=5)
        tk.Label(self.admin_table, text='Объем/Масса', font=('Arial', 12)).grid(row=self.row_counter+1, column=2, padx=5, pady=5)
        tk.Label(self.admin_table, text='Действие', font=('Arial', 12)).grid(row=self.row_counter+1, column=3, padx=5, pady=5)
        self.update_recipe_command = ttk.Combobox(self.admin_table, values=['Обновить', 'Удалить'], width=10, font=('Arial', 12), state='readonly')
        self.update_recipe_command.grid(row=self.row_counter+2, column=3, pady=5, padx=5)
        tk.Button(self.admin_table, text='Выполнить', font=('Arial', 12), command=self.update_recipe_execute).grid(row=self.row_counter+2, column=4, padx=5, pady=5)
        self.row_counter += 3

    pass

    def get_recipe_list(self, event):
        if self.update_recipe_item.get() != '':
            sql = """SELECT id FROM items WHERE item_name = ?"""
            cursor = self.data_base.cursor()
            cursor.execute(sql, [self.update_recipe_item.get()])
            self.data_base.commit()
            item_name = cursor.fetchall()
            self.item_id = item_name[0][0]

            sql = 'SELECT food_name FROM recipe WHERE product_id = ?'
            cursor.execute(sql, [item_name[0][0]])
            self.data_base.commit()
            array = cursor.fetchall()
            cursor.close()
            for arr in array:
                self.update_recipe_items.append(arr[0])
            self.update_recipe_item_box = ttk.Combobox(self.admin_table, values=self.update_recipe_items, font=('Arial', 12), state='readonly', width=15)
            self.update_recipe_item_box.grid(row=self.update_recipe_row, column=1, padx=5, pady=5)
            self.update_recipe_item_box.bind("<<ComboboxSelected>>", self.set_update_recipe_amount)
            self.update_recipe_amount = tk.Entry(self.admin_table, width=10, font=('Arial', 12))
            self.update_recipe_amount.grid(row=self.update_recipe_row, column=2, padx=5, pady=5)
            self.window.update()
        else:
            pass

    def set_update_recipe_amount(self, event):
        if self.update_recipe_item_box.get() != '':
            sql = """SELECT mass_gr FROM recipe WHERE food_name = ?"""
            cursor = self.data_base.cursor()
            cursor.execute(sql, [self.update_recipe_item_box.get()])
            self.data_base.commit()
            amount = cursor.fetchall()
            cursor.close()
            self.update_recipe_amount.delete(0, 'end')
            self.update_recipe_amount.insert(0, amount[0])
            self.window.update()
        else:
            pass

    def update_recipe_execute(self):
        if self.update_recipe_item.get() != '':
            if self.update_recipe_item_box.get() != '':
                if self.update_recipe_amount.get() != '':
                    if self.update_recipe_amount.get().isdigit() or check_float(self.update_recipe_amount.get()):
                        if self.update_recipe_command.get != '':
                            if self.update_recipe_command.get() == 'Обновить':
                                self.update_recipe()
                            else:
                                if messagebox.askyesno(title='Удаление из рецепта', message='Вы уверены, что хотите удалить компонент из рецепта?'):
                                    self.delete_recipe()
                                else:
                                    pass
                        else:
                            messagebox.showerror(title='Упс... Ошибка', message='Выберите действие!')
                    else:
                        messagebox.showerror(title='Упс... Ошибка', message='Масса или объем должно быть числовым значением. Например: 170 или 170,5 или 170.5')
                else:
                    messagebox.showerror(title='Упс... Ошибка', message='Строка кол-ва пустая. Введите массу в гр или объем в мл. Например, 170.')
            else:
                messagebox.showerror(title='Упс... Ошибка', message='Выберите компонент.')
        else:
            messagebox.showerror(title='Упс... Ошибка', message='Выберите товарную позицию.')

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


    def add_recipe(self):
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
        sql = """UPDATE recipe SET mass_gr = ? WHERE product_id = ? AND food_name = ?"""
        cursor = self.data_base.cursor()
        amount = convert_to_float(self.update_recipe_amount.get())
        cursor.execute(sql, [amount, self.item_id, self.update_recipe_item_box.get()])
        self.data_base.commit()
        cursor.close()
        self.window.update()

    def delete_recipe(self):
        sql = """DELETE FROM recipe WHERE product_id = ? AND food_name = ?"""
        cursor = self.data_base.cursor()
        cursor.execute(sql, [self.item_id, self.update_recipe_item_box.get()])
        self.data_base.commit()
        cursor.close()
        self.window.update()

    def update_product_cost(self):
        item = self.change_price_combobox.get()
        if item != '':
            if item.isdigit():
                sql = ("""UPDATE items SET cost = ? WHERE item_name = ?""")
                cursor = self.data_base.cursor()
                cursor.execute(sql, [self.change_price_entry.get(), self.change_price_combobox.get()])
                self.data_base.commit()
                cursor.close()
                self.get_item_price()
                self.window.update()
            else:
                messagebox.showerror(title='Упс... Ошибка', message='Цена должна иметь целочисленное значение. Например: 270')
        else:
            messagebox.showerror(title='Упс... Ошибка', message='Пожалуйста, выберите товар')


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


def check_float(str):
    if str.replace('.', '', 1).isdigit():
        return True
    elif str.replace(',', '', 1).isdigit():
        return True
    else:
        return False


def convert_to_float(str):
    check = str
    if check.replace('.', '', 1).isdigit():
        return float(str)
    elif check.replace(',', '', 1).isdigit():
        return float(str.replace(',', '.', 1))


def item_type_case(str):
    if str == 'кофе':
        return 1
    elif str == 'авторский':
        return 2
    elif str == 'коктейл':
        return 3
    elif str == 'чай':
        return 4