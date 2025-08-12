from suzaku import *
import glfw
import ctypes
import skia

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
)

frame1 = SkFrame(app)

frame2 = SkFrame(frame1)

frame3 = SkFrame(frame2)

button = SkButton(frame3)
button.box(padx=0, pady=0)

frame3.fixed(x=10, y=10, width=150, height=150)

frame2.fixed(x=10, y=10, width=200, height=200)

frame1.fixed(x=10, y=10, width=250, height=250)

app.run()