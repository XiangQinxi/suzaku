from suzaku import *

import skia


app = SkApp()

window = SkWindow(theme=dark_theme)

popupmenu = SkPopupMenu(window)
popupmenu.add_command("文件")
popupmenu.add_command("编辑")
popupmenu.add_command("视图")
popupmenu.add_command("窗口")
popupmenu.add_command("帮助")
popupmenu.add_command("帮助")

btn = SkTextButton(window, "删除一个选项")
btn.box(side="top")

menubutton = SkMenuButton(
    window,
    "MenuButton",
    menu=popupmenu,
)
menubutton.box()

app.mainloop()
