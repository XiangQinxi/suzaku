from suzaku import *
# import glfw

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
)
app.resize(200, 200)

frame = SkFrame(app).box(expand=True)
SkButton(frame).box()
SkButton(frame).box()

"""SkButton(app, command=lambda: SkButton(app).box(side="left", expand=True)).box(side="left")

SkButton(app).box(side="right", expand=True)"""

app.run()