from .after import After


class EventHanding(After):

    """
    事件绑定管理器
    """

    def __init__(self):

        """
        初始化所有可绑定的事件
        """

        self.evts = {}

    def event_generate(self, name: str, *args, **kwargs) -> bool:
        """
        发出事件信号

        :param name: 事件名称，没有则创建
        :param args: 传参
        :param kwargs: 传参
        :return:
        """

        if not name in self.evts:
            self.evts[name] = []
        for evt in self.evts[name]:
            evt(*args, **kwargs)

    def bind(self, name: str, func: callable, add: bool = True) -> "EventHanding":
        """
        绑定事件

        :param name: 事件名称，没有则创建
        :param func: 绑定函数
        :param add: 是否在绑定的事件后添加，而不是清除其他事件只保留自己
        :return: self
        """
        if name not in self.evts:
            self.evts[name] = [func]
        if add:
            self.evts[name].append(func)
        else:
            self.evts[name] = [func]
        return self

    def unbind(self, name, func):
        """
        解绑事件

        -> 后续事件将以ID作为识别码来解绑

        :param name: 事件名称
        :param func: 要解绑函数
        :return:
        """
        self.evts[name].remove(func)


class Event:

    """
    用于传递事件的参数
    """

    def __init__(self, x: int = None, y: int = None, rootx: int = None, rooty: int = None, key: int = None):
        """
        初始化

        :param x: 鼠标的/组建的X坐标(相对于窗口)
        :param y: 鼠标的/组建的Y坐标(相对于窗口)
        :param rootx: 鼠标的/组建的X坐标(相对于屏幕)
        :param rooty: 鼠标的/组建的Y坐标(相对于屏幕)
        """
        self.x = x
        self.y = y
        self.rootx = rootx
        self.rooty = rooty
        self.key = key
