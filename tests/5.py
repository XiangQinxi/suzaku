import tkinter as tk
from tkinter import ttk
from sv_ttk import use_dark_theme

root = tk.Tk()
root.geometry("600x400+200+200")
root.title("Ttk 主题小部件演示")

use_dark_theme()

text = tk.StringVar()
style = ttk.Style(root)


def change_theme():
    style.theme_use(selected_theme.get())


def callback():
    pass


left_frame = tk.Frame(root, width=300, height=400)
left_frame.pack(side="left", fill="both", padx=10, pady=5, expand=True)

right_frame = tk.Frame(root, width=300, height=400)
right_frame.pack(side="right", fill="both", padx=10, pady=5, expand=True)

selected_theme = tk.StringVar()
theme_frame = ttk.LabelFrame(left_frame, text="Themes")
theme_frame.pack(padx=10, pady=10, ipadx=30, ipady=30)

for theme_name in style.theme_names():
    rb = ttk.Radiobutton(
        theme_frame,
        text=theme_name,
        value=theme_name,
        variable=selected_theme,
        command=change_theme,
    )
    rb.pack(expand=True, fill="both", padx=5, pady=5)

label = ttk.Label(right_frame, text="ttk标签")
label.pack(pady=5)
button = ttk.Button(right_frame, text="ttk按钮", command=callback)
button.pack(pady=5)
entry = ttk.Entry(right_frame, textvariable=text, text="文本框")
entry.pack(pady=5)
entry.insert(0, "ttk单行文本框")
frame2 = ttk.LabelFrame(right_frame, text="ttk复选框")
frame2.pack(pady=5)
cb3 = ttk.Checkbutton(frame2, text="Number 3")
cb3.pack()
cb4 = ttk.Checkbutton(frame2, text="Number 4")
cb4.pack()
frame4 = ttk.LabelFrame(right_frame, text="ttk单选按钮")
frame4.pack(pady=5)
r1 = ttk.Radiobutton(frame4, text="option 1", value=1)
r1.pack()
r2 = ttk.Radiobutton(frame4, text="option 2", value=2)
r2.pack()
scale2 = ttk.Scale(right_frame, from_=0, to=100, orient="horizontal", length=100)
scale2.pack(pady=5)
combobox = ttk.Combobox(right_frame, values=["Python", "Java", "C++"])
combobox.pack(pady=5)
menubttn = ttk.Menubutton(right_frame, text="ttk菜单按钮")
menu = tk.Menu(menubttn, tearoff=0)
menu.add_checkbutton(label="Python")
menu.add_checkbutton(label="Java")
menubttn["menu"] = menu
menubttn.pack(pady=5)
spinbox2 = ttk.Spinbox(right_frame, from_=0, to=10, wrap=True)
spinbox2.pack(pady=5)
root.mainloop()
