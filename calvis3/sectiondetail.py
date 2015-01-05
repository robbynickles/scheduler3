from global_environment import *
from utility.helpers import *

class SectionDetail( FloatLayout ):
    def __init__(self, parent, block, pos, size,  *args, **kwargs):    
        super(type(self), self).__init__(*args, **kwargs)
        day, start, end, ty, location, course_dict = block
        s = course_dict
        xdim, ydim = size
        draw_box( self, pos, size, s['my_color'] )
        glay = GridLayout(cols=1, pos=pos, size=size)

        info = "[b]{}[/b]   [i]{}[/i]   {}".format(getsection(s), getavail(s), getprofessor(s))
        glay.add_widget( Label( text=info, font_size=48,markup=True ) )

        chunks = []
        for typ, days, time, locate in zip(gettypes(s), getdays(s), gettimes(s), getlocations(s)):
            if typ == 'DINT': 
                days = ''
            if typ == 'PERS':
                chunks += ["Excluded Time  {}  {}".format( days[0], time )]
            else:
                typ = '[b]{}[/b]'.format( typ )
                chunks += ['  '.join([typ, ''.join(days), time, locate])]
        for chunk in chunks:
            glay.add_widget( Label( text=chunk, font_size=24, markup=True ) )

        if ty == 'PERS':
            def remove_user_event(button):
                parent.bulletin.remove_user_event( button.user_event['ID'] )
                parent.top_layer.remove_widget(parent.active_button.my_popup)
                parent.user_event_layer.remove_widget(parent.active_button)
                parent.active_button = None
            remove_user_event_button = ToggleButton(size_hint_y=.2, text='Remove', on_release=remove_user_event)
            remove_user_event_button.user_event = course_dict
            glay.add_widget( remove_user_event_button )
        self.add_widget(glay)

