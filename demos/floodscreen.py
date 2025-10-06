import suzaku as sk


class FloodScreen(sk.SkWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window_attr("border", False)
        self.titlebar = sk.SkTitlebar(self)
        self.titlebar.box(side="top", padx=0, pady=0)


if __name__ == "__main__":
    app = sk.SkApp()
    window = FloodScreen(app, theme=sk.dark_theme)
    app.mainloop()
