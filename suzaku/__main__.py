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
    app = SkApp(is_get_context_on_focus=False, is_always_update=False, framework="glfw")
    # print(glfw.default_window_hints())

    def create1window():
        window = SkWindow(
            anti_alias=True,
            parent=None,
            title="Suzaku GUI",
            size=(280, 630),
        )
        window.bind("drop", lambda evt: print("drop", evt))

        var1 = SkBooleanVar()
        var1.bind("change", lambda evt: print("Changed:", evt))

        menubar = SkMenuBar(window)
        menubar.box(side="top", padx=0, pady=0)

        popupmenu = SkPopupMenu(window)
        popupmenu.add_command("New window", command=create1window)
        """popupmenu.add_command("New project")
        popupmenu.add_command("Open project")
        popupmenu.add_command("Save changes")
        popupmenu.add_command("Save as...")"""
        popupmenu.add_separator()
        popupmenu.add_checkitem("Agreed", variable=var1)
        popupmenu.add_radioitem("Simple", value=False, variable=var1)
        popupmenu.add_radioitem("Complex", value=True, variable=var1)
        popupmenu.add_separator()
        popupmenu.add_command(
            "Help", command=lambda: show_message(window, message="Hello")
        )
        popupmenu.add_command("Exit", command=window.destroy)

        menubar.add_cascade("File", menu=popupmenu)
        menubar.add_separator()
        menubar.add_command("Exit", command=window.destroy)

        def change_theme(event: SkEvent):
            _text = event.widget.cget("text")
            if _text == "Light":
                window.apply_theme(default_theme)
            elif _text == "Dark":
                window.apply_theme(dark_theme)

        frame = SkCard(window)

        SkTextButton(frame, text="This is a SkTextButton").box(padx=10, pady=(10, 0))

        SkCheckButton(
            frame,
            text="This is a CheckBox",
            variable=var1,
        ).box(padx=10, pady=(10, 0))

        SkRadioButton(frame, text="SkRadioItem 1", value=False, variable=var1).box(
            padx=10, pady=(10, 0)
        )
        SkRadioButton(frame, text="SkRadioItem 2", value=True, variable=var1).box(
            padx=10, pady=(10, 0)
        )

        SkSeparator(frame).box(padx=0, pady=(10, 0))

        SkText(frame, text="This is a SkText").box(padx=10, pady=(10, 0))
        # SkCheckItem(frame, text="这是一个复选框").box(padx=10, pady=10)

        var2 = SkStringVar()
        SkEntry(frame, placeholder="TextVariable", textvariable=var2).box(
            padx=10, pady=(10, 0)
        )
        SkEntry(frame, placeholder="Password", textvariable=var2, show="●").box(
            padx=10, pady=(10, 0)
        )
        SkLabel(frame, textvariable=var2).box(padx=10, pady=(10, 0))

        SkSeparator(frame).box(padx=0, pady=(10, 0))

        SkText(frame, text="Theme Mode", align="left").box(padx=10, pady=(10, 0))

        listbox = SkListBox(frame, items=["Light", "Dark"])
        listbox.bind(
            "changed",
            change_theme,
        )
        listbox.selected_index(1)
        listbox.box(padx=10, pady=(10, 0))

        frame.box(padx=10, pady=10, expand=True)
        frame.bind_scroll_event()

        SkTextButton(window, text="Create New window", command=create1window).box(
            padx=10, pady=(5, 0)
        )
        SkTextButton(window, text="Close the window", command=window.destroy).box(
            side="bottom"
        )

    create1window()

    app.run()
