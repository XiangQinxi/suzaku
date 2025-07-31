from .visual import SkVisual


class SkButton(SkVisual):
    def __init__(self, *args, text: str = "SkButton", size=(110, 40), bg=(0, 0, 0, 20), fg=(0, 0, 0, 235), border=(0, 0, 0, 10), hover_bg=(0, 0, 0, 40), radius=6, id=None, **kwargs):
        super().__init__(*args, size=size, **kwargs)
        self.visual_attr["name"] = "sk_button"
        self._id(id=id)
        self.visual_attr["text"] = text

        from ..style.color import color
        self.visual_attr["bg"] = color(bg)
        self.visual_attr["fg"] = color(fg)
        self.visual_attr["border"] = color(border)
        self.visual_attr["hover_bg"] = color(hover_bg)
        self.visual_attr["radius"] = radius


        """self.bind("mouse_enter", lambda evt: print("enter"))
        self.bind("mouse_leave", lambda evt: print("leave"))
        self.bind("mouse_motion", lambda evt: print("motion"))"""

        #self.bind("mouse_pressed", lambda evt: print("pressed"))

    def _id(self, id=None):
        self.visual_attr["id"] = id or (self.winfo_name() + "." + str(self.get_instance_count()))

    def draw(self, canvas, rect):
        import skia
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
            StrokeWidth=1
        )

        if self.is_mouse_enter:
            rect_paint.setColor(self.visual_attr["hover_bg"])
        else:
            rect_paint.setColor(self.visual_attr["bg"])

        canvas.drawRoundRect(rect, self.visual_attr["radius"], self.visual_attr["radius"], rect_paint)

        rect_paint.setStyle(skia.Paint.kStroke_Style)
        rect_paint.setColor(self.visual_attr["border"])

        canvas.drawRoundRect(rect, self.visual_attr["radius"], self.visual_attr["radius"], rect_paint)

        text_paint = skia.Paint(
            AntiAlias=True,
            Color=self.visual_attr["fg"]
        )

        from ..base.font import default_font
        font = default_font()

        #canvas.drawTextBlob(text, self.winfo_x(), self.winfo_y()+self.winfo_height()/2, paint2)


        text_width = font.measureText(self.visual_attr["text"])
        metrics = font.getMetrics()

        draw_x = self.winfo_x() + self.winfo_width() / 2 - text_width / 2
        draw_y = self.winfo_y() + self.winfo_height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(self.visual_attr["text"], draw_x, draw_y, font, text_paint)
