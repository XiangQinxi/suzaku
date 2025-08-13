from ..base.appbase import SkAppBase


class SkApp(SkAppBase):

    def __init__(
        self,
        *args,
        is_always_update: bool = False,
        is_get_context_on_focus: bool = False,
        **kwargs,
    ):
        """Main application that connects SkAppWindow with SkAppBase.

        :param is_always_update: Whether to always update the application.
        :param is_get_context_on_focus: Whether to update the application when it is focused.
        :param args: Arguments for SkAppBase.
        :param kwargs: Keyword arguments for SkAppBase.
        """
        super().__init__(
            *args,
            is_always_update=is_always_update,
            is_get_context_on_focus=is_get_context_on_focus,
            **kwargs,
        )
