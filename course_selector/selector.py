import time, random
from global_environment import *
from course_selector import course_selector_layout
from course_popup1 import popup_window
from calvis3.calvis.scorer import course_waitlist_score

class Selector( FloatLayout ):
    def create_button( self, dicts, text ):
        sections = filter( lambda d: "{} : {}".format(d['Name'][0],d['Title'][0]) == text, dicts )
        random.shuffle( sections )
        sections = sorted( sections, key=course_waitlist_score, reverse=True)
        name = sections[0]['Name'][0]
        row = GridLayout( rows=1 )
        button = Button( text=text, on_press=self.press_button, on_release=self.release_button )
        # Bug: the nth course_added will always take the nth color. So delete course n-3, then add another course. Now there's a duplicate color.
        button.background_color = color_wheel[ len(self.course_labels.children) ] 
        button.v_x, button.v_y = 0,0
        button.sections = sections
        button.course_name = name
        button.switch_state = False
        row.add_widget( button )
        self.course_labels.add_widget( row )
        for s in button.sections: 
            #Add some keys to the course dictionaries.
            #This is a good place for it because all course dictionaries pass through here.
            s['my_color'] = button.background_color
            s['included_in_search'] = True
            s['old_included_in_search'] = True
            s['kept_section'] = False
            s['row_group'] = 0#len(self.course_labels.children) - 1
        self.update_course_ordering()

    def update_course_ordering(self):
        self.bulletin.selected_courses = []#get current ordering
        for i in range(len(self.course_labels.children)):
            row = self.course_labels.children[i]
            for course_button in row.children:
                self.bulletin.add_course( course_button.sections, i )

    def __init__(self, bulletin=None,
                 pos=(0,0), size=(0,0), 
                 offline_mode=False, courses=[], *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.bulletin = bulletin
        self.ox, self.oy = pos
        self.w, self.h = size
        draw_box( self, (self.ox, self.oy), (self.w,self.h), (0,0,1,1) )
        self.add_widget( course_selector_layout(self.create_button,
                                                size=(self.w, .35*self.h), pos=(self.ox, self.oy + .65*self.h), 
                                                offline_mode=offline_mode) )
        self.course_labels = GridLayout( size=(self.w, .65*self.h), pos=(self.ox, self.oy), cols=1,
                                         spacing=(0,self.h*.05), padding=[.05*w, .2*h, .05*w, .02*h])
        self.add_widget( self.course_labels )
        if offline_mode: #Manually populate course_labels.
            course_names = set( map( lambda c: "{} : {}".format(c['Name'][0],c['Title'][0]), courses ) )
            for course_name in course_names:
                self.create_button( courses, course_name )
        self.in_priority_mode = False
        self.shakers = []
        self.active_button = None
        self.activation_time = 0
        self.moving_button = False
        self.popped = None
        Clock.schedule_interval(self.hold_checker, 1/20)
        self.start_time = time.time()

    def press_button( self, button ):
        self.activation_time = time.time()
        self.active_button = button

    def release_button( self, button ):
        if time.time() - self.activation_time <= 1.5:
            if (not self.popped and not self.in_priority_mode) or self.popped == button: 
                popup_window(self, button, button.sections)
        self.active_button = None
        self.activation_time = 0
        self.moving_button = False

    def remove_course_from_selected( self, course_name ):
        self.bulletin.remove_course( course_name )
        for row in self.course_labels.children:
            for course_button in row.children:
                if course_name == course_button.course_name:
                    row.remove_widget( course_button )
                    if len(row.children) < 1:
                        self.course_labels.remove_widget( row )
                    self.press_button( course_button )#Emulate a course_button press.
                    self.release_button( course_button )

    def hold_checker(self, dt):
        if self.active_button and time.time() - self.activation_time > 1.0:
            if not self.in_priority_mode:
                self.shakers = reduce( lambda x,y: x+y,
                                       map( lambda row: row.children, self.course_labels.children ))
                self.in_priority_mode = True
                Clock.schedule_interval( self.prioritize_mode, 1/10 ) 
                self.parent.do_translation = False
                self.parent.do_scale = False
    
    def on_touch_down( self, e ):
        super(type(self), self).on_touch_down(e)
        if self.in_priority_mode:
            if e.is_double_tap:
                self.in_priority_mode = False
                Clock.unschedule( self.prioritize_mode ) 
                for button in self.shakers:
                    button.x, button.y = button.x - button.v_x, button.y - button.v_y
                self.parent.do_translation = True
                self.parent.do_scale = True
                self.bulletin.selected_courses = []#get current ordering
                rows = self.course_labels.children
                for i in range(len(rows)):
                    for button in rows[i].children:
                        self.bulletin.add_course( button.sections, i )

    def on_touch_move( self, e ):
        super(type(self), self).on_touch_move(e)
        if self.in_priority_mode:
            if self.active_button:
                button = self.active_button
                button.x, button.y = button.x - button.v_x, button.y - button.v_y
                self.moving_button = True
                self.active_button.x += e.dx
                self.active_button.y += e.dy

    def on_touch_up( self, e ):
        super(type(self), self).on_touch_up(e)
        if self.in_priority_mode:
            if self.active_button:
                for row in self.course_labels.children:
                    if row.collide_widget( self.active_button ):
                        self.active_button.parent.remove_widget( self.active_button )
                        row.add_widget( self.active_button )
                        return 

    def prioritize_mode( self, dt ):
        for button in self.shakers:
            if self.moving_button and self.active_button and button == self.active_button:
                continue
            button.x, button.y = button.x - button.v_x, button.y - button.v_y
            button.v_x, button.v_y = random.random()*2 - 1, random.random()*2 - 1
            button.x, button.y = button.x + button.v_x, button.y + button.v_y
        
