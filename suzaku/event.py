from __future__ import annotations as _

import threading
import time
import typing
import warnings
from dataclasses import dataclass

# import re

if typing.TYPE_CHECKING:
    from .widgets import SkWidget, SkWindow


class SkBindedTask:
    """A class to represent binded task when a event is triggered."""

    def __init__(
        self,
        id_: str,
        target: typing.Callable,
        multithread: bool = False,
        _keep_at_clear: bool = False,
    ):
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


class SkDelayTask(SkBindedTask):
    """A class to represent delay tasks"""
    def __init__(self, id_: str, target: typing.Callable, delay_, *args, **kwargs):
        """Inherited from SkBindedTask, used to store tasks binded to `delay` events.
        
        :param delay: Time to delay, in seconds, indicating how log to wait before the task is 
                      executed.
        """
        SkBindedTask.__init__(self, id_, target, *args, **kwargs) # For other things,same as 
                                                                  # SkBindedTask
        self.target_time = float(time.time()) + delay_ # To store when to execute the task

class SkRepeatTask(SkBindedTask):
    """A class to represent repeat tasks"""
    def __init__(self, id_: str, target: typing.Callable, interval, *args, **kwargs):
        """Inherited from SkBindedTask, used to store tasks binded to `repeat` events.
        
        :param delay: Time to delay, in seconds, indicating how log to wait before the task is 
                      executed.
        """
        SkBindedTask.__init__(self, id_, target, *args, **kwargs) # For other things,same as 
                                                                  # SkBindedTask
        self.target_time = float(time.time()) + interval # To store when to execute the task for 
                                                         # the next time, will be accumulated after 
                                                         # execution of the task
        self.interval = interval # Interval of the class

