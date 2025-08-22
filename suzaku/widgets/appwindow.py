from .app import SkApp
from .window import SkWindow


class SkAppWindow(SkWindow):

    _instance_count = 0

    def __init__(
        self,
        *args,
        is_always_update: bool = ...,
        is_get_context_on_focus: bool = ...,
        vsync: bool = ...,
        **kwargs,
    ) -> None:
        """Main window that connects SkApp with SkWindow."""
        import platform

        if platform.system() == "Darwin":
            if "force_hardware_acceleration" in kwargs.keys():
                kwargs.pop("force_hardware_acceleration")

        self.app = SkApp(
            is_always_update=is_always_update,
            is_get_context_on_focus=is_get_context_on_focus,
            vsync=vsync,
        )
        super().__init__(parent=self.app, *args, **kwargs)
        if self.__class__._instance_count == 0:
            self.__class__._instance_count += 1
        else:
            raise ValueError("SkAppWindow can only be instantiated once.")
        self.attributes["name"] = "sk_appwindow"

        del platform

    def run(self, *args, **kwargs) -> None:
        """Run application."""
        self.app.run(*args, **kwargs)

    def quit(self, *args, **kwargs) -> None:
        """Exit application."""
        self.app.quit(*args, **kwargs)

    mainloop = run


Sk = SkAppWindow
