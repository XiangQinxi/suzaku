from .after import After

from typing import Union, Any


class EventHanding(After):

    """
    Event binding manager.

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
                Event name, create if not existed.

                事件名称，没有则创建。

            *args: 
                Passed to `evt`.

                传参。

            **kwargs: 
                Passed to `evt`.

                传参。

        Returns:
            function_return (Any): Return value from the function, or False for failed. 函数返回值，出错则False。

        """

        if not name in self.events:
            self.events[name] = []

        for evt in self.events[name]:
            evt(*args, **kwargs)


    def bind(self, name: str, func: callable, add: bool=True) -> "EventHanding":
        """
        Bind event.

        绑定事件。

        Args:
            name (str): 
                Event name, create if not existed.

                事件名称，没有则创建。

            func (callable): 
                Function to bind.
                
                绑定函数。

            add (bool): 
                Whether to add after existed events, otherwise clean other and add itself.

                是否在绑定的事件后添加，而不是清除其他事件只保留自己。

        Returns:
            self

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

            func (callable): 
                Function to unbind.
                
                要解绑函数。
        Returns:
            None
        """
        self.events[name].remove(func)


class Event:

    """
    Used to pass event via arguments.

    用于传递事件的参数。
    """

    def __init__(self, event_type: str, x: int = None, y: int = None, rootx: int = None, rooty: int = None,
                 key: int = None, keyname: str = None, mods: str = None, char: str = None,
                 width: int = None, height: int = None):
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
