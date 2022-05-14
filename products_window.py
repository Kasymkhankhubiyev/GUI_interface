import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3 as db

def prod_win_construct(table, prod_list, items_list, spinboxs_list, buttons_list, row_counter):
    for row in range(len(prod_list)):
        lbl = Item_label(table, text=prod_list[row], item_name=prod_list[row], font=('Arial', 12))
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        items_list.append(lbl)
        tk.Label(table, text='кол-во', font=('Arial', 12)).grid(row=row, column=1, padx=10, pady=5)
        spin = tk.Spinbox(table, from_=0, to=100, width=5, font=('Arial', 12))
        spin.grid(row=row, column=2, padx=10, pady=5)
        spinboxs_list.append(spin)
        btn = Mybutton(table, drink_id=row+row_counter, text='🛒', fg='GREEN', font=('Aril', 11))
        btn.config(command=lambda button=btn: add_to_basket(button))
        buttons_list.append(btn)
        btn.grid(row=row, column=3, padx=10, pady=5)