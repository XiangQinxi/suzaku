from .event import EventHanding


class Var(EventHanding):
    def __init__(self, default_value, typ: type = any):
        """Store and share values.

        * default_value: Initial value
        """

        super().__init__()
        self.evts = {
            "change": []
        }
        self.value: type = default_value
        self.type = typ

    def set(self, value: any) -> None:
        """Set the value and generate a 'change' event.

        * value: New value
        """
        if not type(value) is self.type:
            raise ValueError(f"Value must be {self.type}")
        self.value = value
        self.event_generate("change", value)
        return None

    def get(self) -> any:
        """Get the value."""
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
