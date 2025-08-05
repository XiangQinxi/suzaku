from suzaku import *
# import glfw

app = SkAppWindow(size=(100, 100))
app.title("Test")

SkButton(app).fixed(x=10, y=10, width=50, height=50)

app.run()