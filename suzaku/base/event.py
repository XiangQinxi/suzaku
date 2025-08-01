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

        self.evts = {}

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

        if not name in self.evts:
            self.evts[name] = []
            try:
                for evt in self.evts[name]:
                    return evt(*args, **kwargs)
            except Exception as e:
                print(e)
                return False
        else:
            return True

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
        if name not in self.evts:
            self.evts[name] = [func]
        if add:
            self.evts[name].append(func)
        else:
            self.evts[name] = [func]
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
        self.evts[name].remove(func)


class Event:

    """
    Used to pass event via arguments.

    用于传递事件的参数。
    """

    def __init__(self, x: int = None, y: int = None, rootx: int = None, rooty: int = None):
        """
        Used to pass event via arguments.

        用于传递事件的参数。

        Args:
            x: 
                x position of cursor / component (Relative to window).

                鼠标的/组件的x坐标(相对于窗口)。

            y: 
                y position of cursor / component (Relative to window).

                鼠标的/组件的y坐标(相对于窗口)。

            rootx: 
                x position of cursor / component (Relative to screen).

                鼠标的/组件的x坐标(相对于荧幕)。

            rooty: 
                y position of cursor / component (Relative to screen).

                鼠标的/组件的y坐标(相对于荧幕)。

        """
        self.x = x
        self.y = y
        self.rootx = rootx
        self.rooty = rooty
