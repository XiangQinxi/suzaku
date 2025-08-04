from .windowbase import SkWindowBase
from .container import SkContainer
import skia


class SkWindow(SkWindowBase, SkContainer):
    def __init__(self, *args, themename="light", style="SkWindow", name="sk_window", **kwargs) -> None:
        """
        SkWindow, inherited from SkWindowBase

        :param args: SkWindowBase Args
        :param themename: Theme name
        :param kwargs: SkWindowBase Kwargs
        """
        SkWindowBase.__init__(self, *args, name=name, **kwargs)
        SkContainer.__init__(self)

        from suzaku.styles.theme import default_theme

        self.theme = default_theme

        self.attributes["styles"] = style
        self.focus_widget = self
        self.draws = []

        self.window = self

        self.previous_widget = None

        self.set_draw_func(self.draw)
        self.bind("mouse_motion", self._motion, add=True)
        self.bind("mouse_press", self._mouse)
        self.bind("mouse_release", self._mouse_release)

        self.bind("focus_out", self._leave)
        self.bind("mouse_leave", self._leave)

        self.bind("char", self._char)

        self.bind("key_press", self._key_press)
        self.bind("key_repeat", self._key_repect)
        self.bind("key_release", self._key_release)

        self.bind("update", self._update)

    from suzaku.styles.theme import SkTheme

    def apply_theme(self, new_theme: SkTheme):
        self.attributes["theme"] = new_theme
        for child in self.children:
            child.apply_theme(new_theme)

    def _update(self, event):
        """
        Update event for SkWindow.

        Args:
            event: Update event.

        Returns:

        """
        for widget in self.children:
            from .event import SkEvent
            widget.event_generate("update", SkEvent(event_type="update"))

    def _key_press(self, event):
        #print(cls.cget("focus_widget"))
        if self.focus_get() is not self:
            self.focus_get().event_generate("key_press", event)

    def _key_repect(self, event):
        if self.focus_get() is not self:
            self.focus_get().event_generate("key_repeat", event)

    def _key_release(self, event):
        if self.focus_get() is not self:
            self.focus_get().event_generate("key_release", event)

    def _char(self, event):
        #print(12)
        if self.focus_get() is not self:
            self.focus_get().event_generate("char", event)

    def _leave(self, event):
        from .event import SkEvent
        event = SkEvent(event_type="mouse_leave", x=event.x, y=event.y, rootx=event.rootx, rooty=event.rooty)
        for widget in self.children:
            widget.event_generate("mouse_leave", event)

    def _mouse(self, event) -> None:
        for widget in self.children:
            if (widget.x <= event.x <= widget.x + widget.width and
                    widget.y <= event.y <= widget.y + widget.height):
                widget.focus_set()
                #print(widget)
                widget.event_generate("mouse_press", event)
                break

    from .event import SkEvent

    def _motion(self, event: SkEvent) -> None:
        """

        Args:
            event:

        Returns:

        """
        current_widget = None
        from .event import SkEvent
        event = SkEvent(event_type="mouse_motion", x=event.x, y=event.y, rootx=event.rootx, rooty=event.rooty)

        # 找到当前鼠标所在的视觉元素
        for widget in reversed(self.children):
            if (widget.x <= event.x <= widget.x + widget.width and
                widget.y <= event.y <= widget.y + widget.height):
                current_widget = widget
                break

        # 处理上一个元素的离开事件
        if self.previous_widget and self.previous_widget != current_widget:
            self.cursor(self.default_cursor())
            self.previous_widget.event_generate("mouse_leave", event)
            self.previous_widget.is_mouse_enter = False

        # 处理当前元素的进入和移动事件
        if current_widget:
            if current_widget.visible:
                if not current_widget.is_mouse_enter:
                    self.cursor(current_widget.attributes["cursor"])
                    current_widget.event_generate("mouse_enter", event)
                    current_widget.is_mouse_enter = True
                else:
                    self.cursor(current_widget.attributes["cursor"])
                    current_widget.event_generate("mouse_motion", event)
                self.previous_widget = current_widget
        else:
            self.previous_widget = None

    def add_child(self, child: "SkWidget"):
        """
        Add child widget to window.

        Args:
            child: SkWidget

        Returns:
            None
        """
        self.children.append(child)

    def add_draw(self, draw_func) -> None:
        self.draws.append(draw_func)

    def remove_draw(self, draw_func) -> None:
        self.draws.remove(draw_func)

    def draw(self, canvas: skia.Surfaces) -> None:
        from ..styles.color import color
        canvas.clear(color(self.theme.styles[self.winfo_style()]["bg"]))

        for i, f in enumerate(self.draws):
            #print(i, f)
            if self.children[i].visible:
                f(canvas)
        return None

    def winfo_style(self) -> str:
        return self.attributes["styles"]

    def _mouse_release(self, event) -> None:
        from .event import SkEvent
        event = SkEvent(
            event_type="mouse_release",
            x=event.x,
            y=event.y,
            rootx=self.mouse_rootx,
            rooty=self.mouse_rooty
        )
        for widget in self.children:
            if widget.is_mouse_pressed:
                widget.event_generate("mouse_release", event)
                widget.is_mouse_pressed = False
        return None

    def focus_get(self):
        return self.focus_widget

    def focus_set(self, widget):
        self.focus_widget = widget
