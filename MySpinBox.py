import tkinter as tk


class MySpinbox(tk.Spinbox):
    def __init__(self, master, item_id, item_type_id=0, *args, **kwargs):
        super(MySpinbox, self).__init__(master, *args, **kwargs)
        self.item_id = item_id

    def get_spinbox_id(self):
        return self.item_id