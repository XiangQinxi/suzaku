from suzaku import Sk, SkText, SkEntry, SkStringVar


root = Sk(vsync=False, is_always_update=False)

var = SkStringVar(default_value="Hello, world!")

entry = SkEntry(root, textvariable=var).box()
text = SkText(root, textvariable=var).box()

root.mainloop()
