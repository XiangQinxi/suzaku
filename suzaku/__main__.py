try:
    from suzaku import *
except:
    raise ModuleNotFoundError("Suzaku module not found! Install suzaku or run with python3 -m suzaku in parent dir.")
import skia


if __name__ == "__main__":
    appwindow = Sk(title="Suzaku GUI", themename="light", size=(480, 300))
    appwindow.bind("close", lambda: print("Window closed"))

    SkButton(appwindow, text=f"Switch to light theme", command=lambda: appwindow.theme.use_theme("light")).vbox(padx=10, pady=10)
    SkButton(appwindow, text=f"Switch to dark theme", command=lambda: appwindow.theme.use_theme("dark")).vbox(padx=10, pady=10)

    SkEmpty(appwindow).vbox(padx=0, pady=0, expand=True)

    btn = SkButton(appwindow, text=f"Remove self", command=lambda: btn.box_forget()).vbox(padx=10, pady=10)

    SkButton(appwindow, text=f"Horizontal layout", command=lambda: appwindow.winfo_layout().change_direction("h")).vbox(padx=10, pady=10)
    SkButton(appwindow, text=f"Vertical layout", command=lambda: appwindow.winfo_layout().change_direction("v")).vbox(padx=10, pady=10)

    SkButton(appwindow, text=f"Close this window", command=appwindow.quit).vbox(padx=10, pady=10)

    #SkButton(appwindow, text=f"Button").put(margin=(10, 10, 10, 10))

    appwindow.run()
