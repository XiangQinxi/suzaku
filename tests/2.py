import glfw

try:
    from suzaku import *
except ModuleNotFoundError:
    import os
    import sys

    parent_dir = os.path.abspath("../suzaku")
    sys.path.append(parent_dir)
    from suzaku import *

app = Sk(
    # theme=SkTheme.INTERNAL_THEMES["dark"]
    is_always_update=True
)

app.bind("closed", lambda _: print("closed"))

btn = SkTextButton(app, text="This is a SkTextButton")
btn.fixed(x=10, y=10)

btn2 = SkTextButton(
    app, text="Delete two characters", command=lambda: btn.set(btn.get()[:-2])
)
btn2.fixed(x=10, y=80)

app.run()
