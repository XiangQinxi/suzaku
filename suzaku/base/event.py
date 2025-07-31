class EventHanding:

    def __init__(self):
        self.evts = {}

    def event_generate(self, name: str, *args, **kwargs):
        if name in self.evts:
            for evt in self.evts[name]:
                evt(*args, **kwargs)

    def bind(self, name: str, func: callable, add: bool = True, id=None):
        if name not in self.evts:
            self.evts[name] = []
        if add:
            self.evts[name].append(func)
        else:
            self.evts[name] = [func]
        return self

    def unbind(self, name, func):
        self.evts[name].remove(func)


class Event:
    def __init__(self, x, y, rootx, rooty):
        self.x = x
        self.y = y
        self.rootx = rootx
        self.rooty = rooty
