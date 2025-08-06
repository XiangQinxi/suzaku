from suzaku.event import SkEventHanding


class SkVar(SkEventHanding):
    def __init__(self, default_value, value_type: type = any):
        """
        Save a variable.

        Args:
            default_value: The initial value of the variable.
            value_type: The type of the variable.
        """

        super().__init__()
        self.events = {"change": []}
        self.value: type = default_value
        self.value_type = value_type

    def set(self, value: any) -> None:
        """
        Set the value of the variable.

        Args:
            value: The new value of the variable.

        Returns:
            None
        """
        if not type(value) is self.value_type:
            raise ValueError(f"Value must be {self.value_type}")
        self.value = value
        self.event_generate("change", value)
        return None

    def get(self) -> any:
        """
        Get the value of the variable.

        Returns:
            any: The value of the variable.
        """
        return self.value


class SkStringVar(SkVar):
    def __init__(self, default_value: str = ""):
        super().__init__(default_value, str)


class SkIntVar(SkVar):
    def __init__(self, default_value: int = 0):
        super().__init__(default_value, int)


class SkBooleanVar(SkVar):
    def __init__(self, default_value: bool = False):
        super().__init__(default_value, bool)


class SkFloatVar(SkVar):
    def __init__(self, default_value: float = 0.0):
        super().__init__(default_value, float)
