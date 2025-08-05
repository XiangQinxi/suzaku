from typing import Any, Union

import skia

from suzaku.event import SkEventHanding

from ..styles.theme import SkTheme, default_theme
from .window import SkWindow


class SkWidget(SkEventHanding):

    _instance_count = 0

    theme = default_theme

    def __init__(self, parent: Union[SkWindow, "SkWidget"], size: tuple[int, int]=(100, 30), 
                 style="SkWidget", widget_id: Union[str, None] = None, name="SkWidget") -> None:
        """Basic visual component, telling SkWindow how to draw.

        parent: Parent component (Usually a SkWindow)
        size: Default size (not the final drawn size)
        styles: Style of the widget
        widget_id: Identification code
        """

        super().__init__()

        self.__class__._instance_count += 1

        self.parent = parent

        self.window = self.parent if isinstance(self.parent, SkWindow) else self.parent.window

        self.attributes = {
            "name": name,
            "cursor": "arrow",
            "id": widget_id,
            "theme": None,
            "dwidth": size[0],  # default width
            "dheight": size[1],  # default height
        }

        self.theme = self.parent.theme
        self.style = style

        self.x = 0
        self.y = 0

        self.width = size[0]
        self.height = size[1]

        self.layout = None
        self.visible = False

        if not widget_id:
            self.attributes["id"] = name + "." + str(self.__class__._instance_count)

        self.events = {
            "mouse_motion": [],
            "mouse_enter": [],
            "mouse_leave": [],
            "mouse_pressed": [],
            "mouse_released": [],
            "focus_gain": [],
            "focus_loss": [],
            "key_press": [],
            "key_release": [],
            "key_repeat": [],
            "char": [],
        }

        try:
            self.parent.add_child(self)
        except TypeError:
            raise TypeError("Parent component is not SkWindow or SkWidget.")

        # Events-related
        self.is_mouse_floating = False
        self.is_mouse_pressed = False
        self.is_focus = False

        def _on_event(event):
            match event.event_type:
                case "mouse_enter":
                    self.is_mouse_floating = True
                case "mouse_leave":
                    self.is_mouse_floating = False
                case "focus_gain":
                    self.is_focus = True
                case "focus_loss":
                    self.is_focus = False
            pass

        self.bind("mouse_enter", _on_event)
        self.bind("mouse_leave", _on_event)
        self.bind("mouse_pressed", _on_event)
        self.bind("mouse_released", _on_event)
        self.bind("focus_in", _on_event)
        self.bind("focus_out", _on_event)

    def draw(self, canvas: skia.Surfaces) -> None:
        """Execute the widget rendering and subwidget rendering

        :param canvas:
        :return: None
        """
        rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)
        self._draw(canvas, rect)
        if hasattr(self, "draw_children"):
            self.draw_children(canvas)

    def _draw(self, canvas: skia.Surfaces, rect: skia.Rect) -> None:
        """Execute the widget rendering

        :param canvas: skia.Surfaces
        :param rect: skia.Rect
        :return:
        """
        pass

    def show(self):
        """Make the component visible

        :return: self
        """
        self.visible = True
        return self

    def hide(self):
        """Make the component invisible

        :return: self
        """
        self.visible = False
        return self

    # Attributes related
    def get_attribute(self, attribute_name: str) -> Any:
        """Get attribute of a widget by name.

        :param attribute_name: attribute name
        """
        return self.attributes[attribute_name]

    cget = get_attribute

    def set_attribute(self, **kwargs):
        """Set attribute of a widget by name.

        :param kwargs: attribute name and value
        :return: self
        """
        self.attributes.update(**kwargs)
        return self

    configure = config = set_attribute

    def apply_theme(self, new_theme: SkTheme):
        """Apply theme to the widget and its children.`

        :param new_theme:
        :return:
        """
        self.theme = new_theme
        if hasattr(self, "children"):
            for child in self.children:
                child.apply_theme(new_theme)

    def place(self, x: int, y: int, width: int = None, height: int = None):
        """Place the widget at a specific position.

        :param x:
        :param y:
        :param width:
        :param height:
        :return: self
        """
        self.x = x
        self.y = y
        if width:
            self.width = width
        if height:
            self.height = height
        self.parent.add_floating_child(
            {
                "child": self,
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height
            }
        )
        self.visible = True
        return self

    def place_forget(self):
        """Remove widget layout

        :return: self
        """
        self.visible = False
        return self

    # Layout related
    def pack(self, padx: int=0, pady: int=0, expand: bool=False):
        pass

    def focus_set(self):
        self.window.focus_widget = self

    def focus_get(self):
        return self.window.focus_get()
