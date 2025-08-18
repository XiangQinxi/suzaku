from suzaku import Sk, SkText, SkEntry, SkStringVar


root = Sk()

var = SkStringVar(default_value="Hello, world!")

entry = SkEntry(root, textvariable=var).box()
text = SkText(root, textvariable=var).box()


root.mainloop()
