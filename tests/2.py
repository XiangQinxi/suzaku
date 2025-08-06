from suzaku import *
# import glfw

app = SkApp(window_event_wait=False)
window = SkWindow(app)
window.resize(200, 200)

#window2 = SkWindow(window)

#SkButton(window).fixed(x=10, y=10, width=100, height=100)
SkButton(window).box(expand=True)
SkButton(window).box(expand=False)
SkButton(window).box(expand=True)
SkButton(window).box(expand=False)
SkButton(window).box(expand=True)

app.run()