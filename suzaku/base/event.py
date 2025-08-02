from .after import After

from typing import Union, Any


class EventHanding(After):

    """Event binding manager."""

    def __init__(self):

        """Initialize all bindable events."""

        self.evts = {}

    def event_generate(self, name: str, *args, **kwargs) -> Union[bool, Any]:
        """Send event signal.

        * name: Event name, create if not existed
        * *args: Passed to `evt`
        * **kwargs: Passed to `evt`
        * return: Return value from the function, or False for failed
        """

        if not name in self.evts:
            self.evts[name] = []

        for evt in self.evts[name]:
            evt(*args, **kwargs)


    def bind(self, name: str, func: callable, add: bool=True) -> "EventHanding":
        """Bind event.

        * name: Event name, create if not existed.
        * func: Function to bind.
        * add: If do append, otherwise replace.
        """
        if name not in self.evts:
            self.evts[name] = [func]
        if add:
            self.evts[name].append(func)
        else:
            self.evts[name] = [func]
        return self

    def unbind(self, name: str, func: callable) -> None:
        """Unbind event.

        * name: Event name
        * func: Function to unbind
        """
        self.evts[name].remove(func)


class Event:

    """Used to pass event via arguments."""

    def __init__(self, x: int = None, y: int = None, rootx: int = None, rooty: int = None, key: int = None, keyname: str = None, mods: str = None, char: str = None):
        """Used to pass event via arguments.

        * x: x position of cursor / component (Relative to window)
        * y: y position of cursor / component (Relative to window)
        * rootx: x position of cursor / component (Relative to screen)
        * rooty: y position of cursor / component (Relative to screen)
        * key: Key name
        * keyname: Key name string
        * mods: Modifier keys
        * char: Character
        """
        self.x = x
        self.y = y
        self.rootx = rootx
        self.rooty = rooty
        self.key = key
        self.keyname = keyname
        self.mods = mods
        self.char = char
