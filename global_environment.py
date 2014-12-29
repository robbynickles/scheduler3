from kivy.graphics import *
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window 
w, h = Window.width, Window.height

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label

from utility.color_wheel import some_colors, get_color
from utility.coordinates import XGAP, YGAP, cal_map, inverse_cal_map, label_offset, extract_times
from utility.util import draw_box, draw_window_frame, draw_border

