from .app import SkApp
from .window import SkWindow


class SkAppWindow(SkWindow):

    _instance_count = 0

    def __init__(self, *args, window_event_wait: bool = False, **kwargs) -> None:
        """Main window that connects SkApp with SkWindow."""
        self.app = SkApp(window_event_wait=window_event_wait)
        super().__init__(parent=self.app, *args, **kwargs)
        if self.__class__._instance_count == 0:
            self.__class__._instance_count += 1
        else:
            raise ValueError("SkAppWindow can only be instantiated once.")
        self.attributes["name"] = "sk_appwindow"

    def run(self, *args, **kwargs) -> None:
        """Run application."""
        self.app.run(*args, **kwargs)

    def quit(self, *args, **kwargs) -> None:
        """Exit application."""
        self.app.quit(*args, **kwargs)

    mainloop = run


Sk = SkAppWindow
