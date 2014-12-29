from global_environment import *
from utility.helpers import getsection

class MapPage( FloatLayout ):
    def __init__(self, calender=None, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.calender = calender
        xdim, ydim = self.size
        r,g,b,a = some_colors['steelblue1']
        self.add_widget( Button( on_press=self.show_map, 
                                 pos=(self.x, .9*ydim + self.y), 
                                 size_hint_y=.1,
                                 background_color=(r,g,b,.5),
                                 text="Show Map of Schedule" ) )
    
    def show_map( self, button ):
        for s in self.calender.get_current_schedule():
            print getsection(s.event_dict)

