try:
    from suzaku import *
except:
    raise ModuleNotFoundError(
        "Suzaku module not found! Install suzaku or run with python3 -m suzaku in parent dir."
    )
import glfw
import skia

if __name__ == "__main__":
    # 修改主窗口创建代码
    app = SkApp(is_get_context_on_focus=True, is_always_update=False, framework="glfw")
    # print(glfw.default_window_hints())

    def create1window():
        window = SkWindow(
            anti_alias=True,
            parent=None,
            title="Suzaku GUI",
            size=(280, 550),
        )
        window.apply_theme(dark_theme)
        window.bind("drop", lambda evt: print("drop", evt))

        frame = SkCard(window)

        SkTextButton(
            frame, text="This is a SkTextButton", command=window.keyboard_open
        ).box(padx=10, pady=(10, 0))

        popupmenu = SkPopupMenu(frame)
        popupmenu.add_command("New window", command=create1window)
        popupmenu.add_command("New project")
        popupmenu.add_command("Open project")
        popupmenu.add_command("Save changes")
        popupmenu.add_command("Save as...")
        popupmenu.add_separator()
        popupmenu.add_command(
            "Help", command=lambda: show_message(window, message="Hello")
        )
        popupmenu.add_command("Exit", command=window.destroy)

        menubutton = SkMenu(
            frame,
            "This is a SkMenuButton",
            menu=popupmenu,
        )
        menubutton.box(padx=10, pady=(10, 0))

        checkbox = SkCheckItem(
            frame,
            text="This is a CheckBox",
            command=lambda: print("Checked:", checkbox.checked),
        )
        checkbox.box(padx=10, pady=(10, 0))

        SkSeparator(frame).box(padx=0, pady=(15, 0))

        SkText(frame, text="This is a SkLabel").box(padx=10, pady=(10, 0))
        # SkCheckItem(frame, text="这是一个复选框").box(padx=10, pady=10)

        var = SkStringVar()
        SkEntry(frame, placeholder="TextVariable", textvariable=var).box(
            padx=10, pady=(10, 0)
        )
        SkText(frame, textvariable=var).box(padx=10, pady=(10, 0))

        frame2 = SkCard(frame)
        SkTextButton(frame2, text="Create 1 New window", command=create1window).box(
            padx=10, pady=(10, 0)
        )
        SkTextButton(
            frame2,
            text="Switch to Light Theme",
            command=lambda: window.apply_theme(default_theme),
        ).box(padx=10, pady=(10, 0))
        SkTextButton(
            frame2,
            text="Switch to Dark Theme",
            command=lambda: window.apply_theme(dark_theme),
        ).box(padx=10, pady=(10, 10))

        frame2.box(padx=10, pady=10)
        frame2.bind_scroll_event()

        frame.box(padx=10, pady=10, expand=True)
        frame.bind_scroll_event()

        SkTextButton(window, text="Close the window", command=window.destroy).box(
            side="bottom"
        )

    create1window()

    app.run()
