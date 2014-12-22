from kivy.uix.scatter import ScatterPlane
from kivy.graphics.transformation import Matrix 
from global_environment import Clock, w, h
from time import time

class SwipePlane( ScatterPlane ):
    SWIPE_THRESHOLD = .1*h
    ACC = 1
    def __init__(self, *args, **kwargs):
        """ScatterPlane that responds to swipe gestures."""
        super(type(self), self).__init__(*args, **kwargs)
        self.do_rotation = False
        self.do_translation_y = False
        Clock.schedule_interval(self.animate, 1/60)
        self.stop_inertia()
    
    def start_inertia(self, xvel):
        self.inertial = True
        self.myx, self.xvel = self.x, xvel
        self.xacc = -abs(self.xvel)/self.xvel*self.ACC if abs(self.xvel)>0 else 0
        
    def stop_inertia(self):
        self.inertial = False
        self.xvel, self.xacc = 0,0

    def animate( self, dt ):
        if self.inertial:
            EPSLN = self.ACC
            if -EPSLN <= self.xvel <= EPSLN:
                self.stop_inertia()
                return
            self.xvel += self.xacc
            self.myx  += self.xvel
            self.x_shift( self.myx )

    def x_shift(self, x):
        self.apply_transform( 
            self.transform.inverse().translate( x, 0, 0) 
        )
                
    def on_touch_down( self, touch ):
        super(type(self), self).on_touch_down( touch )
                        
    def on_touch_move( self, touch ):
        super(type(self), self).on_touch_move( touch )

    def on_touch_up( self, touch ):
        self.start_inertia( touch.dx*.1 )
        super(type(self), self).on_touch_up(touch)
    
