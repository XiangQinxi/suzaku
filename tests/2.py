from suzaku import *
import glfw

app = SkAppWindow()
app.title("Test")

frame = SkFrame(app)
frame.put(margin=(20, 20, 20, 20))

frame2 = SkFrame(frame)
frame2.put(margin=(20, 20, 20, 20))

app.run()