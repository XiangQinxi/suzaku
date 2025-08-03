from suzaku import *
import glfw

app = SkAppWindow()
app.title("Test")

frame = SkFrame(app)
frame.visible = True
frame.put(margin=(20, 20, 20, 20))

app.run()