import typing

from ..base.appbase import SkAppBase


class SkApp(SkAppBase):
    """
    :param bool is_always_update:
        Whether to continuously refresh (if `False`, refresh only when a window event is triggered).
        【是否一直刷新（如果为False，则只有触发窗口事件时才刷新）】
    :param bool is_get_context_on_focus:
        Is the context only obtained when the window gains focus.
        【是否只有在窗口获得焦点时，获得上下文】
    """

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(
            **kwargs,
        )
