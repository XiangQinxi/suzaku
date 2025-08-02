try:
    from suzaku import *
except:
    raise ModuleNotFoundError("Suzaku module not found! Install suzaku or run with python3 -m suzaku in parent dir.")
import skia


if __name__ == "__main__":
    # 修改主窗口创建代码
    appwindow = Sk(
        title="Suzaku GUI",
        themename="light",
        size=(320, 360),
        #force_hardware_acceleration=True
    )
    appwindow.bind("close", lambda: print("Window closed"))

    SkButton(appwindow, text=f"Light Theme / 切换至Light主题", command=lambda: appwindow.theme.use_theme("light")).vbox(padx=10, pady=10)
    SkButton(appwindow, text=f"Dark Theme / 切换至Dark主题", command=lambda: appwindow.theme.use_theme("dark")).vbox(padx=10, pady=10)
    SkLabel(appwindow, text="This is a SkLabel / 这是一个标签").vbox(padx=10, pady=10)
    label = SkLabel(appwindow)
    label.bind("update", lambda: print(appwindow.focus_get()))
    label.vbox(padx=10, pady=10)
    print(label.winfo_id())

    SkEmpty(appwindow).vbox(padx=0, pady=0, expand=True)

    #SkButton(appwindow, text=f"Horizontal Layout / 水平布局", command=lambda: appwindow.winfo_layout().change_direction("h")).vbox(padx=10, pady=10)
    #SkButton(appwindow, text=f"Vertical Layout / 垂直 布局", command=lambda: appwindow.winfo_layout().change_direction("v")).vbox(padx=10, pady=10)

    SkButton(appwindow, text=f"Close Window / 关闭窗口", command=appwindow.destroy, style="Close.SkButton").vbox(padx=10, pady=10)

    """
    toplevel = SkWindow()
    SkButton(toplevel, text=f"关闭窗口", command=toplevel.destroy, style="Close.SkButton").vbox(padx=10, pady=10)
    """
    appwindow.run()
