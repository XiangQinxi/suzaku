from suzaku import *
import skia


if __name__ == "__main__":
    appwindow = Sk(title="Suzaku GUI", themename="light", size=(300, 300))
    appwindow.bind("close", lambda: print("Window closed"))

    SkButton(appwindow, text=f"切换至Light主题", command=lambda: appwindow.theme.use_theme("light")).vbox(padx=10, pady=10)
    SkButton(appwindow, text=f"切换至Dark主题", command=lambda: appwindow.theme.use_theme("dark")).vbox(padx=10, pady=10)

    SkButton(appwindow, text=f"按钮").vbox(padx=10, pady=10, expand=True)

    #SkButton(appwindow, text=f"按钮").put(margin=(10, 10, 10, 10))

    appwindow.run()
