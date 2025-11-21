from tkinter import *

root = Tk()  # 源码来自wb98.com

la1 = Label(root, text="用户名：")
la1.grid(row=0, column=0, padx=(10, 0), pady=10)  # 0行0列

en1 = Entry(root)  # 用户名文本框
en1.grid(row=0, column=1, columnspan=2, padx=(0, 10), ipadx=60)  # 0行1列，跨2列

la2 = Label(root, text="密　码：")
la2.grid(row=1, column=0, padx=(10, 0))

en2 = Entry(root)  # 密码文本框
en2.grid(row=1, column=1, columnspan=2, padx=(0, 10), ipadx=60)  # 1行1列，跨2列

but1 = Button(root, text="确定")
but1.grid(row=2, column=1, sticky=E, pady=10, ipadx=30)
but2 = Button(root, text="取消")
but2.grid(row=2, column=2, sticky=W, padx=(0, 30), ipadx=30)

root.mainloop()
