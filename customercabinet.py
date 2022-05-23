import tkinter as tk
import random
from tkinter.ttk import Combobox
from tkinter import ttk
import sqlite3 as db
from tkinter import messagebox
import customer


class CustomerCabinet:
    def __init__(self, win, ttk_notebook, dbase, customer):

        self.customer = customer
        self.order_list = []
        self.order_buttons = []

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
        # for slave in self.cabin.place_slaves():
        #     slave.destroy()
        # self.cabinet_window()
        if log_pwd == 0:
            messagebox.showerror(title="Ups, error...", message='No such login')
        else:
            if log_pwd == pwd:
                uid = self.get_user_uid(login)
                for slave in self.cabin.place_slaves():
                    slave.destroy()
                self.customer = customer.Customer(login, uid)  # инициализируем пользователя
                self.cabinet_window()
            else:
                messagebox.showerror(title='Ups, error...', message='Incorrect pwd')

    def get_login_pwd(self, login):
        cursor = self.dbase.cursor()
        sql = """SELECT user_pwd FROM customers WHERE user_login = ?"""
        cursor.execute(sql, [login])
        self.dbase.commit()
        result = cursor.fetchall()
        if len(result) == 0:
            print('Nothing found....')
            return 0
        else:
            return result[0][0]

    def cabinet_window(self, default='Не выбрано'):
        for slave in self.cabin.grid_slaves():
            slave.destroy()
        row = 0
        self.order_list.clear()
        self.order_buttons.clear()
        tk.Label(self.cabin, text="Выберите операцию:", font=('Arial', 14)).grid(row=0, column=0, pady=5, padx=10)
        values=['главная страница', 'история заказов', 'аналитика', 'личные данные']
        self.command_combobox=ttk.Combobox(self.cabin, values=values, font=('Arial', 14), state='readonly', width=25)
        self.command_combobox.grid(row=1, column=0, padx=10, pady=5)
        self.command_combobox.set(default)
        self.command_combobox.bind("<<ComboboxSelected>>", self.choose_command)
        tk.Label(self.cabin, text='Текущие заказы:')
        row += 2
        self.order_list = self.get_current_orders(self.customer.return_uid())
        columns = (1, 2, 3)
        tree = ttk.Treeview(self.cabin, show='headings', column=columns, height=7)
        tree.heading(1, text='Заказ №')
        tree.heading(2, text='Дата')
        tree.heading(3, text='Статус')
        ysb = ttk.Scrollbar(self.cabin, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=ysb.set)
        for order in self.order_list:
            tree.insert("", tk.END, values=order)

        tree.grid(row=row, column=0, sticky=tk.W+tk.E)
        ysb.grid(row=row, column=1, sticky=tk.N+tk.S)


    def get_current_orders(self, uid):
        sql = """SELECT id, order_date, order_status FROM order_history WHERE customer_id = ? AND order_status = 'ГОТОВИТСЯ'"""
        cursor = self.dbase.cursor()
        cursor.execute(sql, [uid])
        self.dbase.commit()
        lists = []
        array = cursor.fetchall()
        for arr in array:
            print(arr)
            lists.append(arr)
        return lists

    def choose_command(self, event):
        command = self.command_combobox.get()
        if command == 'главная страница':
            self.cabinet_window(default=command)
        elif command == 'история заказов':
            self.history_window(command)
        elif command == 'аналитика':
            self.analytic_window(command)
        elif command == 'личные данные':
            self.user_data(command)

    def history_window(self, command_name):
        for slave in self.cabin.grid_slaves():
            slave.destroy()
        row = 0
        self.order_list.clear()
        self.order_buttons.clear()
        tk.Label(self.cabin, text="Выберите операцию:", font=('Arial', 14)).grid(row=0, column=0, pady=5, padx=10)
        values=['главная страница', 'история заказов', 'аналитика', 'личные данные']
        self.command_combobox=ttk.Combobox(self.cabin, values=values, font=('Arial', 14), state='readonly', width=25)
        self.command_combobox.grid(row=1, column=0, padx=10, pady=5)
        self.command_combobox.set(command_name)
        self.command_combobox.bind("<<ComboboxSelected>>", self.choose_command)
        tk.Label(self.cabin, text='История заказов:')
        row += 2
        self.order_list = self.get_orders_history(self.customer.return_uid())
        columns = (1, 2, 3, 4)
        tree = ttk.Treeview(self.cabin, show='headings', column=columns, height=7)
        tree.heading(1, text='Заказ №')
        tree.column(1, width=70, stretch=False)
        tree.heading(2, text='Дата')
        tree.column(2, minwidth=100, stretch=False)
        tree.heading(3, text='Статус')
        tree.column(4, width=70, stretch=False)
        tree.heading(4, text='Стоимость')
        tree.column(4, width=70, stretch=False)
        ysb = ttk.Scrollbar(self.cabin, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=ysb.set)
        for order in self.order_list:
            tree.insert("", tk.END, values=order)

        tree.grid(row=row, column=0, sticky=tk.W + tk.E)
        ysb.grid(row=row, column=1, sticky=tk.N + tk.S)

        tk.Label(self.cabin, text='Подребнее').grid(row=row+1,column=0,padx=10, pady=5)

    def get_orders_history(self, uid):
        sql = """SELECT order_history.id, order_history.order_date, order_history.order_status, fee.cost 
                FROM 
                    order_history 
                    INNER JOIN
                    (SELECT id, SUM(item_cost) AS cost FROM orders 
                    WHERE order_id in (SELECT id FROM order_history WHERE customer_id = ?)
                    GROUP BY id)fee
                    ON order_history.id = fee.id
                WHERE customer_id = ? GROUP BY order_history.id"""
        cursor = self.dbase.cursor()
        cursor.execute(sql, [uid, uid])
        self.dbase.commit()
        array = cursor.fetchall()
        result = []
        for arr in array:
            result.append(arr)
        return result

    def analytic_window(self, command):
        for slave in self.cabin.grid_slaves():
            slave.destroy()
        row = 0
        self.order_list.clear()
        self.order_buttons.clear()
        tk.Label(self.cabin, text="Выберите операцию:", font=('Arial', 14)).grid(row=0, column=0, pady=5, padx=10)
        values = ['главная страница', 'история заказов', 'аналитика', 'личные данные']
        self.command_combobox=ttk.Combobox(self.cabin, values=values, font=('Arial', 14), state='readonly', width=25)
        self.command_combobox.grid(row=1, column=0, padx=10, pady=5, columnspan=4)
        self.command_combobox.set(command)
        self.command_combobox.bind("<<ComboboxSelected>>", self.choose_command)
        tk.Label(self.cabin, text='История заказов:')
        row += 2
        self.r_var = tk.IntVar()
        self.r_var.set(0)
        self.week_button = tk.Radiobutton(self.cabin, variable=self.r_var, value=0, text='Неделя', command=self.draw_week_charts)
        self.week_button.grid(row=row, column=0, pady=5, sticky=tk.E)
        self.month_button = tk.Radiobutton(self.cabin, text='Месяц', variable=self.r_var, value=1, command=self.draw_month_charts)
        self.month_button.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
        self.year_button = tk.Radiobutton(self.cabin, text='Год', variable=self.r_var, value=2, command=self.draw_year_charts)
        self.year_button.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
        self.interval_button = tk.Radiobutton(self.cabin, text='Интервал', variable=self.r_var, value=3, command=self.draw_interval_charts)
        self.interval_button.grid(row=row, column=3, padx=5, pady=5, sticky=tk.W)

    def draw_week_charts(self):
        print('WEEK')
        sql = """SELECT item_name, date(order_date)
                FROM order_history
                WHERE order_date BETWEEN date('2022-05-13 12:40:00') AND (SELECT date('2022-05-13', 'start of day', '-1 day'))"""
        # sql = """SELECT * FROM order_history"""
        cursor = self.dbase.cursor()
        uid = self.customer.return_uid()
        cursor.execute(sql)
        self.dbase.commit()
        array = cursor.fetchall()
        for arr in array:
            print(arr)

    def draw_month_charts(self):
        print('MONTH')

    def draw_year_charts(self):
        print('YEAR')

    def draw_interval_charts(self):
        pass


    def user_data(self, command):
        pass


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

    def get_user_uid(self, login):
        sql = """SELECT user_id FROM customers WHERE user_login = ?"""
        cursor = self.dbase.cursor()
        cursor.execute(sql, [login])
        result = cursor.fetchall()
        cursor.close()
        return result[0][0]

    def add_customer(self):
        if self.reg_login.get() != '':
            if self.reg_pwd.get() != '':
                if self.reg_rep_pwd.get() != '':
                    if self.reg_pwd.get() == self.reg_rep_pwd.get():
                        if self.reg_email.get() != '':
                            if self.email_check(self.reg_email.get()):
                                if self.get_login_pwd(self.reg_login.get()) == 0:
                                    if self.insert_customer(self.reg_login.get(), self.reg_pwd.get(), self.reg_email.get()):
                                        uid = self.get_user_uid(self.reg_login.get())
                                        self.customer = customer.Customer(self.reg_login.get(), uid)
                                        self.cabinet_window()
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
