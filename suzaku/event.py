from typing import Any, Union

from suzaku.after import SkAfter


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


class SkEvent:
    """
    Used to pass event via arguments.

    用于传递事件的参数。
    """

    def __init__(
        self,
        event_type: str,
        x: Union[int, None] = None,
        y: Union[int, None] = None,
        rootx: Union[int, None] = None,
        rooty: Union[int, None] = None,
        key: Union[int, None, str] = None,
        keyname: Union[str, None] = None,
        mods: Union[str, None] = None,
        char: Union[str, None] = None,
        width: Union[int, None] = None,
        height: Union[int, None] = None,
        widget=None,
    ):
        """
        Used to pass event via arguments.

        Args:
            x:
                x position of cursor / component (Relative to window).

            y:
                y position of cursor / component (Relative to window).

            rootx:
                x position of cursor / component (Relative to screen).

            rooty:
                y position of cursor / component (Relative to screen).

            key:
                Key name.

            mods:
                Modifier keys.

        """
        self.event_type = event_type
        self.x = x
        self.y = y
        self.rootx = rootx
        self.rooty = rooty
        self.key = key
        self.keyname = keyname
        self.mods = mods
        self.char = char
        self.width = width
        self.height = height
        self.widget = widget
