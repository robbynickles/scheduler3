from global_environment import *

def human( n ):
    nstring = str(n)
    comma = []
    for i in range(len(nstring)):
        if i%3 == 0 and i != 0: comma += [',']
        comma += [str(nstring[::-1][i])]
    return ''.join( comma[::-1] )

class LoadingScreen( FloatLayout ):
    def __init__(self, progressbar, Nsections, Nschedules, *args, **kwargs):    
        super(type(self), self).__init__(*args, **kwargs)
        with self.canvas:
            Color(0,0,0,.7)
            Rectangle( pos=(0,0), size=(w,h) )
        progressbar.center = w/2,h/2
        self.add_widget( progressbar )
        text = "Validating {} schedule{} from {} section{}...".format( human(Nschedules),
                                                                       's' if Nschedules > 1 else '',
                                                                       human(Nsections),
                                                                       's' if Nsections > 1 else '')
        self.add_widget( Label( center=(w/2,h/2 + 30), text=text ) )
