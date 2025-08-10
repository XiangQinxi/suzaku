from suzaku import *
# import glfw

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
)
app.resize(400, 400)

textinput = SkTextInput(app, placeholder="请输入")
print(textinput.__name__)
textinput.box()

app.run()