class SkEventHandling:
    """A class containing event handling abilities.

    This class should be inherited by other classes with such abilities.

    Events should be represented in the form of `event_type` or `event_type[args]`. e.g. `delay` or
    `delay[500]`
    """

    EVENT_TYPES: list[str] = [
        "resize", "move", "configure", "update", 
        "mouse_move", "mouse_enter", "mouse_leave", "mouse_press", "mouse_release", 
        "focus_gain", "focus_loss", 
        "key_press", "key_release", "key_repeat", 
        "char", "click", 
        "delay", "repeat", # This row shows special event type(s)
    ]
    multithread_tasks: list[tuple[SkBindedTask, SkEvent]] = []
    WORKING_THREAD: threading.Thread
    instance_count = 0

    @classmethod
    def _working_thread_loop(cls):
        while True:
            cls.multithread_tasks[0][0].target(cls.multithread_tasks[0][1])
            cls.multithread_tasks.pop(0)

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
        self.delay_tasks: list[SkDelayTask] = []
        # Make a initial ID here as it will be needed anyway even if the object does not have an ID.
        self.id = f"{self.__class__.__name__}{self.__class__.instance_count}"
        ## Initialize tasks list
        for event_type in self.__class__.EVENT_TYPES:
            self.tasks[event_type] = []
        ## Accumulate instance count
        self.__class__.instance_count += 1
        # Event binds
        self.bind(
            "update", self._check_delay_events, _keep_at_clear=True
        )  # Delay checking loop

    def parse_event_type_str(self, event_type_str) -> dict:
        """This function parses event type string.

        :param event_type_str: The event type string to be parsed
        :returns: json, parsed event type
        """
        event_type = event_type_str.split("[")[0]  # To be changed
        if len(event_type_str.split("[")) > 1:
            params = event_type_str.split("[")[1][0:-1].split(",")
        else:
            params = []
        NotImplemented  # The prvious lines are to be changed as they r soooo frickin' shitty
        return {event_type: params}

    def execute_task(
        self, task: SkBindedTask | SkDelayTask, event_obj: SkEvent | None = None
    ):
        """To execute a task

        Example
        -------
        .. code-block:: python
            my_task = SkWidget.bind("delay[5]", lambda: print("Hello Suzaku"))
            SkWidget.execute_task(my_task)
        """
        if event_obj == None:
            event_obj = SkEvent()
        assert event_obj is not None
        if event_obj.widget == None:
            event_obj.widget = self
        if not task.multithread:
            # If not multitask, execute directly
            task.target(event_obj)
            # If is a delay event, it should be removed right after execution
            if isinstance(task, SkDelayTask):
                self.unbind(task)
        else:
            # Otherwise add to multithread tasks list and let the working thread to deal with it
            # If is a delay task, should add some code to let it unbind itself, here is a way, 
            # which is absolutely not perfect, though works, to implemet this machanism, by 
            # overriding its target with a modified version
            def self_destruct_template(task, event_obj):
                task.target(event_obj)
                self.unbind(task)
            if isinstance(task, SkDelayTask):
                task.target = lambda event_obj: self_destruct_template(task, event_obj)
            SkEventHandling.multithread_tasks.append((task, event_obj))

    def trigger(self, event_type: str, event_obj: SkEvent | None = None) -> None:
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
        # Parse event type string
        parsed_event_type = self.parse_event_type_str(event_type)
        # Create a default SkEvent object if not soecified
        if event_obj == None:
            event_obj = SkEvent(
                widget=self, event_type=list(parsed_event_type.keys())[0]
            )
        # Add the event to event lists (the widget itself and the global list)
        self.events.append(event_obj)
        SkEvent.global_list.append(event_obj)
        # Find targets
        targets = []
        targets.append(event_type)
        if list(parsed_event_type.values())[0] in ["", "*"]:
            # If match all
            targets.append(list(parsed_event_type.keys())[0])
            targets.append(list(parsed_event_type.keys())[0] + "[*]")
        for target in targets:
            if target in self.tasks:
                for task in self.tasks[target]:
                    # To execute all tasks binded under this event
                    self.execute_task(task, event_obj)

    def bind(
        self,
        event_type: str,
        target: typing.Callable,
        multithread: bool = False,
        _keep_at_clear: bool = False,
    ) -> SkBindedTask | bool:
        """To bind a task to the object when a specific type of event is triggered.

        Example
        -------
        .. code-block
            my_button = SkButton(...).pack()
            press_down_event = my_button.bind("mouse_press", lambda _: print("Hello world!"))
        This shows binding a hello world to the button when it's press.

        :param event_type: The type of event to be binded to
        :param target: A callable thing, what to do when this task is executed
        :param multithread: If this task should be executed in another thread (False by default)
        :param _keep_at_clear: If the task should be kept when clearning the event's binding
        :return: SkBindedTask that is binded to the task if success, otherwise False
        """
        parsed_event_type = self.parse_event_type_str(event_type)
        if list(parsed_event_type.keys())[0] not in self.__class__.EVENT_TYPES:
            # warnings.warn(f"Event type {event_type} is not present in {self.__class__.__name__}, "
            #                "so the task cannot be binded as expected.")
            # return False
            self.EVENT_TYPES.append(event_type)
        if event_type not in self.tasks:
            self.tasks[event_type] = []
        task_id = f"{self.id}.{event_type}.{len(self.tasks[event_type])}"
        # e.g. SkButton114.focus_gain.514 / SkEventHandling114.focus_gain.514
        match list(parsed_event_type.keys())[0]:
            case "delay":
                task = SkDelayTask(
                    task_id,
                    target,
                    float(parsed_event_type["delay"][0]),
                    multithread,
                    _keep_at_clear,
                )
                self.delay_tasks.append(task)
            case "repeat":
                NotImplemented
            case _: # All normal event types
                task = SkBindedTask(task_id, target, multithread, _keep_at_clear)
        self.tasks[event_type].append(task)
        return task

    def find_task(self, task_id: str) -> SkBindedTask | bool:
        """To find a binded task using task ID.

        Example
        -------
        .. code-block:: python
            my_button = SkButton(...)
            press_task = my_button.find_task("SkButton114.mouse_press.514")
        This shows getting the `SkBindedTask` object of task with ID `SkButton114.mouse_press.514`
        from binded tasks of `my_button`.

        :return: The SkBindedTask object of the task, or False if not found
        """
        task_id_parsed = task_id.split(".")
        for task in self.tasks[task_id_parsed[1]]:
            if task.id == task_id:
                return task
        else:
            return False

    def unbind(self, target_task: str | SkBindedTask) -> bool:
        """To unbind the task with specified task ID.

        Example
        -------
        .. code-block:: python
            my_button = SkButton(...)
            my_button.unbind("SkButton114.mouse_press.514")
        This show unbinding the task with ID `SkButton114.mouse_press.514` from `my_button`.

        .. code-block:: python
            my_button = SkButton(...)
            my_button.unbind("SkButton114.mouse_press.*")
            my_button.unbind("mouse_release.*")
        This show unbinding all tasks under `mouse_press` and `mouse_release` event from 
        `my_button`.

        :param target_task: The task ID or `SkBindedTask` to unbind.
        :return: If success
        """
        match target_task:
            case str():
                task_id_parsed = target_task.split(".")
                if len(task_id_parsed) == 2:
                    task_id_parsed.insert(0, self.id)
                if task_id_parsed != self.id:
                    NotImplemented
                for task_index, task in enumerate(self.tasks[task_id_parsed[1]]):
                    if task.id == target_task:
                        self.tasks[task_id_parsed[1]].pop(task_index)
                        return True
                else:
                    return False
            case SkBindedTask():
                for event_type in self.tasks:
                    if target_task in self.tasks[event_type]:
                        self.tasks[event_type].remove(target_task)
                        return True
                else:
                    return False
            case _:
                warnings.warn("Wrong type for unbind()! Must be event ID or task object", 
                              UserWarning)
                return False

    def _check_delay_events(self, _=None) -> None:
        """To check and execute delay events.

        Example
        -------
        Mostly used by SkWidget.update(), which is internal use
        """
        # print("Checking delayed events...")
        for task in self.delay_tasks:
            if float(time.time()) >= task.target_time:
                # print(f"Current time is later than target time of {task.id}, execute the task.")
                self.execute_task(task)


