from .frame import SkFrame

from typing import Union

class SkButton(SkFrame):

    def __init__(self, *args, text: str = "SkButton", size: tuple[int, int] = (105, 35),
                 cursor: Union[str, None] = "hand", style="SkButton",
                 command: Union[callable, None] = None, id: Union[str, None] = None, **kwargs) -> None:
        """Button Component.

        **Will be re-written in future.**

        * *args: Passed to SkVisual
        * text: Button text
        * size: Default size
        * cursor: Cursor style when hovering
        * style: Style name
        * command: Function to run when clicked
        * id: Identification code (optional)
        * **kwargs: Passed to SkVisual
        """

        super().__init__(*args, size=size, style=style, name="sk_button", **kwargs)

        self.events["click"] = []
        self.attributes["text"] = text

        self.attributes["cursor"] = cursor

        self.command = command

        if command:
            self.bind("click", lambda evt: command())

        #cls.bind("mouse_pressed", lambda evt: print("pressed"))
        self.bind("mouse_released", self._click)

    def _click(self, evt) -> None:
        """
        Check click event (not pressed).

        :return: None
        """
        if self.is_mouse_floating:
            self.event_generate("click", evt)

    def draw(self, canvas, rect) -> None:
        """Draw button.

        * canvas: skia.Surface to draw on
        * rect: Rectangle to draw in
        """


