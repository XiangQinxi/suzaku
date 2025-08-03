from typing import Union, Any
import skia

from .theme import default_theme, SkTheme
from .window import SkWindow
from .layout import Layout
from ..base.event import EventHanding


class SkWidget(EventHanding):

    _instance_count = 0

    theme = default_theme

    def __init__(self, parent: Union[SkWindow, "SkWidget"], size: tuple[int, int]=(100, 30), style="SkWidget",
                 widget_id: Union[str, None] = None, name="sk_visual") -> None:

        """
        Basic visual component, telling SkWindow how to draw.

        Args:
            parent (SkWindow):
                Parent component (Usually a SkWindow).

            size (tuple[int, int]):
                Default size (not the final drawn size).

            style (str):
                Style of the widget.

            widget_id (str):
                Identification code.

        Returns:
            None
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

        self.is_mouse_enter = False
        self.is_mouse_pressed = False
        self.is_focus = False

        self.draws = []

        self.draw_func = lambda canvas: self._draw(canvas)
        self.parent.add_draw(self.draw_func)

        # Events-related
        self.is_mouse_enter = False
        self.is_focus = False


        def _on_event(event):
            match event.event_type:
                case "mouse_enter":
                    self.is_mouse_enter = True
                case "mouse_leave":
                    self.is_mouse_enter = False
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

    def add_draw(self, draw_func) -> None:
        self.draws.append(draw_func)

    def remove_draw(self, draw_func) -> None:
        self.draws.remove(draw_func)

    def draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        pass

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def add_child(self, child: "SkWidget"):
        self.attributes["children"].append(child)

    def apply_theme(self, new_theme: SkTheme):
        self.attributes["theme"] = new_theme
        for child in self.children:
            child.apply_theme(new_theme)

    # Attributes related
    def get_attribute(self, attribute_name: str) -> Any:
        """Get attribute of a widget by name.

        Args:
            attribute_name: attribute name
        """
        return self.attributes[attribute_name]

    def set_attribute(self, **kwargs):
        self.attributes.update(**kwargs)

    # def place_forget(self) -> None:
    #     """
    #     Remove layout.
    #     移除组件布局。

    #     Returns:
    #         None
    #     """
    #     self._hide()

    # def flow(self, padx=5, pady=5, align="left"):
    #     self.set_parent_layout("flow")

    #     self.parent.add_child_with_layout(
    #         {
    #             "widget": self,
    #             "padx": padx,
    #             "pady": pady,
    #             "align": align  # left/center/right
    #         }
    #     )

    # Aliases
    config = set_attribute
