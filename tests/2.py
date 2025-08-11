from suzaku import *
import glfw
import ctypes
import skia

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
)

SkTextInput(app, placeholder="请输入").box()
SkTextInput(app, placeholder="请输入").box()
SkTextInput(app, placeholder="请输入").box()
SkTextInput(app, placeholder="请输入").box()
SkTextInput(app, placeholder="请输入").box()
SkTextInput(app, placeholder="请输入").box()


app.run()