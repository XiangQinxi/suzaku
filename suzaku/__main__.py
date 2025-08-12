try:
    from suzaku.sk import *
except:
    raise ModuleNotFoundError(
        "Suzaku module not found! Install suzaku or run with python3 -m suzaku in parent dir."
    )
import glfw
import skia

if __name__ == "__main__":
    # 修改主窗口创建代码
    root = Sk(
        title="Suzaku GUI",
        size=(280, 460),
    )
    # print(glfw.default_window_hints())
    root.bind("drop", lambda evt: print("drop", evt))

    frame = SkFrame(root, border=True)

    SkButton(frame, text="This is a SkButton / 这是一个按钮").box(padx=8, pady=(8, 0))
    SkLabel(frame, text="This is a SkLabel / 这是一个标签").box(padx=8, pady=(8, 0))

    SkCheckbox(frame, text="这是一个复选框").box(padx=10, pady=10)

    var = SkStringVar()
    SkEntry(frame, placeholder="数值绑定", textvariable=var).box(padx=8, pady=(8, 0))
    SkLabel(frame, textvariable=var).box(padx=8, pady=(8, 0))

    frame.box(padx=10, pady=10, expand=True)

    SkButton(root, text="Close the window", command=root.destroy).box(side="bottom")

    root.run()
