from suzaku import *
# import glfw

app = SkAppWindow()
app.title("Test")

frame = SkFrame(app)
frame.place(x=100, y=100, width=40, height=40)

text = SkText(frame, text="SkLabel")
text.place(x=10, y=100)

app.run()