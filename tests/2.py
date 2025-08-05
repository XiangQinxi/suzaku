from suzaku import *
# import glfw

app = SkApp(window_event_wait=True)
window = SkWindow(app)
window.resize(200, 200)

SkButton(window).fixed(x=10, y=10, width=100, height=100)

app.run()