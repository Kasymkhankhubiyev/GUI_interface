import tkinter as tk


class Mybutton(tk.Button):
    def __init__(self, master, drink_id, *args, **kwargs):
        super(Mybutton, self).__init__(master, *args, **kwargs)
        self.drink_id = drink_id

    def get_button_id(self):
        return self.drink_id
