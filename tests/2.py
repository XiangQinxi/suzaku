from suzaku import *
import glfw

app = SkAppWindow()
app.title("Test")

frame = SkFrame(app)
frame.place(x=100, y=100)

text = SkText(app, text="SkLabel")
text.place(x=100, y=200)

app.run()