import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import ttk
import sqlite3 as db


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
        tk.Label(self.admin_table, text='Изменить цену товара', font=('Arial', 12)).grid(row=0, column=1, padx=10, pady=5)
        item_list = self.get_items_name()
        self.change_price_combobox = ttk.Combobox(self.admin_table, values=item_list, font=('Arial', 12), state='readonly')
        self.change_price_combobox.grid(row=1, column=0,padx=10, pady=5)
        self.change_price_combobox.bind("<<ComboboxSelected>>", self.get_item_price)
        self.change_price_txt = tk.StringVar(value='')
        self.change_price_Lable = tk.Label(self.admin_table, width=10, textvariable=self.change_price_txt, font=('Arial', 12), relief='sunken').grid(row = 1, column=1)


    def bind_test(self, event, val):
        print()

    def get_item_price(self, event):
        sql = ("""SELECT cost FROM items where item_name = ?""")
        item_list = []
        cursor = self.data_base.cursor()
        print(self.change_price_combobox.get())
        cursor.execute(sql, [self.change_price_combobox.get()])
        self.data_base.commit()
        price = cursor.fetchall()
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
        pass

    def add_recepe(self):
        pass

    def delete_product(self):
        pass

    def update_recipe(self):
        pass

    def update_product_cost(self):
        pass