from suzaku import *

app = Sk(themename="light")

SkButton(app, text=f"切换至Light主题", command=lambda: app.theme.use_theme("light")).vbox(padx=10, pady=10)
SkButton(app, text=f"切换至Dark主题", command=lambda: app.theme.use_theme("dark")).vbox(padx=10, pady=10)
SkEntry(app, placeholder="请输入名称").vbox(padx=10, pady=10)

app.run()