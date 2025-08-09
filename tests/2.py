from suzaku import *
# import glfw

app = Sk(
    window_event_wait=False, #theme=SkTheme.INTERNAL_THEMES["dark"]
)
app.resize(400, 400)

frame = SkFrame(app).box(expand=True)
SkTextButton(frame, text="Hello", command=lambda: print("Hello")).box(pady=0)
SkTextButton(frame, text="World", command=lambda: print("World")).box(pady=0)
SkEntry(frame).box()
#SkButton(frame).box(expand=True)

"""frame2 = SkFrame(frame).box(expand=True)
SkButton(frame2).box()
SkButton(frame2).box()"""

"""SkButton(app, command=lambda: SkButton(app).box(side="left", expand=True)).box(side="left")

SkButton(app).box(side="right", expand=True)"""

app.run()