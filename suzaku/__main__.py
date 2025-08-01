from suzaku import *
import skia


if __name__ == "__main__":
    appwindow = Sk(title="Suzaku GUI", themename="light", size=(300, 300))
    appwindow.bind("close", lambda: print("Window closed"))

    SkButton(appwindow, text=f"切换至Light主题", command=lambda: appwindow.theme.use_theme("light")).vbox(padx=10, pady=10)
    SkButton(appwindow, text=f"切换至Dark主题", command=lambda: appwindow.theme.use_theme("dark")).vbox(padx=10, pady=10)

    SkEmpty(appwindow).vbox(padx=0, pady=0, expand=True)

    btn = SkButton(appwindow, text=f"移除自己", command=lambda: btn.box_forget()).vbox(padx=10, pady=10)

    SkButton(appwindow, text=f"水平布局", command=lambda: appwindow.winfo_layout().change_direction("h")).vbox(padx=10, pady=10)
    SkButton(appwindow, text=f"垂直布局", command=lambda: appwindow.winfo_layout().change_direction("v")).vbox(padx=10, pady=10)

    SkButton(appwindow, text=f"关闭窗口", command=appwindow.quit).vbox(padx=10, pady=10)

    #SkButton(appwindow, text=f"按钮").put(margin=(10, 10, 10, 10))

    appwindow.run()
