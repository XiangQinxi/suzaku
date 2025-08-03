from suzaku import *
import glfw

app = SkAppWindow()
app.title("Test")

frame = SkFrame(app)
frame.place(x=100, y=100, width=200, height=200)

app.run()