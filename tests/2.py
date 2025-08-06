from suzaku import *
# import glfw

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
)
app.resize(200, 200)

#SkButton(window).fixed(x=10, y=10, width=100, height=100)
SkButton(app).box()
SkButton(app).box()

app.run()