# Initialize working thread
SkEventHandling.WORKING_THREAD = threading.Thread(
    target=SkEventHandling._working_thread_loop
)


# @dataclass
class SkEvent:
    """Used to represent an event."""

    global_list: list[SkEvent] = []

    def __init__(
        self,
        widget: SkEventHandling | None = None,
        event_type: str = "[Unspecified]",
        **kwargs,
    ):
        """This class is used to represent events.

        Some properties owned by all types of events are stored as attributes, such as widget and type.
        Others are stored as items, which can be accessed or manipulated just like dict, e.g.
        `SkEvent["x"]` for get and `SkEvent["y"] = 16` for set.

        Example
        -------
        Included in descrepsion.

        :param widget: The widget of the event, None by default
        :param event_type: Type of the event, in string, `"[Unspecified]"` by default
        :param **kwargs: Other properties of the event, will be added as items
        """
        self.event_type: str = event_type  # Type of event
        self.widget: typing.Optional[typing.Any] = widget  # Relating widget
        self.window_base: typing.Optional[typing.Any] = (
            None  # WindowBase of the current window
        )
        self.window: typing.Optional[typing.Any] = None  # Current window
        self.event_data: dict = {}
        # Not all proprties above will be used
        # Update stuff from args into attributes
        for prop in kwargs.keys():
            if prop not in ["widget", "event_type"]:
                # self.__setattr__(prop, kwargs[prop])
                self[prop] = kwargs[prop]

    def __setitem__(self, key: str, value: typing.Any):
        self.event_data[key] = value

    def __getitem__(self, key: str) -> typing.Any:
        if key in self.event_data:
            return self.event_data[key]
        else:
            return None  # If no such item avail, returns None
