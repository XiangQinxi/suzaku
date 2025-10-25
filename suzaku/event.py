from __future__ import annotations as _

import threading
import time
import typing
import warnings
import collections.abc
# from dataclasses import dataclass

# import re

# if typing.TYPE_CHECKING:
#     from .widgets import SkWidget, SkWindow


# [TODO] Implementation of clear_bind() and keep_at_clear
# [TODO] Implementation of repeat events
# [TODO] Rewrite event type string parsing
# [TODO] Fix a type error in SkEventHandling.bind()
# [TODO] Support unbind for another widget's event

class SkBoundTask:
    """A class to represent bound task when a event is triggered."""

    def __init__(
        self,
        id_: str,
        target: typing.Callable | typing.Iterable,
        multithread: bool = False,
        _keep_at_clear: bool = False,
    ):
        """Each object is to represent a task bound to the event.

        Example
        -------
        This is mostly for internal use of suzaku.
        .. code-block:: python
            class SkEventHandling():
                def bind(self, ...):
                    ...
                    task = SkBoundTask(event_id, target, multithread, _keep_at_clear)
                    ...
        This shows where this class is used for storing task properties in most cases.

        :param id_: The task id of this task
        :param target: A callable thing, what to do when this task is executed
        :param multithread: If this task should be executed in another thread (False by default)
        :param _keep_at_clear: If the task should be kept when cleaning the event's binding
        """
        self.id: str = id_
        self.target: typing.Callable | typing.Iterable = target
        self.multithread: bool = multithread
        self.keep_at_clear: bool = _keep_at_clear


class SkDelayTask(SkBoundTask):
    """A class to represent delay tasks"""

    def __init__(self, id_: str, target: typing.Callable, delay_, *args, **kwargs):
        """Inherited from SkBoundTask, used to store tasks bound to `delay` events.

        :param delay: Time to delay, in seconds, indicating how log to wait before the task is
                      executed.
        """
        SkBoundTask.__init__(
            self, id_, target, *args, **kwargs
        )  # For other things,same as
        # SkBoundTask
        self.target_time = (
            float(time.time()) + delay_
        )  # To store when to execute the task


class SkRepeatTask(SkBoundTask):
    """A class to represent repeat tasks"""

    def __init__(self, id_: str, target: typing.Callable, interval, *args, **kwargs):
        """Inherited from SkBoundTask, used to store tasks bound to `repeat` events.

        :param delay: Time to delay, in seconds, indicating how log to wait before the task is
                      executed.
        """
        SkBoundTask.__init__(
            self, id_, target, *args, **kwargs
        )  # For other things,same as
        # SkBoundTask
        self.target_time = (
            float(time.time()) + interval
        )  # To store when to execute the task for
        # the next time, will be accumulated after
        # execution of the task
        self.interval = interval  # Interval of the task


