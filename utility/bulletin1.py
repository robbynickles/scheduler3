from helpers import *
from data_objects import Section, Course
from calvis3.scorer import course_waitlist_score

class Bulletin():
    """A Bulletin object is used to  store and manipulate course information.
    Different parts of the GUI are connected here. When a user makes course inclusions or exclusions,
    the GUI communicates the changes to here. Then, when schedules are generated, the list of courses
    plus any user inclusions/exclusions comes from here.
    """
    selected_courses = []
    user_events = []
    excluded_days = dict( zip( ['M','T','W','Th','F'], [False] * 5 ) )
    def find_course( self, course_name ):
        for course in self.selected_courses:
            if course.name == course_name:
                return course
    def exclude_day( self, day ):
        try:
            self.excluded_days[ day ] = not self.excluded_days[ day ]
        except:
            pass
    def add_course( self, sections, row_group ):
        course_name = getname(sections[0])
        self.selected_courses += [ Course( course_name, sections, row_group ) ]
    def remove_course( self, course_name ):
        self.selected_courses.remove( self.find_course( course_name ) )
    def include_section( self, section_dict ):
        course_name, section_number = getname( section_dict ), getsection( section_dict )
        self.find_course( course_name ).include_section( section_number )
    def exclude_section( self, section_dict ):
        course_name, section_number = getname( section_dict ), getsection( section_dict )
        self.find_course( course_name ).exclude_section( section_number )
    def exclude_all_but( self, section_dict, state ):
        course = self.find_course( getname(section_dict) )
        course.exclude_all_but(section_dict, state )
    def add_user_event( self, user_event ):
        self.user_events += [ Section(user_event) ]
    def remove_user_event( self, ID ):
        for ue in self.user_events:
            if ue.event_dict['ID'] == ID:
                self.user_events.remove( ue )
                return
    def get_user_events( self ):
        return self.user_events
    def get_included_sections( self ):
        """ ---> ( A, B ) == ( (a1,a2), (b1,b2) )  
        where A and B are lists of sections for the same course included in the search.
        """
        exclusion_filter = lambda section: \
                           self.compatible_with_excluded_days(section) and \
                           self.compatible_with_user_events(section) and \
                           section.event_dict['included_in_search']
        return map( lambda section_list: filter( exclusion_filter, section_list ),
                    map( lambda c: c.sections, self.selected_courses ) )
    def get_excluded_sections( self ):
        return filter( lambda s: not s.event_dict['included_in_search'],
                       reduce( lambda x,y: x+y, 
                               map( lambda c: c.sections, self.selected_courses )))
    def compatible_with_excluded_days( self, section ):
        ed_set = set(filter(lambda d: self.excluded_days[d], self.excluded_days.keys()))
        sd_set = set(section.weekly_calender.keys())
        return len( ed_set.intersection( sd_set ) ) == 0

    def compatible_with_user_events( self, section ):
        for user_event in self.get_user_events():
            if section.overlap_with_section( user_event ):
                return False
        return True

    def by_group( self, section ): return section.event_dict['row_group']

    def get_sections_selected( self ):
        """The main access point to selected courses. This is called to supply the list
        of sections to the schedule generation function.
        """
        ret = self.get_included_sections() 
        CAP = 10
        for i in range(len(ret)):
            if len(ret[i]) >= CAP:#If over CAP sections in a course, only give the top-CAP waitlists.
                ret[i] = sorted(ret[i], key=course_waitlist_score, reverse=True)[:CAP]
        try:
            return sorted( reduce( lambda x,y: x+y, ret ), key=self.by_group )
        except TypeError: # ret is empty
            return []
        

