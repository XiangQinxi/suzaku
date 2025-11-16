from .app import SkApp  # ✅
from .appwindow import Sk, SkAppWindow  # ✅
from .button import SkButton  # ✅
from .canvas import SkCanvas  # ⛔ 无任何功能
from .card import SkCard  # ✅
from .checkbox import SkCheckBox  # ✅

SkCheckbox = SkCheckBox
from .checkitem import SkCheckItem  # ✅

SkCheckButton = SkCheckbutton = SkCheckitem = SkCheckItem

from .combobox import SkComboBox  # ✅

SkCombobox = SkComboBox
from .container import SkContainer  # ✅
from .empty import SkEmpty  # ✅
from .entry import SkEntry  # ✅
from .frame import SkFrame  # ✅
from .hynix import SkHynix  # ✅
from .image import SkImage  # ⛔ 各种颜色处理未实现
from .label import SkLabel  # ✅
from .lineinput import SkLineInput  # ✅
from .listbox import SkListBox  # ✅

SkListbox = SkListBox
from .listitem import SkListItem  # ✅
from .menu import SkMenu  # ✅
from .menubar import SkMenuBar  # ✅ 但是不是很完善
from .menuitem import SkMenuItem  # ✅

SkMenuitem = SkMenuItem
from .messagebox import SkMessageBox, show_message  # ✅ 但是不是很完善
from .mutiline_input import SkMultiLineInput  # ⛔ 无任何功能
from .popup import SkPopup  # ✅
from .popupmenu import SkPopupMenu  # ✅

SkPopupmenu = SkPopupMenu
from .radiobox import SkRadioBox  # ✅

SkRadiobox = SkRadioBox
from .radioitem import SkRadioItem  # ✅

SkRadioButton = SkRadiobutton = SkRadioitem = SkRadioItem
from .separator import SkSeparator  # ✅
from .sizegrip import SkSizeGrip  # ✅

SkSizegrip = SkSizeGrip
from .slider import SkSlider  # ⛔
from .stack import SkStack
from .switch import SkSwitch  # ✅
from .switchbox import SkSwitchBox  # ✅
from .tabbar import SkTabBar  # ✅

SkTabbar = SkSegmented = SkTabBar
from .tabbutton import SkTabButton  # ✅

SkTabbutton = SkSegmentedButton = SkTabButton
from .tabs import SkTabs  # ✅
from .text import SkText  # ✅
from .textbutton import SkCloseButton, SkMinimizeButton, SkTextButton  # ✅
from .titlebar import SkTitleBar, SkWindowCommand, titlebar  # ✅

SkTitlebar = SkHeaderBar = SkHeaderbar = SkTitleBar

from .widget import SkWidget  # ✅
from .window import SkWindow  # ✅
