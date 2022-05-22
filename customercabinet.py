import tkinter as tk
import random
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
        if log_pwd == 0:
            messagebox.showerror(title="Ups, error...", message='No such login')
        else:
            if log_pwd == pwd:
                pass  # run the cabinet
            else:
                messagebox.showerror(title='Ups, error...', message='Incorrect pwd')

    def get_login_pwd(self, login):
        sql = """SELECT user_pwd FROM customers WHERE user_login = ?"""
        cursor = self.dbase.cursor()
        cursor.execute(sql, [login])
        self.dbase.commit()
        result = cursor.fetchall()
        if len(result) == 0:
            print('Nothing found....')
            return 0
        else:
            return result[0]

    def draw_registration_window(self):
        tk.Label(self.cabin, text='ЛОГИН', font=('Arial', 12)).place(x=130, y=100)
        self.reg_login = tk.Entry(self.cabin, font=('Arial', 14), width=25)
        self.reg_login.place(x=250, y=100)
        tk.Label(self.cabin, text='ПАРОЛЬ', font=('Arial', 12)).place(x=130, y=140)
        self.reg_pwd = tk.Entry(self.cabin, font=('Arial', 14), width=25, show='*')
        self.reg_pwd.place(x=250, y=140)
        tk.Label(self.cabin, text='ПАРОЛЬ', font=('Arial', 12)).place(x=130, y=180)
        self.reg_rep_pwd = tk.Entry(self.cabin, font=('Arial', 14), width=25, show='*')
        self.reg_rep_pwd.place(x=250, y=180)
        tk.Button(self.cabin, text='Подтвердить', font=('Arial', 14), command=self.add_customer).place(x=190, y=220)

    def create_account(self):
        slaves = self.cabin.place_slaves()
        for slave in slaves:
            slave.destroy()
        self.draw_registration_window()


    def add_customer(self):
        if self.reg_login.get() != '':
            pass
        else:
            text = self.reg_login.get()
            self.reg_login = tk.Entry(self.cabin, font=('Arial', 14), background='RED', width=25)
            self.reg_login.insert(0, text)
            self.reg_login.place(x=250, y=100)
            messagebox.showerror(title='Error', message='Поле "Логин" пустое.')
