from suzaku import *
# import glfw

app = SkAppWindow(size=(100, 100))
app.title("Test")

SkButton(app).box(side="top")

app.run()