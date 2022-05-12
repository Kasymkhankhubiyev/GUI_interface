import tkinter as tk

def create_window():
    window = tk.Tk()
    window.title("RNBCoffee")
    window.geometry("700x500")
    icon = tk.PhotoImage(file='rnb.png')
    window.iconphoto(False, icon)
    return window

win1 = create_window()
rnb_image = tk.PhotoImage(file='rnb.png')
rnb_image = rnb_image.subsample(2, 2)
image_lable = tk.Label(win1, image=rnb_image)
image_lable.place(x=20, y=20)
win1.mainloop()