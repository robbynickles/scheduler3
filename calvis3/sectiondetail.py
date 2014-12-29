from global_environment import *
from utility.helpers import *

class SectionDetail( FloatLayout ):
    def __init__(self, block, pos, size,  *args, **kwargs):    
        super(type(self), self).__init__(*args, **kwargs)
        day, start, end, ty, location, course_dict = block
        s = course_dict
        xdim, ydim = size
        draw_box( self, pos, size, s['my_color'] )
        glay = GridLayout(cols=1, pos=pos, size=size)
        info = "[b]{}[/b]   [i]{}[/i]   {}".format(getsection(s), getavail(s), getprofessor(s))
        chunks = []
        for ty, days, time, locate in zip(gettypes(s), getdays(s), gettimes(s), getlocations(s)):
            ty = '[b]{}[/b]'.format( ty )
            chunks += ['  '.join([ty, ''.join(days), time, locate])]

        glay.add_widget( Label( text=info, font_size=48,markup=True ) )
        for chunk in chunks:
            glay.add_widget( Label( text=chunk, font_size=24, markup=True ) )

        self.add_widget(glay)
