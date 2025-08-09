from typing import Any, Union, Optional, List

from dataclasses import dataclass
from .after import SkAfter


class SkEventHanding(SkAfter):
    """
    SkEvent binding manager.

    事件绑定管理器。

    """

    def __init__(self):
        """
        Initialize all bindable events.

        初始化所有可绑定的事件。

        """

        self.events = {}

    def event_generate(self, name: str, *args, **kwargs) -> Union[bool, Any]:
        """
        Send event signal.

        发出事件信号。

        Args:
            name (str):
                SkEvent name, create if not existed.

                事件名称，没有则创建。

            *args:
                Passed to `event`.

                传参。

            **kwargs:
                Passed to `event`.

                传参。

        Returns:
            function_return (Any): Return value from the function, or False for failed. 函数返回值，出错则False。

        """

        if not name in self.events:
            self.events[name] = []

        for event in self.events[name]:
            event(*args, **kwargs)

    def bind(self, name: str, func: callable, add: bool = True) -> "SkEventHanding":
        """
        Bind event.

        绑定事件。

        Args:
            name (str):
                SkEvent name, create if not existed.

                事件名称，没有则创建。

            func (function):
                Function to bind.

                绑定函数。

            add (bool):
                Whether to add after existed events, otherwise clean other and add itself.

                是否在绑定的事件后添加，而不是清除其他事件只保留自己。

        Returns:
            cls

        """
        if name not in self.events:
            self.events[name] = [func]
        if add:
            self.events[name].append(func)
        else:
            self.events[name] = [func]
        return self

    def unbind(self, name: str, func: callable) -> None:
        """
        Unbind event.

        解绑事件。

        -> 后续事件将以ID作为识别码来解绑

        Args:
            name (str):
                Name of the event.

                事件名称。

            func (function):
                Function to unbind.

                要解绑函数。
        Returns:
            None
        """
        self.events[name].remove(func)


@dataclass
class SkEvent:
    """
    Used to pass event via arguments.

    用于传递事件的参数。
    """
    event_type: str
    x: Optional[int] = None
    y: Optional[int] = None
    rootx: Optional[int] = None
    rooty: Optional[int] = None
    key: Union[int, str, None] = None
    keyname: Optional[str] = None
    mods: Optional[str] = None
    char: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    widget: Any = None
    maximized: Optional[bool] = None
    paths: Optional[List[str]] = None
    iconified: Optional[bool] = None
