from .visual import SkVisual

from typing import Union
from typing import Any


class SkButton(SkVisual):
    def __init__(self, *args, text: str="SkButton", size: tuple[int, int]=(110, 40), cursor: str="hand", 
                 command: Union[function, None]=None, id: Any=None, **kwargs):
        super().__init__(*args, size=size, **kwargs)

        self.evts["click"] = []
        self.visual_attr["name"] = "sk_button"
        self._id(id=id)
        self.visual_attr["text"] = text

        self.visual_attr["radius"] = self.theme.get_theme()["SkButton"]["radius"]
        self.visual_attr["cursor"] = cursor

        self.command = command

        if command:
            self.bind("click", lambda evt: command())

        """self.bind("mouse_enter", lambda evt: print("enter"))
        self.bind("mouse_leave", lambda evt: print("leave"))
        self.bind("mouse_motion", lambda evt: print("motion"))"""

        #self.bind("mouse_pressed", lambda evt: print("pressed"))
        self.bind("mouse_released", self._click)

    def _click(self, evt):
        if self.is_mouse_enter:
            self.event_generate("click", evt)

    def _id(self, id=None):
        self.visual_attr["id"] = id or (self.winfo_name() + "." + str(self.get_instance_count()))

    def draw(self, canvas, rect):
        import skia
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        from ..style.color import color

        if self.is_mouse_enter:
            if self.is_mouse_pressed:
                sheets = self.theme.get_theme()["SkButton"]["pressed"]
            else:
                sheets = self.theme.get_theme()["SkButton"]["hover"]
        else:
            sheets = self.theme.get_theme()["SkButton"]["rest"]
        rect_paint.setColor(color(sheets["bg"]))
        rect_paint.setStrokeWidth(sheets["width"])

        canvas.drawRoundRect(rect, self.visual_attr["radius"], self.visual_attr["radius"], rect_paint)

        rect_paint.setStyle(skia.Paint.kStroke_Style)
        rect_paint.setColor(color(sheets["border"]))

        canvas.drawRoundRect(rect, self.visual_attr["radius"], self.visual_attr["radius"], rect_paint)

        text_paint = skia.Paint(
            AntiAlias=True,
            Color=color(sheets["fg"])
        )

        from ..base.font import default_font
        font = default_font()

        #canvas.drawTextBlob(text, self.winfo_x(), self.winfo_y()+self.winfo_height()/2, paint2)


        text_width = font.measureText(self.visual_attr["text"])
        metrics = font.getMetrics()

        draw_x = self.winfo_x() + self.winfo_width() / 2 - text_width / 2
        draw_y = self.winfo_y() + self.winfo_height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(self.visual_attr["text"], draw_x, draw_y, font, text_paint)
