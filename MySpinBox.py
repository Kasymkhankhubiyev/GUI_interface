import tkinter as tk


class MySpinbox(tk.Spinbox):
    def __init__(self, master, drink_id, *args, **kwargs):
        super(MySpinbox, self).__init__(master, *args, **kwargs)
        self.drink_id = drink_id

    def get_spinbox_id(self):
        return self.drink_id