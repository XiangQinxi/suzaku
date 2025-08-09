from .color_old import color
from .gradient import linear_gradient


def style(sheet, paint, widget=None):
    if isinstance(sheet, list | tuple | str):
        paint.setColor(color(sheet))
    elif isinstance(sheet, dict):
        if "linear" in sheet:
            if widget is not None:
                paint.setColor(color("white"))
                linear_gradient(widget=widget, configs=sheet["linear"], paint=paint)
    return None
