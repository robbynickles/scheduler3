from global_environment import *
from cal_popup import add_block
import random

def on_touch_down(self, mouse_motion_event):
    super(type(self), self).on_touch_down( mouse_motion_event )
    if self.in_exclusion_mode:
        self.layout = FloatLayout()
        self.top_layer.add_widget( self.layout )

def on_touch_move(self, mouse_motion_event):
    super(type(self), self).on_touch_move( mouse_motion_event )
    if self.in_exclusion_mode:
        x , y = mouse_motion_event.x, mouse_motion_event.y
        ox, oy = mouse_motion_event.ox, mouse_motion_event.oy 
        self.top_layer.remove_widget( self.layout )
        self.layout = FloatLayout()
        left = (int(x) / int(XGAP)) * XGAP
        pos, size = (left, min(y, oy)), (XGAP, abs(y - oy))
        with self.layout.canvas:
            Color(*some_colors['steelblue1'])
            Rectangle( pos=pos, size=size )
            Color(*some_colors['steelblue1'])
            Line( points=[0,y,w,y] )
            Line( points=[0,oy,w,oy] )
        day, start = inverse_cal_map(x,min(y,oy))
        day, end = inverse_cal_map(x,max(y,oy))
        OFFSET = XGAP if day == 'M' else -XGAP 
        start, end = map( adjust_time, [start, end] )
        self.layout.add_widget(Label(text=start, color=some_colors['springgreen3'],
                                     font_size=40, pos=label_offset((pos[0]+XGAP*.3+OFFSET,min(y,oy)))))
        self.layout.add_widget(Label(text=end,color=some_colors['springgreen3'],
                                     font_size=40, pos=label_offset((pos[0]+XGAP*.3+OFFSET,max(y,oy)))))
        self.top_layer.add_widget( self.layout )

def on_touch_up(self, mouse_motion_event):
    super(type(self), self).on_touch_up( mouse_motion_event )
    try:
        self.top_layer.remove_widget( self.layout )
    except:
        return
    x , y = mouse_motion_event.x, mouse_motion_event.y
    ox, oy = mouse_motion_event.ox, mouse_motion_event.oy
    if self.in_exclusion_mode and \
           .2*h < y < h - .05*h and .2*h < oy < h - .05*h and abs(y-oy) > .01*h:
        day, start = inverse_cal_map(x, min(y, oy))
        day, end = inverse_cal_map(x, max(y, oy))
        course_dict = create_course_dict(start, end, day)
        self.add_user_event( course_dict )
        
def create_course_dict(start, end, day, name='MPersonal'):
    start, end = map(adjust_time, [start, end])
    return \
        {'Name': [name], 'Title': [''],
         'Section': [''], 'Days': [[day]],
         'Times': ['{} - {}'.format( start, end)],
         'Avail': [''], 'Location': [''],
         'Units': [''], 'Instructor': [''], 'Type': ['PERS'],
         'Important Notes': [''], 'Max/': [''],
         'ID' : int(random.random()*1000),
         'included_in_search' : True,
         'row_group' : None,
         'my_color' : some_colors['steelblue1'],
         'old_included_in_search' : True,
         'kept_section' : False }

def adjust_time(t):
    hr, m, mer = t.split(' ')
    hr = '0'+hr if int(hr)<10 else hr
    m = str(int(m)/5 * 5)
    m = '0'+m if int(m)<10 else m
    mer = 'A' if mer == 'AM' else 'P'
    return "{}:{}{}".format(hr, m, mer)
