import threading, time
from kivy.uix.progressbar import ProgressBar

from global_environment import *
from utility.color_wheel import somet_colors
from cal_popup import add_block
from algorithm.helpers import overlap
import exclusion
from loadingscreen import LoadingScreen

from math import factorial
ncr = lambda n, r: factorial(n) / ( factorial(r) * factorial( n - r ) )
def a_function(N, n):
    return sum( [ ncr(N, n - i ) for i in range( n-3 ) ])

class Calender(FloatLayout):
    def generation_object( self ):
        self.clear_layer(self.schedule_layer)
        self.stored_schedules = []
        self.schedule_index = -1
        items = self.bulletin.get_sections_selected()
        number_of_courses = len(self.bulletin.selected_courses)
        number_of_schedules = a_function(len(items), number_of_courses) 
        self.pb1 = ProgressBar(max=number_of_schedules)
        loadscreen = LoadingScreen( self.pb1, len(items), number_of_schedules, pos=(self.x, self.y) )
        self.schedule_layer.add_widget( loadscreen )
        self.schedules = self.schedule_generator( items, number_of_courses, self.pb1 )
        loadscreen.clear_widgets()
        self.schedule_layer.remove_widget( loadscreen )
    
    def __init__(self, bulletin=None, schedule_generator=lambda courses, N: [], *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.bulletin = bulletin

        self.schedule_generator = schedule_generator
        self.schedules = (i for i in xrange(0))#empty generator
        self.stored_schedules = []
        self.current_sched = None
        self.gen_sched = False
        self.schedule_index = -1
        self.schedule_generation_thread = threading.Thread( target=self.generation_object )

        self.on_touch_down = lambda e: exclusion.on_touch_down(self, e)
        self.on_touch_move = lambda e: exclusion.on_touch_move(self, e)
        self.on_touch_up = lambda e: exclusion.on_touch_up(self, e)

        self.active_button = None #for class-block popups
        self.create_layers()
        self.build_middle_layer()
        draw_window_frame(self.bottom_layer, (self.x, self.y) )
        draw_border(self.bottom_layer, (self.x, self.y) )

        Clock.schedule_interval(self.hold_checker, 1.0 / 120.0)
    
    def create_layers( self ):
        self.meta_layer       = FloatLayout()
        self.top_layer        = FloatLayout()
        self.middle_layer     = FloatLayout()
        self.bottom_layer     = FloatLayout()
        self.schedule_layer   = FloatLayout()
        self.user_event_layer = FloatLayout()
        self.my_layers = [ self.top_layer, self.meta_layer,   self.user_event_layer,  self.schedule_layer, 
                           self.middle_layer, self.bottom_layer ]
        for w in self.my_layers[::-1]: 
            self.add_widget( w )#The widget last added is last rendered.

    def build_middle_layer(self):
        self.clear_layer(self.middle_layer)
        self.in_exclusion_mode = False
        opacity = lambda (r,g,b,a): (r,g,b,0.50*a)
        slider_color = opacity(some_colors['steelblue1'])
        slider_w = 60
        slider_button = Button( background_color=slider_color, markup=True,
                                text='[color=000000][b]^[/b][/color]', on_press=self.slide_bottom_controls, 
                                pos=(self.x+w/2.0-slider_w/2.0, self.y+.15*h), size=(slider_w,40) )
        self.meta_layer.add_widget( slider_button )
        bottom_controls = GridLayout( cols=2,  pos=(self.x,self.y), size=(w,.15*h), spacing=(.01*w, .01*h), padding=(.01*w,.01*h), )
        self.exclude_button = ToggleButton( background_color=somet_colors['darkturquoise'], text="Exclude Times", 
                                            on_press=self.exclusion_mode )
        self.exclude_button.layout = None
        bottom_controls.add_widget(self.exclude_button)
        self.gen_button = Button( background_color=somet_colors['steelblue1'], text="Generate Schedules", 
                                  on_press=lambda button: self.generate_schedules() )
        bottom_controls.add_widget( self.gen_button )
        self.next_button = Button( background_color=somet_colors['indianred4'], text="Next Schedule", 
                                   on_press=lambda button : self.press_button(button),
                                   on_release=lambda button : self.release_button(button) )
        self.prev_button = Button( background_color=somet_colors['deepskyblue4'], text="Previous Schedule", 
                                   on_press=lambda button: self.press_button(button),
                                   on_release=lambda button : self.release_button(button) )
        bottom_controls.add_widget( self.prev_button )
        bottom_controls.add_widget( self.next_button )
        self.next_button.on, self.prev_button.on = False, False
        
        self.bottom_controls = bottom_controls
        self.meta_layer.add_widget( self.bottom_controls )
        self.slide_bottom_controls( slider_button )
        days = ['M','T','W','Th','F']
        for i in range(len( days )):
            day, x = days[i], i*XGAP
            button = ToggleButton( pos=(self.x + x, self.y + h-.05*h), size=(XGAP, .05*h), background_color=some_colors['indianred4'],
                             text=day,
                             on_press=lambda button : self.exclude_day(button))
            button.my_name = day
            button.layout = FloatLayout()
            self.middle_layer.add_widget( button )

    # Callbacks
    def slide_bottom_controls( self, button ):
        if self.bottom_controls.y == 0:
            y_slide = -1
        else:
            y_slide = 1
        new_y = self.bottom_controls.y + y_slide * self.bottom_controls.height
        anim1 = Animation(y=new_y, duration=.10)
        anim1.start( self.bottom_controls)
        anim2 = Animation(y=new_y + self.bottom_controls.height, duration=.10)
        anim2.start( button )

    def exclude_day(self, button):
        if not self.active_button:
            days = ['M','T','W','Th','F']
            self.bulletin.exclude_day(button.my_name)
            if self.bulletin.excluded_days[ button.my_name ]:
                button.layout = FloatLayout()
                with button.layout.canvas:
                    Color(1,1,1,.3)
                    Rectangle(pos=(self.x + XGAP*days.index( button.my_name ), self.y), 
                              size=(XGAP, h))
                self.middle_layer.add_widget(button.layout)
            else:
                self.middle_layer.remove_widget(button.layout)
        else:
            button.state = 'normal'

    def exclusion_mode(self, button):
        if not self.active_button:
            self.in_exclusion_mode = not self.in_exclusion_mode
            if self.in_exclusion_mode:
                self.parent.do_translation_x = False
            else:
                self.parent.do_translation_x = True
        else:
            if button.state == 'down':
                button.state = 'normal'
            else:
                button.state = 'down'

    def generate_schedules( self ):
        if not self.active_button:
            try:# How to terminate running thread?
                self.schedule_generation_thread.start()
            except RuntimeError:
                self.schedule_generation_thread = threading.Thread( target=self.generation_object )
                self.schedule_generation_thread.start()

    first = False
    WAIT, ACC = 0, 0

    def press_button( self, b ): 
        b.on = True
        self.first = True
        self.WAIT, self.ACC = .1, .005

    def release_button( self, b ):
        b.on = False    

    def hold_checker( self, dt ):
        self.WAIT -= self.ACC
        if self.WAIT > 0: time.sleep( self.WAIT )
        if self.first:#1 press and release equals 2 cycles. So minus 1.
            self.first = False
            return
        if self.next_button.on: 
            self.next_schedule()
        if self.prev_button.on: 
            self.previous_schedule()

    #Helpers
    def get_current_schedule( self ):
        return self.current_sched
    
    def iterate_schedules( self, step ):
        if self.active_button == None:
            self.schedule_index += step
            if self.schedule_index<0:
                self.schedule_index = 0 
            if self.schedule_index == 0 and len(self.stored_schedules) == 0: return
            elif self.schedule_index >= len(self.stored_schedules):
                try:
                    next_sched = self.schedules.next() 
                    self.stored_schedules += [next_sched]
                except StopIteration:
                    self.schedule_index = len(self.stored_schedules) - 1
                    return
            else:
                next_sched = self.stored_schedules[ self.schedule_index ]
            self.add_schedule( next_sched )
    
    def next_schedule( self ): self.iterate_schedules( 1 )
    def previous_schedule( self ): self.iterate_schedules( -1 )

    def clear_layer( self, layer ):
        layer.clear_widgets()

    def add_user_event(self, user_event):
        if not self.active_button:
            self.bulletin.add_user_event( user_event )
            self.clear_layer(self.user_event_layer)
            for ue in self.bulletin.get_user_events():
                self.add_course( ue.event_dict, self.user_event_layer )

    def add_schedule( self, sched ):
        self.clear_layer( self.schedule_layer )
        self.current_sched = sched
        online_days = ['M','T','W','Th','F']
        for section in sched:
            s = section.event_dict
            for i in range(len(s['Type'])):
                if s['Type'][i] not in ['LEC', 'LAB', 'PERS']:
                        s['Days'][i] = [online_days.pop()]
        for i in range(len(sched)):
            self.add_course( sched[i].event_dict, self.schedule_layer )

    def add_course( self, course_dict, layer ):
        time_data = zip(course_dict['Days'], course_dict['Times'], course_dict['Type'], course_dict['Location'])
        for d_list, t, ty, location in time_data:
            start, end = extract_times(t)
            self.add_blocks( d_list, start, end, ty, location, course_dict, layer )

    def add_blocks( self, d_list, start, end, ty, location, course_dict, layer ):
        try:
            for day in d_list:
                if day == 'TH': day ='Th'
                block = day, start, end, ty, location, course_dict
                add_block(self, block, layer)
        except:
            pass

