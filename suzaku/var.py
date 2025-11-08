import typing

from .event import SkEvent, SkEventHandling


class SkVar(SkEventHandling):
    """Similar to Tkinter's `Var`, it is used for data transfer and synchronization.
    【类似与tkinter的Var，用于数据传递、同步】

    Args:
        default_value: The initial _value of the variable.【初始值】
        value_type: The type of the variable.【数据类型】
    """

    _instance = 0

    def __init__(self, default_value=None, value_type: type | typing.Any = typing.Any):
        super().__init__()
        self.id = self.__class__.__name__ + str(self._instance + 1)
        SkVar._instance += 1
        # self.bindedtasks = {"change": {}}
        self.EVENT_TYPES = ["change"]
        self._value: type = default_value if default_value is not None else value_type()
        self._value_type: type = value_type

    def set(self, value: typing.Any) -> typing.Self:
        """
        Set the _value of the data, which will then trigger a `change` event.
        【设置数据的值，之后会触发change事件】

        Args:
            value: The new _value of the variable.

        Returns:
            None
        """
        if not type(value) is self._value_type:
            raise ValueError(f"Value must be {self._value_type}")
        if self._value != value:
            self._value = value
            self.trigger(f"change", SkEvent(self, "change", value=value))
        return self

    def get(self) -> typing.Any:
        """
        Get the _value of the variable.【获取数据值】

        :rtype: typing.Any
        :return: The _value of the data.
        """
        return self._value


class SkStringVar(SkVar):
    """Only records values of type `str`.【只记录类型为str的值】"""

    def __init__(self, default_value: str = ""):
        super().__init__(default_value, str)


class SkIntVar(SkVar):
    """Only records values of type `int`.【只记录类型为int的值】"""

    def __init__(self, default_value: int = 0):
        super().__init__(default_value, int)


class SkBooleanVar(SkVar):
    """Only records values of type `bool`.【只记录类型为bool的值】"""

    def __init__(self, default_value: bool = False):
        super().__init__(default_value, bool)


class SkFloatVar(SkVar):
    """Only records values of type `float`.【只记录类型为float的值】"""

    def __init__(self, default_value: float = 0.0):
        super().__init__(default_value, float)
