from suzaku import *
# import glfw

app = SkAppWindow(size=(1000, 100))
app.title("Test")

for i in range(2):
    SkFrame(app).box(side="left")

for i in range(2):
    SkFrame(app).box(side="left", expand=True)

for i in range(2):
    SkFrame(app).box(side="right", expand=True)

for i in range(2):
    SkFrame(app).box(side="right")

app.run()