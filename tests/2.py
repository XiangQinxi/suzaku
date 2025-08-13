try:
    from suzaku import *
except ModuleNotFoundError:
    import os
    import sys
    parent_dir = os.path.abspath("../suzaku")
    sys.path.append(parent_dir)
    from suzaku import *
# import glfw
# import ctypes
# import skia

app = Sk(
    #theme=SkTheme.INTERNAL_THEMES["dark"]
)

frame1 = SkFrame(app, border=True)

frame2 = SkFrame(frame1, border=True)

frame3 = SkFrame(frame1, border=True)

button = SkButton(frame3)
button.box(padx=10, pady=10)

frame3.box(side="left", expand=True)

frame2.box(side="left", expand=True)

frame1.box(side="left", expand=True)

app.run()