try:
    from suzaku import *
except ModuleNotFoundError:
    import os
    import sys
    parent_dir = os.path.abspath("../suzaku")
    sys.path.append(parent_dir)
    from suzaku import *

app = Sk(
    #theme=SkTheme.INTERNAL_THEMES["dark"]
    is_always_update=True
)
app.window_attr("topmost", True)
#app.bind("update", lambda evt: print(app.time()))

id1 = app.after(2, lambda: print("123"))
app.after(1, lambda: app.after_cancel(id1))
app.after(2, lambda: print("456"))

"""
import skia

from win32gui import GetWindowLong, SetWindowLong, SetLayeredWindowAttributes
from win32con import GWL_EXSTYLE, WS_EX_LAYERED, LWA_COLORKEY, LWA_ALPHA

hwndGLFW = app.hwnd

ret = GetWindowLong(hwndGLFW, GWL_EXSTYLE)
ret = ret | WS_EX_LAYERED
SetWindowLong(hwndGLFW, GWL_EXSTYLE, ret)
SetLayeredWindowAttributes(hwndGLFW, skia.Color(240, 240, 240), 100, LWA_COLORKEY)
"""

frame1 = SkFrame(app, border=True)

frame2 = SkFrame(frame1, border=True)

frame3 = SkFrame(frame1, border=True)

button = SkButton(frame3)
button.box(padx=10, pady=10)

frame3.box(side="left", expand=True)

frame2.box(side="left", expand=True)

frame1.box(side="left", expand=True)

app.run()