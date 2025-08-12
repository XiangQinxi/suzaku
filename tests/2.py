from suzaku import *
import glfw
import ctypes
import skia

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
)

frame1 = SkFrame(app)

frame2 = SkFrame(frame1)

frame2.fixed(x=10, y=10, width=150, height=150)

frame1.fixed(x=10, y=10, width=260, height=440)

app.run()