import tkinter as tk


class MySpinbox(tk.Spinbox):
    def __init__(self, master, item_id, item_type_id, *args, **kwargs):
        super(MySpinbox, self).__init__(master, *args, **kwargs)
        self.item_id = item_id
        self.item_type_id = item_type_id

    def get_spinbox_id(self):
        return self.item_id

    def get_item_type(self):
        return self.item_type_id
