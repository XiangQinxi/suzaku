from suzaku.widgets.app import SkApp

from .window import SkWindow


class SkAppWindow(SkWindow):

    def __init__(self, *args, **kwargs) -> None:
        """Main window that connects SkApp with SkWindow."""
        self.app = SkApp()
        super().__init__(parent=self.app, *args, **kwargs)
        self.attributes["name"] = "sk_appwindow"

    def run(self, *args, **kwargs) -> None:
        """Run application."""
        self.app.run(*args, **kwargs)

    mainloop = run  # 别名

    def quit(self, *args, **kwargs) -> None:
        """Exit application."""
        self.app.quit(*args, **kwargs)

    def winfo_app(self) -> SkApp:
        """Get SkApp class."""
        return self.app


Sk = SkAppWindow