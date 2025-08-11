from .color import SkGradient, color


def style(sheet, paint, widget=None):
    if isinstance(sheet, list | tuple | str):
        paint.setColor(color(sheet))
    elif isinstance(sheet, dict):
        if "linear" in sheet:
            if widget is not None:
                paint.setColor(color("white"))
                gradient = SkGradient()
                gradient.set_linear(widget=widget, config=sheet["linear"])
                gradient.draw(paint=paint)
    return None
