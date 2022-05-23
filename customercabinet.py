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
        tk.Label(self.cabin, text='EMAIL', font=('Arial', 12)).place(x=130, y=220)
        self.reg_email = tk.Entry(self.cabin, font=('Arial', 14), width=25)
        self.reg_email.place(x=250, y=220)
        tk.Button(self.cabin, text='Подтвердить', font=('Arial', 14), command=self.add_customer).place(x=190, y=260)

    def create_account(self):
        slaves = self.cabin.place_slaves()
        for slave in slaves:
            slave.destroy()
        self.draw_registration_window()

    def email_check(self, email):
        sql = """SELECT user_email FROM customers WHERE user_login = ?"""
        cursor = self.dbase.cursor()
        cursor.execute(sql, [email])
        self.dbase.commit()
        exists = cursor.fetchall()
        cursor.close()
        if len(exists) != 0:
            return True
        else:
            return False

    def insert_customer(self, login, pwd, email):
        try:
            uid = str(round(random.random() * 255)) + '.' + str(round(random.random() * 255)) + '.' + \
                     str(round(random.random() * 255)) + '.' + str(round(random.random() * 255))
            cursor = self.dbase.cursor()
            sql = """INSERT INTO customers(user_id, user_login, user_pwd, user_email)
                    VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, [uid, login.lower(), pwd, email])  # email не зависит от регистра
            self.dbase.commit()
        except self.dbase.Error as error:
            messagebox.showerror(title='Error', message='Data Base error occurred. Try again, please.')
            return False
        finally:
            cursor.close()
            return True

    def add_customer(self):
        if self.reg_login.get() != '':
            if self.reg_pwd.get() != '':
                if self.reg_rep_pwd.get() != '':
                    if self.reg_pwd.get() == self.reg_rep_pwd.get():
                        if self.reg_email.get() != '':
                            if self.email_check(self.reg_email.get()):
                                if self.get_login_pwd(self.reg_login.get()) == 0:
                                    if self.insert_customer(self.reg_login.get(), self.reg_pwd.get(), self.reg_email.get()):
                                        pass
                                    else:
                                        messagebox.showerror(title='ERROR', message='Упс... Ошибочка вышла. Пожалуйста, повторите еще раз')
                                else:
                                    messagebox.showerror(title='Error', message=f'Логин "{self.reg_login.get()}" занят'+'\n'+'Придумайте, пожалуйста, другой логин.')
                                    self.reg_login.delete(0, tk.END)
                                    self.reg_pwd.delete(0, tk.END)
                                    self.reg_rep_pwd.delete(0, tk.END)
                            else:
                                messagebox.showerror(title='Error', message=f'Этот email: {self.reg_email.get()} уже используется!')
                        else:
                            messagebox.showerror(title='Error', message='Введите почту')
                    else:
                        messagebox.showerror(title='Error', message='Пароли не совпадают!')
                        self.reg_pwd.delete(0, tk.END)
                        self.reg_rep_pwd.delete(0, tk.END)
                else:
                    messagebox.showerror(title='Error', message='Повторите пароль!')
                    self.reg_pwd.delete(0, tk.END)
            else:
                messagebox.showerror(title='Error', message='Придумайте пароль!')
        else:
            # text = self.reg_login.get()
            # self.reg_login = tk.Entry(self.cabin, font=('Arial', 14), background='RED', width=25)
            # self.reg_login.insert(0, text)
            # self.reg_login.place(x=250, y=100)
            messagebox.showerror(title='Error', message='Поле "Логин" пустое.')