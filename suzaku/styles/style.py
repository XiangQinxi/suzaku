from .color import SkGradient, make_color


def style(sheet, paint, widget=None):
    if isinstance(sheet, list | tuple | str):
        paint.setColor(make_color(sheet))
    elif isinstance(sheet, dict):
        if "linear" in sheet:
            if widget is not None:
                paint.setColor(make_color("white"))
                gradient = SkGradient()
                gradient.set_linear(widget=widget, config=sheet["linear"])
                gradient.draw(paint=paint)
    return None
