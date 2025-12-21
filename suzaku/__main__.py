try:
    import suzaku as sk
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
            title=f"Suzaku GUI",
            size=(320, 650),
        )
        window.minsize(100, 80)
        window.resizable(True)
        window.bind("drop", lambda evt: print("Dropped:", evt["paths"]))

        var1 = SkBooleanVar()
        var1.bind("change", lambda evt: print("Changed:", evt["value"]))

        headerbar = SkTitlebar(window).box(side="top", padx=0, pady=0)
        headerbar.hide()

        menubar = SkMenuBar(window)
        menubar.box(side="top", padx=0, pady=0)

        popupmenu = SkPopupMenu(window)
        popupmenu.add_command("New project")
        popupmenu.add_command("Open project")
        # popupmenu.add_cascade("")
        popupmenu.add_separator()
        popupmenu.add_checkitem("Agreed", variable=var1)
        popupmenu.add_radioitem("Simple", value=False, variable=var1)
        popupmenu.add_radioitem("Complex", value=True, variable=var1)
        popupmenu.add_switch("Switch", variable=var1)
        popupmenu.add_separator()
        popupmenu.add_command("Help", command=lambda: show_message(window, message="Hello"))
        popupmenu.add_command("Exit", command=window.destroy)

        menubar.add_cascade("File", menu=popupmenu)
        menubar.add_command("New", command=create1window)
        menubar.add_command("Exit", command=window.destroy)

        tabs = SkTabs(window, expand=True)

        def tab1():
            tab_widgets = SkFrame(tabs)
            tab_widgets.bind_scroll_event()
            tabs.add(tab_widgets, text="Widgets")

            SkTextButton(tab_widgets, text="SkTextButton", command=lambda: print("Clicked")).box(
                padx=10, pady=(10, 0)
            )

            combobox = SkCombobox(tab_widgets, values=["Item 1", "Item 2"], readonly=False).box(
                padx=10, pady=(10, 0)
            )
            combobox.bind(
                "command", lambda evt: print(f"Selected: (Index: {evt['index']}) {evt['text']}")
            )
            SkListBox(tab_widgets, items=["SkListItem 1", "SkListItem 2"]).box(
                padx=10, pady=(10, 0)
            )

            SkCheckButton(
                tab_widgets,
                text="SkCheckItem",
                variable=var1,
            ).box(padx=10, pady=(10, 0))

            SkRadioButton(tab_widgets, text="SkRadioItem 1", value=False, variable=var1).box(
                padx=10, pady=(10, 0)
            )
            SkRadioButton(tab_widgets, text="SkRadioItem 2", value=True, variable=var1).box(
                padx=10, pady=(10, 0)
            )

            SkSwitch(tab_widgets, text="SkSwitch", variable=var1).box(padx=10, pady=(10, 0))

            SkSlider(tab_widgets).box(padx=10, pady=(10, 0))

            frame1 = SkFrame(tab_widgets).box(padx=10, pady=(10, 0))

            var2 = SkFloatVar(25)

            progress = SkProgressBar(frame1, variable=var2).grid(
                row=0, column=0, columnspan=3, padx=0, pady=5
            )

            def start(_=None):
                progress.configure(value=progress.cget("value") * 1.1 + 0.1)
                start_button.configure(disabled=True)
                progress.update(True)
                start_button.update(True)
                if progress.cget("value") < progress.cget("maxvalue"):
                    window.bind("delay[10ms]", start)
                else:
                    start_button.configure(disabled=False)
                    start_button.update(True)

            SkTextButton(
                frame1,
                text="Increase",
                command=lambda: progress.configure(value=progress.cget("value") + 10),
            ).grid(row=1, column=0, padx=3, pady=3)

            SkTextButton(
                frame1,
                text="Decrease",
                command=lambda: progress.configure(value=progress.cget("value") - 10),
            ).grid(row=1, column=1, padx=3, pady=3)

            start_button = SkTextButton(frame1, text="Start", command=start).grid(
                row=1, column=2, padx=3, pady=3
            )

            SkLabel(frame1, textvariable=var2).grid(row=1, column=3, padx=3, pady=3)

            SkSeparator(tab_widgets, orient=Orient.H).box(padx=0, pady=(10, 0))

            SkText(tab_widgets, text="SkText").box(padx=10, pady=(10, 0))
            # SkCheckItem(tab_widgets, text="这是一个复选框").box(padx=10, pady=10)

            var2 = SkStringVar()
            SkEntry(tab_widgets, placeholder="TextVariable", textvariable=var2).box(
                padx=10, pady=(10, 0)
            )
            SkEntry(tab_widgets, placeholder="Password", textvariable=var2, show="●").box(
                padx=10, pady=(10, 0)
            )
            SkLabel(tab_widgets, text=f"Suzaku Version: {sk.__version__}").box(
                padx=10, pady=(10, 10)
            )

        tab1()

        def tab2():
            tab_settings = SkFrame(tabs)
            tab_settings.bind_scroll_event()
            tabs.add(tab_settings, text="Settings")

            def change_theme(event: SkEvent):
                window.apply_theme(themes[event["text"]])

            SkText(tab_settings, text="Theme", align="left").box(padx=10, pady=(10, 0))
            themes = {}
            for theme in SkTheme.loaded_themes:
                themes[theme.friendly_name] = theme
            listbox = SkListBox(tab_settings, items=list(themes.keys()))
            listbox.bind(
                "change",
                change_theme,
            )
            listbox.select(index=2)
            listbox.box(padx=10, pady=(10, 0))

            SkTextButton(
                tab_settings,
                text="Screenshot (wait 3s)",
                command=lambda: window.bind("delay[3s]", lambda _: window.save()),
            ).box(padx=10, pady=(10, 0))

            def anti_alias():
                window.anti_alias = switch.checked

            def custom_titlebar():
                window.window_attr("border", not switch2.checked)
                if switch2.checked:
                    headerbar.show()
                else:
                    headerbar.hide()
                window.update_layout()
                window.update(True)
                headerbar.update(True)

            switch = SkSwitch(
                tab_settings,
                text="Enabled Anti Aliasing",
                command=anti_alias,
                default=True,
            ).box(padx=10, pady=(10, 0))

            switch2 = SkSwitch(
                tab_settings,
                text="Enabled Custom Titlebar",
                command=custom_titlebar,
                default=False,
            ).box(padx=10, pady=(10, 0))

        tab2()

        tabs.select(0)
        tabs.box(padx=8, pady=8, expand=True)

        tipbar = SkTipBar(window, prefix="Entered widget: ")
        tipbar.box(side="bottom", padx=0, pady=0)

        window.update_layout()

        # window.bind("delay[5]", lambda _: print("Delay 5"))

    create1window()

    app.run()
    print("Closed")
