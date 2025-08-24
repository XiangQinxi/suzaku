import typing
import threading
import warnings
from dataclasses import dataclass


class SkBindedTask():
    """A class to represent binded task when a event is triggered."""
    def __init__(self, id_: str, target: typing.Callable, multithread: bool=False, 
                 _keep_at_clear: bool=False):
        """Each object is to represent a task binded to the event.

        Example
        -------
        This is mostly for internal use of suzaku.
        .. code-block:: python
            class SkEventHandling():
                def bind(self, ...):
                    ...
                    task = SkBindedTask(event_id, target, multithread, _keep_at_clear)
                    ...
        This shows where this class is used for storing task properties in most cases.

        :param id_: The task id of this task
        :param target: A callable thing, what to do when this task is executed
        :param multithread: If this task should be executed in another thread (False by default)
        :param _keep_at_clear: If the task should be kept when clearning the event's binding
        """
        self.id: str = id_
        self.target: typing.Callable = target
        self.multithread: bool = multithread
        self.keep_at_clear: bool = _keep_at_clear


class SkEventHandling():
    """A class containing event handling abilities.
    
    This class should be inherited by other classes with such abilities.
    """

    EVENT_TYPES: list[str] = [
        "resize", "move", "configure", "update", 
        "mouse_move", "mouse_enter", "mouse_leave", "mouse_press", "mouse_release", 
        "focus_gain", "focus_loss", 
        "key_press", "key_release", "key_repeat", 
        "char", "click", 
        "after", 
    ]
    multithread_tasks: list[SkBindedTask] = []
    WORKING_THREAD: threading.Thread
    instance_count = 0

    @classmethod
    def _working_thread_loop(cls):
        return [task.target() for task in cls.multithread_tasks]

    def __init__(self):
        """A class containing event handling abilities.
        
        Example
        -------
        This is mostly for internal use of suzaku.
        .. code-block:: python
            class SkWidget(SkEventHandling, ...):
                def __init__(self):
                    super().__init__(self)
            ...
        This shows subclassing SkEventHandling to let SkWidget gain the ability of handling events.
        """
        self.events: list = []
        self.tasks: dict[str, list[SkBindedTask]] = {}
        # Make a initial ID here as it will be needed anyway even if the object does not have an ID.
        self.id = f"{self.__class__.__name__}{self.__class__.instance_count}"
        ## Initialize tasks list
        for event_type in self.__class__.EVENT_TYPES:
            self.tasks[event_type] = []
        ## Accumulate instance count
        self.__class__.instance_count += 1
    
    def trigger(self, event_type: str) -> None:
        """To trigger a type of event

        Example
        -------
        .. code-block:: python
            class SkWidget(SkEventHandling, ...):
                ...
            
            my_widget = SkWidget()
            my_widget.trigger("mouse_press")
        This shows triggering a `mouse_press` event in a `SkWidget`, which inherited `SkEventHandling` so has the 
        ability to handle events.
        
        :param event_type: The type of event to trigger
        """
        for task in self.tasks[event_type]:
            # Add the Event object to the global list
            NotImplemented
            # To execute all tasks binded under this event
            if not task.multithread:
                # If not multitask, execute dirctly
                task.target()
            else:
                # Otherwise add to multithread tasks list and let the working thread to deal with it
                SkEventHandling.multithread_tasks.append(task)
    
    def bind(self, event_type: str, target: typing.Callable, 
             multithread: bool, _keep_at_clear: bool) -> bool:
        """To bind a task to the object when a specific type of event is triggered.

        Example
        -------
        .. code-block
        
        :param event_type: The type of event to be binded to
        :param target: A callable thing, what to do when this task is executed
        :param multithread: If this task should be executed in another thread (False by default)
        :param _keep_at_clear: If the task should be kept when clearning the event's binding
        :return: If success
        """
        if event_type not in self.__class__.EVENT_TYPES:
            warnings.warn(f"Event type {event_type} is not present in {self.__class__.__name__}, "
                           "so the task cannot be binded as expected.")
            return False
        event_id = f"{self.id}.{event_type}.{len(self.tasks[event_type])}"
        # e.g. SkButton114.focus_gain.514 / SkEventHandling114.focus_gain.514
        task = SkBindedTask(event_id, target, multithread, _keep_at_clear)


# Initialize working thread
SkEventHandling.WORKING_THREAD = threading.Thread(target = SkEventHandling._working_thread_loop)

