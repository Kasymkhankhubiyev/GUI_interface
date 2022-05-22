import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import ttk
import sqlite3 as db
from tkinter import messagebox


class CustomerCabinet:
    def __init__(self, win, ttk_notebook, dbase, customer):

        self.customer = customer

        self.window = win
        self.notebook = ttk_notebook
        self.dbase = dbase
        self.cabin = ttk.Frame(ttk_notebook)
        self.notebook.add(self.cabin, text='АККАУНТ ⎆')

        tk.Label(self.cabin, text='login', font=('Arial', 14)).place(x=200, y=150)
        tk.Label(self.cabin, text='password', font=('Arial', 14)).place(x=200, y=190)
        self.login = tk.Entry(self.cabin, font=('Arial', 14))
        self.login.place(x=300, y=150)
        self.password = tk.Entry(self.cabin, show='*', font=('Arial', 14))
        self.password.place(x=300, y=190)
        self.outprint = tk.Entry(self.cabin, font=('Arial', 12))
        self.outprint.place(x=250, y=300, width=300)
        tk.Button(self.cabin, command=self.enter_account, text='Войти ⎆', font=('Arial', 14)).place(x=300, y=250)
        tk.Button(self.cabin, command=self.create_account, text='Регистрация', font=('Arial', 14)).place(x=400, y=250)

    def enter_account(self):
        login = self.login.get()
        pwd = self.password.get()
        log_pwd = self.get_login_pwd(login)

    def get_login_pwd(self, login):
        return 0

    def create_account(self):
        pass