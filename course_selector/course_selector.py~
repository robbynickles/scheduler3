from utilkit import find_and_destroy_widget
from global_environment import *

def course_selector_layout( callout, size=(0,0), pos=(0,0), offline_mode=False ):
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
        set_school_value( text )
        term_spinner.values =   get_term_labels()
        department_spinner.values = get_subject_labels()

    def term_selected(spinner, text): 
        set_term_value(text)
        
    def dept_selected(spinner, text): 
        set_subject_value(text)
        submit_form()

    def wrapper(): 
        wrapper.dictionaries = []

    def course_selected( spinner, text ):
        if text != 'This department offers no courses for the selected term.': 
            callout( wrapper.dictionaries, text )

    def get_number(name):
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        s = name.split(':')[0].split('-')[1].strip()
        if s.isdigit():
            return int(s)
        else: # something like 1C goes to 1+3=4
            return int(s[:-1]) + alpha.index(s[-1].lower())

    def submit_form(): 
        wrapper.dictionaries = submit_HTMLform()
        name = lambda d: "{} : {}".format(d['Name'][0],d['Title'][0])
        course_spinner.values = sorted(set(map(name, wrapper.dictionaries)), key=get_number)

    school_spinner     = make_spinner_with_values( get_school_labels(), 'School', 'school', 
                                                   some_colors['darkturquoise'], school_selected )
    term_spinner       = make_spinner_with_values( [], 'Term', 'term', 
                                                   some_colors['steelblue1'], term_selected )
    department_spinner = make_spinner_with_values( [], 'Department', 'department', 
                                                   some_colors['indianred4'], dept_selected )
    course_spinner     = make_spinner_with_values( [], 'Course', 'subject', 
                                                   some_colors['deepskyblue4'], course_selected )

    return layout

