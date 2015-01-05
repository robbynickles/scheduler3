from utilkit import find_and_destroy_widget
from global_environment import *
import threading

class LoadingScreen( FloatLayout ):
    def populate(self, text):
        flay = FloatLayout()
        with flay.canvas:
            Color(0,0,0,.7)
            Rectangle( pos=(-1.2*w,0), size=(w,h) )
        self.add_widget( flay )
        text = text.split(':')[1]
        self.text_of_label = "Retrieving {} courses".format( text )
        self.ellipsis = ""
        self.label = Label( center=(-1.2*w + w/2,h/2 + 30) )
        self.add_widget( self.label )

    def update_label( self, dt ):
        if self.ellipsis == ". . . . . ":
            self.ellipsis = ""
        self.ellipsis += ". "
        self.label.text = self.text_of_label + self.ellipsis


def course_selector_layout( parent, callout, size=(0,0), pos=(0,0), offline_mode=False ):
    if offline_mode:
        from offline.session import \
            get_school_labels, set_school_value, \
            get_term_labels,    set_term_value, \
            get_subject_labels, set_subject_value, \
            submit_HTMLform
    else:
        from scrapekit.session import \
            get_school_labels, set_school_value, \
            get_term_labels,    set_term_value, \
            get_subject_labels, set_subject_value, \
            submit_HTMLform
        
    layout = GridLayout(cols=1, pos=pos, size=size )
    
    def make_spinner_with_values( values, text, id, color, callback ): 
        spinner = Spinner(text=text, values=values, id=id, background_color=color)
        find_and_destroy_widget( layout, id )
        spinner.bind(text=callback)
        layout.add_widget( spinner )
        return spinner

    def school_selected( spinner, text ):
        if 'Please' not in text and len(text)>0:
            set_school_value( text )
            term_spinner.values =   get_term_labels()
            department_spinner.values = [ 'Please select a term first.' ]
            course_spinner.values     = [ 'Please select a term first.' ]

    semester_courses = []
    load_screen = LoadingScreen()
    def term_selected(spinner, text): 
        if 'Please' not in text:
            set_term_value(text)
            load_screen.populate( text )
            parent.add_widget( load_screen )
            Clock.schedule_interval( load_screen.update_label, 1/3.0 )
            threading.Thread( target=submit_form ).start()

    def submit_form(): 
        global semester_courses
        semester_courses = submit_HTMLform() #The dictionary of all departments, with their courses, with their sections.
        department_spinner.values = [ dept['name'] for dept in semester_courses ]
        Clock.unschedule( load_screen.update_label )
        load_screen.clear_widgets()
        parent.remove_widget( load_screen )
        
    def dept_selected(spinner, text): 
        name = lambda d: "{} : {}".format(d['Name'][0],d['Title'][0])
        sections = []
        for dept in semester_courses:
            if dept['name'] == text:
                for course in dept['courses']:
                    sections += course['sections']
        course_spinner.values = sorted(set(map(name, sections)), key=get_number)

    def course_selected( spinner, text ):
        if text != 'This department offers no courses for the selected term.' and \
           'Please' not in text:
            # Send out a list of all sections from the currently selected departement 
            # and the name of the course selected.
            for dept in semester_courses:
                if dept['name'] == department_spinner.text:
                    for course in dept['courses']:
                        if course['name'] in text:
                            course_sections = course['sections']
            callout( course_sections,  text ) 

    def get_number(name):
        s = name.split(':')[0].split('-')[1].strip()
        if s.isdigit():
            return int(s)
        else: # something like 1C goes to 1+2=3
            alpha = 'abcdefghijklmnopqrstuvwxyz'
            try:
                return int(s[:-1]) + alpha.index(s[-1].lower())
            except ValueError:
                try:
                    return int(s[:-2]) + alpha.index(s[-2].lower()) + alpha.index(s[-1].lower())
                except:
                    print "{} caused an error.".format( s )
                    return 0

    school_spinner     = make_spinner_with_values( get_school_labels(), 'School', 'school', 
                                                   some_colors['darkturquoise'], school_selected )
    term_spinner       = make_spinner_with_values( ['Please select a school first.'], 'Term', 'term', 
                                                   some_colors['steelblue1'], term_selected )
    department_spinner = make_spinner_with_values( ['Please select a school first.'], 'Department', 'department', 
                                                   some_colors['indianred4'], dept_selected )
    course_spinner     = make_spinner_with_values( ['Please select a school first.'], 'Course', 'subject', 
                                                   some_colors['deepskyblue4'], course_selected )

    return layout

