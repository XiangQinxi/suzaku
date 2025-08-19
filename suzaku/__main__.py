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
    app = SkApp(is_get_context_on_focus=True, is_always_update=False)
    # print(glfw.default_window_hints())

    def create1window():
        window = SkToplevel(
            parent=None,
            # theme=SkTheme.INTERNAL_THEMES["default.dark"],
            title="Suzaku GUI",
            size=(280, 460),
        )
        # window.hide()
        window.bind("drop", lambda evt: print("drop", evt))

        frame = SkCard(window)
        # frame.allowed_out_of_bounds = True

        SkButton(frame, text="This is a SkButton").box(padx=10, pady=(10, 0))
        SkButton(frame, text="Ask Notice", command=window.hongwen).box(
            padx=10, pady=(10, 0)
        )
        SkLabel(frame, text="This is a SkLabel").box(padx=10, pady=(10, 0))
        SkCheckbox(frame, text="这是一个复选框").box(padx=10, pady=10)

        var = SkStringVar()
        SkEntry(frame, placeholder="数值绑定", textvariable=var).box(
            padx=10, pady=(10, 0)
        )
        SkLabel(frame, textvariable=var).box(padx=10, pady=(10, 0))

        frame2 = SkCard(frame)
        SkButton(frame2, text="Create 1 New window", command=create1window).box(
            padx=10, pady=(10, 0)
        )
        frame2.box(padx=10, pady=10, expand=True)

        frame.box(padx=10, pady=10, expand=True)

        SkButton(window, text="Close the window", command=window.destroy).box(
            side="bottom"
        )

    create1window()

    app.run()
