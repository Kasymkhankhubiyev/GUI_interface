import random
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import ttk
import sqlite3 as db
from tkinter import messagebox

class Customer:
    def __init__(self, login, uid=None):
        #  надо реализовать рандомное создание ip
        if uid is None:
            self.uid = str(round(random.random() * 255)) + '.' + str(round(random.random() * 255)) + '.' + \
                     str(round(random.random() * 255)) + '.' + str(round(random.random() * 255))
        else:
            self.uid = uid
        self.user_login = login

    def return_uid(self):
        return self.uid

    def return_login(self):
        return self.user_login


class CustomerCabinet:
    def __init__(self, win, ttk_notebook, dbase):
        self.window = win
        self.notebook = ttk_notebook
        self.dbase = dbase
        self.cabin = ttk.Frame(ttk_notebook)
        self.notebook.add(self.cabin, text='АККАУНТ ⎆')

        tk.Label(self.cabin, text='login', font=('Arial', 14)).place(x=200, y=150)
        tk.Label(self.cabin, text='password', font=('Arial', 14)).place(x=200, y=190)
        self.login = tk.Entry(self.cabin, font=('Arial', 14))
        self.login.place(x=300, y=150)
        self.passwort = tk.Entry(self.cabin, show='*', font=('Arial', 14))
        self.passwort.place(x=300, y=190)
        self.outprint = tk.Entry(self.cabin, font=('Arial', 12))
        self.outprint.place(x=250, y=300, width=300)
        tk.Button(self.cabin, text='Войти', font=('Arial', 14)).place(x=300, y=250)
        tk.Button(self.cabin, text='Регистрация', font=('Arial', 14)).place(x=400, y=250)