class SkEventHandling:
    """A class containing event handling abilities.

    This class should be inherited by other classes with such abilities.

    Events should be represented in the form of `event_type` or `event_type[args]`. e.g. `delay` or
    `delay[500]`
    """
    
    # fmt: off
    EVENT_TYPES: list[str] = [
        "resize", "move", 
        "configure", "update", "redraw", 
        "mouse_move", "mouse_enter", "mouse_leave", "mouse_press", "mouse_release", "click", 
        "focus_gain", "focus_loss", 
        "key_press", "key_release", "key_repeat", "char", 
        "delay", "repeat", # This row shows special event type(s)
    ]
    # fmt: on
    multithread_tasks: list[tuple[SkBoundTask, SkEvent]] = []
    WORKING_THREAD: threading.Thread
    instance_count = 0

    @classmethod
    def _working_thread_loop(cls):
        while True:
            try:
                SkEventHandling._execute_task(cls.multithread_tasks[0][0], 
                                              cls.multithread_tasks[0][1])
                # For line above: [0][0] is task object, [0][1] is SkEvent object
            except Exception as e:
                warnings.warn(RuntimeWarning("Error in multithread suzaku-event-bound task "
                                            f"with ID {cls.multithread_tasks[0][0].id}, "
                                            f"detailed error info: \"{str(e)}\". "
                                             "The working thread will head to the next task "
                                             "(skipping current causing the error)."))
            cls.multithread_tasks.pop(0) # Executed tasks should be removed, anyway

            if not cls.multithread_tasks:
                time.sleep(0.01)  # Avoid CPU draining while no tasks avail
                continue
            
            # # Codes below written by AI, will be removed as same fixes already been made to 
            # # current codes manually.
            # try:
            #     task, event_obj = cls.multithread_tasks[0]
            #     task.target(event_obj)
            #     cls.multithread_tasks.pop(0)
            # except Exception as e:
            #     # 即使任务执行失败，也要从队列中移除，防止队列堵塞
            #     if cls.multithread_tasks:
            #         failed_task = cls.multithread_tasks.pop(0)
            #         warnings.warn(
            #             f"Multithread task failed and removed: {failed_task[0].id}, error: {e}"
            #         )

    @staticmethod
    def _execute_task(task: SkBoundTask, event_obj: SkEvent) -> None:
        """To execute the binded task directly, regardless its props, mainly for internal use."""
        match task.target:
            case _ if callable(task.target):
                task.target(event_obj)
            case _ if isinstance(task.target, collections.abc.Iterable):
                for task_step in task.target:
                    task_step(event_obj)
            case _:
                raise ValueError("Error type for suzaku task target! Excepted callable or "
                                f"iterable but received {type(task.target)}")

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
        self.tasks: dict[str, list[SkBoundTask]] = {}
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
        NotImplemented  # The previous lines are to be changed as they r soooo frickin' shitty
        return {event_type: params}

    def execute_task(
        self, task: SkBoundTask, event_obj: SkEvent | None = None
    ):
        """To execute a task

        Example
        -------
        .. code-block:: python
            my_task = SkWidget.bind("delay[5]", lambda: print("Hello Suzaku"))
            SkWidget.execute_task(my_task)
        """
        if event_obj is None:
            event_obj = SkEvent()
        assert event_obj is not None
        if event_obj.widget is None:
            event_obj.widget = self
        if not task.multithread:
            # If not multitask, execute directly
            SkEventHandling._execute_task(task, event_obj)
            # If is a delay event, it should be removed right after execution
            if isinstance(task, SkDelayTask):
                self.unbind(task)
        else:
            # Otherwise add to multithread tasks list and let the working thread to deal with it
            # If is a delay task, should add some code to let it unbind itself, here is a way,
            # which is absolutely not perfect, though works, to implement this mechanism, by
            # overriding its target with a modified version
            def self_destruct_template(task, event_obj):
                SkEventHandling._execute_task(task, event_obj)
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
        # Create a default SkEvent object if not specified
        if event_obj == None:
            event_obj = SkEvent(
                widget=self, event_type=list(parsed_event_type.keys())[0]
            )
        # Add the event to event lists (the widget itself and the global list)
        self.events.append(event_obj)
        SkEvent.latest = event_obj
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
                    # To execute all tasks bound under this event
                    self.execute_task(task, event_obj)

        """
        parsed_event_type = self.parse_event_type_str(event_type)
        # Create a default SkEvent object if not specified
        if event_obj is None:
            event_obj = SkEvent(
                widget=self, event_type=list(parsed_event_type.keys())[0]
            )

        # 限制事件列表大小，防止无限增长
        MAX_EVENTS_PER_INSTANCE = 1000
        MAX_GLOBAL_EVENTS = 5000

        if len(self.events) >= MAX_EVENTS_PER_INSTANCE:
            self.events = self.events[MAX_EVENTS_PER_INSTANCE // 2 :]
        self.events.append(event_obj)

        if len(SkEvent.global_list) >= MAX_GLOBAL_EVENTS:
            SkEvent.global_list = SkEvent.global_list[MAX_GLOBAL_EVENTS // 2 :]
        SkEvent.global_list.append(event_obj)

        # Find targets
        targets = [event_type]
        if list(parsed_event_type.values())[0] in ["", "*"]:
            targets.append(list(parsed_event_type.keys())[0])
            targets.append(list(parsed_event_type.keys())[0] + "[*]")

        for target in targets:
            if target in self.tasks:
                for task in self.tasks[target]:
                    self.execute_task(task, event_obj)

        """

    def bind(self, 
             event_type: str, target: typing.Callable | typing.Iterable,
             multithread: bool = False, _keep_at_clear: bool = False,
            ) -> SkBoundTask | bool:
        """To bind a task to the object when a specific type of event is triggered.

        Example
        -------
        .. code-block
            my_button = SkButton(...).pack()
            press_down_event = my_button.bind("mouse_press", lambda _: print("Hello world!"))
        This shows binding a hello world to the button when it's press.

        :param event_type: The type of event to be bound to
        :param target: A (list of) callable thing, what to do when this task is executed
        :param multithread: If this task should be executed in another thread (False by default)
        :param _keep_at_clear: If the task should be kept when cleaning the event's binding
        :return: SkBoundTask that is bound to the task if success, otherwise False
        """
        parsed_event_type = self.parse_event_type_str(event_type)
        if list(parsed_event_type.keys())[0] not in self.__class__.EVENT_TYPES:
            # warnings.warn(f"Event type {event_type} is not present in {self.__class__.__name__}, "
            #                "so the task cannot be bound as expected.")
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
                    target, # I will fix this type error later (ignore is ur type check is off)
                    float(parsed_event_type["delay"][0]),
                    multithread,
                    _keep_at_clear,
                )
            case "repeat":
                NotImplemented
            case _:  # All normal event types
                task = SkBoundTask(task_id, target, multithread, _keep_at_clear)
        self.tasks[event_type].append(task)
        return task

    def find_task(self, task_id: str) -> SkBoundTask | bool:
        """To find a bound task using task ID.

        Example
        -------
        .. code-block:: python
            my_button = SkButton(...)
            press_task = my_button.find_task("SkButton114.mouse_press.514")
        This shows getting the `SkBoundTask` object of task with ID `SkButton114.mouse_press.514`
        from bound tasks of `my_button`.

        :return: The SkBoundTask object of the task, or False if not found
        """
        task_id_parsed = task_id.split(".")
        if len(task_id_parsed) == 2: # If is a shortened ID (without widget indicator)
            task_id_parsed.insert(0, self.id) # We assume that this indicates self
        for task in self.tasks[task_id_parsed[1]]:
            if task.id == task_id:
                return task
        else:
            return False

    def unbind(self, target_task: str | SkBoundTask) -> bool:
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

        :param target_task: The task ID or `SkBoundTask` to unbind.
        :return: If success
        """
        match target_task:
            case str(): # If given an ID string
                task_id_parsed = target_task.split(".")
                if len(task_id_parsed) == 2: # If is a shortened ID (without widget indicator)
                    task_id_parsed.insert(0, self.id) # We assume that this indicates self
                if task_id_parsed != self.id: # If given ID indicates another widget
                    NotImplemented 
                    # Still not inplemented, as we currently cannot get a SkWidget object itself 
                    # only with its ID (waiting for XiangQinxi)
                    # This part should call the unbind function of the widget with such ID
                for task_index, task in enumerate(self.tasks[task_id_parsed[1]]):
                    if task.id == target_task:
                        self.tasks[task_id_parsed[1]].pop(task_index)
                        return True
                else:
                    return False
            case SkBoundTask():
                for event_type in self.tasks:
                    if target_task in self.tasks[event_type]:
                        self.tasks[event_type].remove(target_task)
                        return True
                else:
                    return False
            case _:
                warnings.warn(
                    "Wrong type for unbind()! Must be event ID or task object",
                    UserWarning,
                )
                return False

    def _check_delay_events(self, _=None) -> None:
        """To check and execute delay events.

        Example
        -------
        Mostly used by SkWidget.update(), which is internal use
        """
        # print("Checking delayed events...")
        for binded_event_type in self.tasks:
            if next(iter(self.parse_event_type_str(binded_event_type))) == "delay":
                for task in self.tasks[binded_event_type]:
                    if isinstance(task, SkDelayTask):
                        if float(time.time()) >= task.target_time:
                            # print(f"Current time is later than target time of {task.id}, "
                            #        "execute the task.")
                            self.execute_task(task)


# Initialize working thread
SkEventHandling.WORKING_THREAD = threading.Thread(
    target=SkEventHandling._working_thread_loop
)


# @dataclass
class SkEvent:
    """Used to represent an event."""
    latest: SkEvent

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
        Included in description.

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
        # Not all properties above will be used
        # Update stuff from args into attributes
        for prop in kwargs.keys():
            if prop not in ["widget", "event_type"]:
                self[prop] = kwargs[prop]

    def __setitem__(self, key: str, value: typing.Any):
        self.event_data[key] = value

    def __getitem__(self, key: str) -> typing.Any:
        if key in self.event_data:
            return self.event_data[key]
        else:
            return None  # If no such item avail, returns None
