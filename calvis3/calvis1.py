from global_environment import *
from cal_popup import add_block
from algorithm.helpers import overlap
import scorer
import exclusion
import threading
from kivy.uix.progressbar import ProgressBar
from loadingscreen import LoadingScreen

class Calender(FloatLayout):
    def generation_object( self ):
        self.clear_layer(self.schedule_layer)
        self.stored_schedules = []
        self.schedule_index = -1
        items = self.bulletin.get_sections_selected()
        number_of_courses = len(self.bulletin.selected_courses)
        loadscreen = LoadingScreen( self.pb1 ) 
        self.schedule_layer.add_widget( loadscreen )
        self.schedules = self.schedule_generator( items, number_of_courses, self.pb1, self.pb2  )
        self.schedule_layer.remove_widget( loadscreen )
    
    def __init__(self, bulletin=None, schedule_generator=lambda courses, N: [], *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.bulletin = bulletin
        self.schedule_generator = schedule_generator
        self.schedules = []
        self.stored_schedules = []
        self.gen_sched = False
        self.schedule_index = -1
        self.schedule_generation_thread = threading.Thread( target=self.generation_object )
        self.on_touch_down = lambda e: exclusion.on_touch_down(self, e)
        self.on_touch_move = lambda e: exclusion.on_touch_move(self, e)
        self.on_touch_up = lambda e: exclusion.on_touch_up(self, e)
        self.active_button = None #for class-block popups
        self.create_layers()
        self.pb1 = ProgressBar(max=1000)
        self.pb2 = ProgressBar(max=1000, pos=(w/2,0))
        self.top_layer.add_widget( self.pb1 ) 
        #self.top_layer.add_widget( self.pb2 ) 
        self.build_middle_layer()
        draw_window_frame(self.bottom_layer)
        draw_border(self.bottom_layer)
        hold_hz = 7.0
        Clock.schedule_interval(self.hold_checker, 1.0 / hold_hz)
    
    def create_layers( self ):
        self.top_layer = FloatLayout()
        self.middle_layer = FloatLayout()
        self.bottom_layer = FloatLayout()
        self.schedule_layer = FloatLayout()
        self.user_event_layer = FloatLayout()
        self.my_layers = [ self.top_layer, self.user_event_layer, self.schedule_layer, 
                           self.middle_layer, self.bottom_layer ]
        for w in self.my_layers[::-1]: 
            self.add_widget( w )#The widget last added is last rendered.

    def build_middle_layer(self):
        self.clear_layer(self.middle_layer)
        self.in_exclusion_mode = False
        bottom_controls = GridLayout(cols=2, pos=(0,0), size=(w, .1*h) )
        self.exclude_button = ToggleButton( background_color=some_colors['darkturquoise'], text="Exclude Times", 
                                            on_press=lambda button : self.exclusion_mode() )
        self.exclude_button.layout = None
        bottom_controls.add_widget(self.exclude_button)
        self.gen_button = Button( background_color=some_colors['steelblue1'], text="Generate Schedules", 
                                  on_press=lambda button: self.generate_schedules() )
        bottom_controls.add_widget( self.gen_button )
        self.next_button = Button( background_color=some_colors['indianred4'], text="Next Schedule", 
                                   on_press=lambda button : self.press_button(button),
                                   on_release=lambda button : self.release_button(button) )
        self.prev_button = Button( background_color=some_colors['deepskyblue4'], text="Previous Schedule", 
                                   on_press=lambda button: self.press_button(button),
                                   on_release=lambda button : self.release_button(button) )
        bottom_controls.add_widget( self.prev_button )
        bottom_controls.add_widget( self.next_button )
        self.next_button.on, self.prev_button.on = False, False
        self.middle_layer.add_widget( bottom_controls )
        days = ['M','T','W','Th','F']
        for i in range(len( days )):
            day, x = days[i], i*XGAP
            button = ToggleButton( pos=(x, h-.05*h), size=(XGAP, .05*h), background_color=some_colors['indianred4'],
                                   text=day,
                                   on_press=lambda button : self.exclude_day(button))
            button.my_name = day
            button.layout = FloatLayout()
            self.middle_layer.add_widget( button )

    # Callbacks
    def exclude_day(self, button):
        days = ['M','T','W','Th','F']
        self.bulletin.exclude_day(button.my_name)
        if self.bulletin.excluded_days[ button.my_name ]:
            button.layout = FloatLayout()
            with button.layout.canvas:
                Color(1,1,1,.3)
                Rectangle(pos=(XGAP*days.index( button.my_name ),.1*h), 
                          size=(XGAP, .9*h))
            self.top_layer.add_widget(button.layout)
        else:
            self.top_layer.remove_widget(button.layout)

    def exclusion_mode(self):
        self.in_exclusion_mode = not self.in_exclusion_mode
        if self.in_exclusion_mode:
            self.parent.do_scale, self.parent.do_translation = False, False
        else:
            self.parent.do_scale, self.parent.do_translation = True, True
        
    def generate_schedules( self ):
        number_of_courses = len(self.bulletin.selected_courses)
        if number_of_courses > 1:
            try:
                self.schedule_generation_thread.start()
            except RuntimeError:
                self.schedule_generation_thread = threading.Thread( target=self.generation_object )

    def press_button( self, b ): b.on = True
    def release_button( self, b ): b.on = False    

    def hold_checker( self, dt ):
        if self.next_button.on: self.next_schedule()
        if self.prev_button.on: self.previous_schedule()

    #Helpers
    def iterate_schedules( self, step ):
        if 0 <= step + self.schedule_index <= len(self.stored_schedules) and \
           self.active_button == None:
            self.schedule_index = step + self.schedule_index 
            if self.schedule_index == len(self.stored_schedules):
                try:
                    next_sched = self.schedules.next() 
                    self.stored_schedules += [next_sched]
                except StopIteration:
                    return
            else:
                next_sched = self.stored_schedules[ self.schedule_index ]
            self.add_schedule( next_sched )
    
    def next_schedule( self ): self.iterate_schedules( 1 )
    def previous_schedule( self ): self.iterate_schedules( -1 )

    def clear_layer( self, layer ):
        layer.clear_widgets()

    def add_user_event(self, user_event):
        self.bulletin.add_user_event( user_event )
        self.clear_layer(self.user_event_layer)
        for ue in self.bulletin.get_user_events():
            self.add_course( ue.event_dict, self.user_event_layer )

    def add_schedule( self, sched ):
        self.clear_layer( self.schedule_layer )
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

