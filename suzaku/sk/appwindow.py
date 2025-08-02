from .window import SkWindow


class SkAppWindow(SkWindow):

    def __init__(self, *args, **kwargs) -> None:
        """
        Main window that connects SkApp with SkWindow.

        将SkApp与SkWindow组合起来的主窗口。
        """
        from .app import SkApp
        self.app = SkApp()
        super().__init__(parent=self.app, *args, **kwargs)
        self.attributes["name"] = "sk_appwindow"

    def run(self, *args, **kwargs) -> None:
        """
        Run application.

        运行应用程序。
        """
        self.app.run(*args, **kwargs)

    mainloop = run  # 别名

    def quit(self, *args, **kwargs) -> None:
        """
        Exit application.
        
        退出应用程序。
        """
        self.app.quit(*args, **kwargs)

    from .app import SkApp

    def winfo_app(self) -> SkApp:
        """
        Get SkApp class.

        获取`SkApp`类。
        """
        return self.app