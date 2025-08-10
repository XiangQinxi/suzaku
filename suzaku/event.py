from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union

from .after import SkAfter


class SkEventHanding(SkAfter):
    def __init__(self):
        """SkEvent binding manager."""

        self.events: dict[str, dict[str, Callable]] = {}

    def event_generate(self, name: str, *args, **kwargs) -> Union[bool, Any]:
        """Send event signal.

        :param name: Event name.
        :param args: Event arguments.
        :param kwargs: Event keyword arguments.
        :return: self
        """

        if not name in self.events:
            self.events[name] = {}

        for event in self.events[name].values():
            event(*args, **kwargs)

        return self

    def bind(self, name: str, func: callable, add: bool = True) -> str:
        """Bind event.

        :param name: Event name.
        :param func: Event function.
        :param add: Whether to add after existed events, otherwise clean other and add itself.
        :return: Event ID
        """
        if name not in self.events:  # Create a new event
            self.events[name] = {}
        _id = func.__name__ + "." + str(len(self.events[name]) + 1)
        if add:
            self.events[name][_id] = func
        else:
            self.events[name] = {_id: func}
        return _id

    def unbind(self, name: str, _id: str) -> None:
        """Unbind event.

        :param name: Event name.
        :param _id Event ID.
        :return: None
        """
        del self.events[name][_id]


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
