from .window import SkWindow


class SkAppWindow(SkWindow):
    def __init__(self, *args, **kwargs):
        from .app import SkApp
        self.app = SkApp()
        super().__init__(parent=self.app, *args, **kwargs)
        self.window_attr["name"] = "sk_appwindow"

    def run(self):
        self.app.run()

    def winfo_app(self):
        return self.app