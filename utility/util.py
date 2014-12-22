from kivy.graphics import *
from kivy.uix.label import Label
from color_wheel import *
from coordinates import *

def draw_box(widg, pos, size, color, alpha=.3, width=1):
    (x,y), (xdim, ydim), (r,g,b,a) = pos, size, color
    with widg.canvas:
        Color(r, g, b, alpha)
        Line( points=(x, y, x, y+ydim, x+xdim, y+ydim, x+xdim, y, x, y), width=width )

def draw_window_frame(self):
    draw_box(self, (0,0), (w,h), (0,0,1,.5))

def draw_border(self):
    days = ['M','T','W','Th','F']
    hrs = ['12'] + [str(x+1) for x in range(11)]
    r,g,b,a = some_colors['steelblue1']
    for hr in hrs:
        time = hr + ' 00 AM'
        x, y = cal_map('M', time)
        self.add_widget(Label(text=time, pos=label_offset((x-65,y))))
        y += YGAP
        with self.canvas:
            Color(r,g,b,.3)
            Line(points=(x,y,x+w,y))
    for hr in hrs:
        time = hr + ' 00 PM'
        x, y = cal_map('M', time)
        self.add_widget(Label(text=time, pos=label_offset((x-65,y))))
        y += YGAP
        with self.canvas:
            Color(r,g,b,.3)
            Line(points=(x,y,x+w,y))
    for day in days[1:]:
        x, y = cal_map(day, '12 00 AM')
        self.add_widget(Label( pos=label_offset((x,y-30)), text="" ))
        with self.canvas:
            Color(r,g,b,.3)
            Line(points=(x,y,x,y+h))

