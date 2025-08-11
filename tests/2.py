from suzaku import *
import glfw
import ctypes
import skia

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
    overrideredirect=True
)

app.resize(400, 400)

textinput = SkTextInput(app, placeholder="请输入")
textinput.box()

hwnd = app.hwnd

app.run()