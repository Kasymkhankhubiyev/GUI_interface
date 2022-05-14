import tkinter as tk
from tkinter import messagebox
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
        tk.Button(self.admin_table, command=self.enter_program, text='Enter', font=('Arial', 14)).place(x=350, y=250)  #

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
        print(passwd)

        if value2 != passwd:
            self.outprint.delete(0, tk.END)
            print('Incorrect password')
            self.outprint.insert(0, "Incorrect password or login")
            self.login.delete(0, tk.END)
            self.passwort.delete(0, tk.END)
        else:
            print("Success!")
            list = self.window.place_slaves()
            for i in list:
                i.destroy()

        self.window.update()
        cursor.close()
