import tkinter as tk


class ItemLabel(tk.Label):
    def __init__(self, master, item_name, *args, **kwargs):
        super(ItemLabel, self).__init__(master, *args, **kwargs)
        self.item_name = item_name

    def get_item_name(self):
        return self.item_name
