import suzaku as sk


class FloodScreen(sk.SkWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup()

        from pywinstyles import apply_style

        apply_style(self.window_id, "dark")

    def setup(self):
        self.window_attr("border", False)
        self.titlebar = sk.SkTitlebar(self)
        self.titlebar.box(side="top", padx=0, pady=0)

        self.tabs = sk.SkTabs(self, expand=False)
        self.tabs.box(expand=True, padx=10, pady=10)

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

        self.tabs.select(0)

    def setup_tab1(self):
        self.tab1 = sk.SkFrame(self.tabs)
        self.tabs.add(self.tab1, "Home")

    def setup_tab2(self):
        self.tab2 = sk.SkFrame(self.tabs)
        self.tabs.add(self.tab2, "Settings")

        def switch():
            if switch_theme.checked:
                self.apply_theme(sk.sv_dark_theme)
            else:
                self.apply_theme(sk.sv_light_theme)

        sk.SkLabel(self.tab2, "Theme", align="left").box("top", padx=5, pady=5)
        switch_theme = sk.SkSwitch(self.tab2, text="Dark mode", command=switch).box(
            side="top",
            pady=5,
            padx=5,
        )
        # switch_theme.invoke()

    def setup_tab3(self):
        self.tab3 = sk.SkFrame(self.tabs)
        self.tabs.add(self.tab3, "About")


if __name__ == "__main__":
    app = sk.SkApp()
    window = FloodScreen(app, title="FloodScreen", theme=sk.sv_light_theme)
    app.mainloop()