class SkEventHandingOld:
    """SkEvent binding manager.【事件绑定管理器】"""

    _afters = {}
    _after = 0

    def __init__(self):
        # events = { event_name : { event_id : [event_func, whether_to_use_multithreading] } }
        self.events: dict[str, dict[str, list[typing.Callable | bool]]] = {}
        warnings.warn("Old SkEventHanlding class will be deprecated.", DeprecationWarning)

    def event_generate(self, name: str) -> typing.Self:
        """Create a new event type.【创建一个新的事件类型】

        >>> self.event_generate("click")

        :param str name: Event name.【事件名】
        :return: self.
        """

        if not name in self.events:  # Auto create widget`s event
            self.events[name] = dict()  # Create widget`s event
        else:
            warnings.warn(f"Widget {self.id}, Event {name} already exists.")

        return self

    def event_trigger(self, name: str, *args, **kwargs) -> bool | typing.Any:
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

        if name in self.events:
            for event in self.events[name].values():
                if event[1] is True:
                    threading.Thread(target=event[0], args=args, kwargs=kwargs).start()
                else:
                    event[0](*args, **kwargs)
        else:
            raise ValueError(f"Widget {self.id}, Event {name} not found.")

        return self

    # 我也是服了，我不小心将allow_multi的默认值从False改为True，导致创建新窗口时老是报错，
    def bind(
        self,
        name: str,
        func: typing.Callable,
        *,
        add: bool = True,
        allow_multi: bool = False,
    ) -> str:
        """Bind an event.【绑定事件】

        :param name: Event name.【事件名】
        :param func: Event function.【事件函数】
        :param add: Whether to add after existed events, otherwise clean other and add itself.【是否在已存在事件后添加，否则清理其他事件并添加本身】
        :param allow_multi: Whether to allow multiple threads to run the event function at the same time.【是否允许多个线程同时运行事件函数】
        :return: Event ID.【事件ID】
        """
        if name not in self.events:
            raise ValueError(f"Widget {self.id}, Event {name} not found.")
        _id = name + "." + str(len(self.events[name]) + 1)  # Create event ID

        if add:
            self.events[name][_id] = (func, allow_multi)
        else:
            self.events[name] = {_id: (func, allow_multi)}
        return _id

    event_bind = bind

    def unbind(self, name: str, _id: str) -> None:
        """Unbind an event with event ID.【解绑事件】

        :param name: Event name.【事件名】
        :param _id Event ID.【事件ID】
        :return: None.【无返回值】
        """
        del self.events[name][_id]  # Delete event

    event_unbind = unbind

    def after(
        self,
        s: int | float,
        func: typing.Callable,
        *,
        allow_multi: bool = False,
        post: bool = False,
    ) -> str | threading.Timer:
        """Execute a function after a delay (an ID will be provided in the future for unbinding).

        :param s: Delay in seconds
        :param func: Function to execute after delay
        :param allow_multi: Whether to allow multiple threads to run the function at the same time.
        :param post: Whether to execute the `post()` method after the method ends

        :return: ID of the timer
        """

        if allow_multi:
            timer = threading.Timer(s, func)
            timer.start()
            return timer

        _id = "after." + str(self._after)

        self._afters[_id] = [self.time() + s, func, post]
        self._after += 1
        return _id

    def after_cancel(self, _id: str) -> typing.Self:
        """Cancel a timer.

        :param _id: ID of the timer
        """
        if _id in self._afters:
            del self._afters[_id]

        return self


from typing import Any, List, Optional, Union


@dataclass
class SkEvent:
    """
    Used to pass event via arguments.

    【用于传递事件的参数。】
    """

    event_type: str  # 【事件类型】
    x: Optional[int] = None  # 【x轴坐标】
    y: Optional[int] = None  # 【y轴坐标】
    rootx: Optional[int] = None  # 【相对x轴坐标】
    rooty: Optional[int] = None  # 【相对y轴坐标】
    key: Union[int, str, None] = None  # 【键盘按键】
    keyname: Optional[str] = None  # 【键盘按键名】
    mods: Optional[str] = None  # 【修饰键名】
    mods_key: Optional[int] = None  # 【修饰键值】
    char: Optional[str] = None  # 【输入文本值】
    width: Optional[int] = None  # 【宽度】
    height: Optional[int] = None  # 【高度】
    widget: Any = None  # 【事件组件】
    maximized: Optional[bool] = None  # 【窗口是否最大化】
    paths: Optional[List[str]] = None
    #  The file path passed in when the window triggers the `drop` event
    #  【窗口触发drop事件传入的文件路径】
    iconified: Optional[bool] = None  # 【窗口是否最小化】
    dpi_scale: Optional[float] = None  # 【DPI缩放】
    glfw_window: Optional[typing.Any] = None  # 【glfw窗口】
    window: Optional[typing.Any] = None  # 【SkWindow窗口】
    button: typing.Literal[0, 1, 2] = None
    # The provided values are: 0 for left button, 1 for right button, and 2 for middle button.
    # 【给出的值0为左键，1为右键，2为中键】
    x_offset: Optional[float] = None  # 【鼠标滚轮水平滚动偏移量】
    y_offset: Optional[float] = None  # 【鼠标滚轮垂直滚动偏移量】
