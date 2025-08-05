from suzaku import *
# import glfw

app = SkAppWindow(size=(1000, 100))
app.title("Test")

for i in range(2):
    SkFrame(app).box(direction="left")

for i in range(2):
    SkFrame(app).box(direction="left", expand=True)

for i in range(2):
    SkFrame(app).box(direction="right", expand=True)

for i in range(2):
    SkFrame(app).box(direction="right")

app.run()