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

    Events should be represented in the form of `event_type` or `event_type[args]`. e.g. `delay` or 
    `delay[500]`
    """

    EVENT_TYPES: list[str] = [
        "resize", "move", "configure", "update", 
        "mouse_move", "mouse_enter", "mouse_leave", "mouse_press", "mouse_release", 
        "focus_gain", "focus_loss", 
        "key_press", "key_release", "key_repeat", 
        "char", "click", 
        "delay", 
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
            SkEvent.global_list.append(NotImplemented)
            # To execute all tasks binded under this event
            if not task.multithread:
                # If not multitask, execute directly
                task.target()
            else:
                # Otherwise add to multithread tasks list and let the working thread to deal with it
                SkEventHandling.multithread_tasks.append(task)
    
    def bind(self, event_type: str, target: typing.Callable, 
             multithread: bool, _keep_at_clear: bool) -> SkBindedTask | bool:
        """To bind a task to the object when a specific type of event is triggered.

        Example
        -------
        .. code-block
            my_button = SkButton(...).pack()
            press_down_event = my_button.bind("mouse_press", lambda _: print("Hello world!"))
        This shows binding a hello world to the button when it's pressed.
        
        :param event_type: The type of event to be binded to
        :param target: A callable thing, what to do when this task is executed
        :param multithread: If this task should be executed in another thread (False by default)
        :param _keep_at_clear: If the task should be kept when clearning the event's binding
        :return: SkBindedTask that is binded to the task if success, otherwise False
        """
        if event_type not in self.__class__.EVENT_TYPES:
            warnings.warn(f"Event type {event_type} is not present in {self.__class__.__name__}, "
                           "so the task cannot be binded as expected.")
            return False
        task_id = f"{self.id}.{event_type}.{len(self.tasks[event_type])}"
        # e.g. SkButton114.focus_gain.514 / SkEventHandling114.focus_gain.514
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

    def unbind(self, task_id: str) -> bool:
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
        This show unbinding all tasks under `mouse_press` event from `my_button`.

        :param task_id: The task ID to unbind.
        :return: If success
        """
        task_id_parsed = task_id.split(".")
        for task_index, task in enumerate(self.tasks[task_id_parsed[1]]):
            if task.id == task_id:
                self.tasks[task_id_parsed[1]].pop(task_index)
                return True
        else:
            return False
    
    def update(self):
        NotImplemented

# Initialize working thread
SkEventHandling.WORKING_THREAD = threading.Thread(target = SkEventHandling._working_thread_loop)

@dataclass
class SkEvent:
    """Used to represent an event."""

    global_list: list[SkEvents] = []

    def __init__(self):
        self.event_type: str = "[Unspecified]"  # Type of event
        self.widget: typing.Optional[typing.Any] = None  # Relating widget
        self.window_base: typing.Optional[typing.Any] = None  # WindowBase of the current window
        self.window: typing.Optional[typing.Any] = None  # Current window
        self.pos: typing.Optional[tuple[int, int] | list[int]] = None  # Position (to the widget)
        self.abspos: typing.Optional[tuple[int, int] | list[int]] = None  # Absolute position in win
        self.key: typing.Optional[int | str] = None  # Related keys
        self.keyname: typing.Optional[str] = None  # Name of keys
        self.mods: typing.Optional[str] = None  # 【修饰键名】 (? Need explanation)
        self.mods_key: typing.Optional[int] = None  # 【修饰键值】 (? Need explanation)
        self.entered_text: typing.Optional[str] = None  # Text entered
        self.new_size: typing.Optional[tuple[int, int] | list[int]] = None  # The new size
        self.window_state: typing.Optional[str] = None  # New window state
        self.dropped: typing.Optional[list[str] | bytes | bytearray| str] = None # Stuff droped in
        self.cursor_displacement: typing.Optional[tuple[int, int] |\
                                                   list[int]] = None  # Mouse displacement
        # Not all proprties above will be used
