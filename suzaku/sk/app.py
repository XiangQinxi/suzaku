from ..base.application import Application


class SkApp(Application):

    def __init__(self, *args, **kwargs):
        """
        SkApp, inherited from Application
        应用程序，继承自Application
        """
        super().__init__(*args, **kwargs)
