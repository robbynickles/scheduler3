from global_environment import *
from utility.helpers import *

class SectionDetail( FloatLayout ):
    def __init__(self, button, callback, pos, size,  *args, **kwargs):    
        super(type(self), self).__init__(*args, **kwargs)
        xdim, ydim = size
        draw_box( self, pos, size, button.section['my_color'] )
        glay = GridLayout(cols=1, pos=pos, size=size, spacing=(.1*xdim,.1*ydim), padding=(.1*xdim,.1*ydim))
        s = button.section
        info = "[b]{}[/b]   [i]{}[/i]   {}".format(getsection(s), getavail(s), getprofessor(s))
        chunks = []
        for ty, days, time, locate in zip(gettypes(s), getdays(s), gettimes(s), getlocations(s)):
            ty = '[b]{}[/b]'.format( ty )
            chunks += ['   '.join([ty, ''.join(days), time, locate])]
        def press_button(b):
            button.state = b.state
            if b.text == 'Section Excluded':
                b.text = 'Section Included'
            else:
                b.text = 'Section Excluded'
            callback( button )
        tb = ToggleButton( on_press=press_button )
        tb.state = button.state
        if tb.state == 'down':
            tb.text = 'Section Excluded'
        else:
            tb.text = 'Section Included'

        glay.add_widget( tb )
        glay.add_widget( Label( text=info, font=18,markup=True ) )
        for chunk in chunks:
            glay.add_widget( Label( text=chunk, font=18,markup=True ) )

        self.add_widget(glay)
