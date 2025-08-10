from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union

from .after import SkAfter


class SkEventHanding(SkAfter):
    """SkEvent binding manager."""

    events: dict[str, dict[str, dict[str, Callable]]] = {}

    # events = { widget_id : { event_name : { event_id : event_func } } }

    def init_events(self, dict):
        self.events[self.id] = dict

    def event_generate(self, name: str, *args, **kwargs) -> Union[bool, Any]:
        """Send event signal.

        :param name: Event name.
        :param args: Event arguments.
        :param kwargs: Event keyword arguments.
        :return: self
        """

        if not self.id in self.events:  # Auto create widget events
            self.events[self.id] = {}
        if not name in self.events[self.id]:  # Auto create widget`s event
            self.events[self.id][name] = {}

        for event in self.events[self.id][name].values():
            event(*args, **kwargs)

        return self

    def bind(self, name: str, func: callable, add: bool = True) -> str:
        """Bind event.

        :param name: Event name.
        :param func: Event function.
        :param add: Whether to add after existed events, otherwise clean other and add itself.
        :return: Event ID
        """
        if self.id not in self.events:  # Create widget events
            self.events[self.id] = {}
        if name not in self.events[self.id]:  # Create a new event
            self.events[self.id][name] = {}
        _id = name + "." + str(len(self.events[self.id][name]) + 1)  # Create event ID

        if add:
            self.events[self.id][name][_id] = func
        else:
            self.events[self.id][name] = {_id: func}
        return _id

    def unbind(self, name: str, _id: str) -> None:
        """Unbind event.

        :param name: Event name.
        :param _id Event ID.
        :return: None
        """
        del self.events[self.id][name][_id]  # Delete event


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
