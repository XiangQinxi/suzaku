from suzaku import *
# import glfw

app = SkAppWindow()
app.title("Test")

frame = SkFrame(app)
frame.place(x=100, y=100, width=500, height=500)

text = SkText(frame, text="SkLabel")
text.place(x=100, y=100)

app.run()