from .event import EventHanding


class Var(EventHanding):
    def __init__(self, default_value, typ: type = any):
        """
        存储、共享数值。

        Args:
            default_value: 初始值
        """

        super().__init__()
        self.evts = {
            "change": []
        }
        self.value: type = default_value
        self.type = typ

    def set(self, value: any) -> None:
        """
        设置值，并创建change事件。

        Args:
            value: 新值

        Returns:

        """
        if not type(value) is self.type:
            raise ValueError(f"Value must be {self.type}")
        self.value = value
        self.event_generate("change", value)
        return None

    def get(self) -> any:
        """
        获取值。

        Returns:
            any: 值
        """
        return self.value


class StringVar(Var):
    def __init__(self, default_value: str = ""):
        super().__init__(default_value, str)


class IntVar(Var):
    def __init__(self, default_value: int = 0):
        super().__init__(default_value, int)


class BooleanVar(Var):
    def __init__(self, default_value: bool = False):
        super().__init__(default_value, bool)


class FloatVar(Var):
    def __init__(self, default_value: float = 0.0):
        super().__init__(default_value, float)
