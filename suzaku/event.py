import typing
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union

from .after import SkAfter


class SkEventHanding(SkAfter):
    """SkEvent binding manager.【事件绑定管理器】"""

    events: dict[str, dict[str, dict[str, Callable]]] = {}

    # events = { widget_id : { event_name : { event_id : event_func } } }

    def init_events(self, events_dict: dict[str, dict[str, Callable]]) -> typing.Self:
        """Init current class events.
        【初始化当前类的事件】

        Under normal circumstances, it should be called during component initialization. In other cases, it is recommended to use `event_generate`.
        【一般情况下，需要在组件初始化时调用，除此情况下，建议用event_generate】

        .. code-block:: python
            self.init_events(
                {
                    "click": {},
                }
            )

        :param dict[str, dict[str, Callable]] events_dict: Event dict.
        :return: None
        """
        self.events[self.id] = events_dict
        return self

    def event_generate(self, name: str) -> typing.Self:
        """Create a new event type.【创建一个新的事件类型】

        >>> self.event_generate("click")

        :param str name: Event name.【事件名】
        :return: self.
        """

        if not self.id in self.events:  # Auto create widget events
            self.events[self.id] = {}  # Create widget events
        if not name in self.events[self.id]:  # Auto create widget`s event
            self.events[self.id][name] = {}  # Create widget`s event

        return self

    def event_trigger(self, name: str, *args, **kwargs) -> Union[bool, Any]:
        """Send the event signal of the corresponding event type
        (trigger the corresponding event)

        【发送对应事件类型的事件信号（触发对应事件）】

        Generally, the event name is followed by "SkEvent" to pass data. Of course,
        for custom events, parameters can also be passed directly.

        【一般事件名后接SkEvent，用于传递数据。当然如果是自定义事件，也可以直接传递参数。】

        >>> self.event_trigger("click", SkEvent(event_type="click"))
        >>> self.event_trigger("custom_event", "custom_data")

        :param name: Event name.【事件名】
        :param args: Event arguments.【事件参数】
        :param kwargs: Event keyword arguments.【事件关键字参数】
        :return: self.
        """

        if self.id in self.events and name in self.events[self.id]:
            for event in self.events[self.id][name].values():
                event(*args, **kwargs)
        else:
            raise ValueError(f"Widget {self.id} Event {name} not found.")

        return self

    def bind(self, name: str, func: callable, add: bool = True) -> str:
        """Bind an event.【绑定事件】

        :param name: Event name.【事件名】
        :param func: Event function.【事件函数】
        :param add: Whether to add after existed events, otherwise clean other and add itself.【是否在已存在事件后添加，否则清理其他事件并添加本身】
        :return: Event ID.【事件ID】
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

    event_bind = bind

    def unbind(self, name: str, _id: str) -> None:
        """Unbind an event with event ID.【解绑事件】

        :param name: Event name.【事件名】
        :param _id Event ID.【事件ID】
        :return: None.【无返回值】
        """
        del self.events[self.id][name][_id]  # Delete event

    event_unbind = unbind


@dataclass
class SkEvent:
    """
    Used to pass event via arguments.

    【用于传递事件的参数。】
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
    dpi_scale: Optional[float] = None
