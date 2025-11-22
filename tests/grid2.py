from suzaku import *

root = Sk(theme=sv_light_theme)
root.bind_scroll_event()

la1 = SkText(root, text="用户名：")
la1.grid(row=0, column=0)  # 0行0列

la2 = SkText(root, text="密码：", align="left")
la2.grid(row=1, column=0)

en1 = SkEntry(root)  # 用户名文本框
en1.grid(row=0, column=1, columnspan=2)  # 0行1列，跨2列

en2 = SkEntry(root, show="*")  # 密码文本框
en2.grid(row=1, column=1, columnspan=2)  # 1行1列，跨2列

SkEmpty(root).grid(row=2, column=0)
but1 = SkTextButton(root, text="确定")
but1.grid(row=2, column=1)
but2 = SkTextButton(root, text="取消")
but2.grid(row=2, column=2)

root.mainloop()
