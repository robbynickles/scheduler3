from helpers import *
from data_objects import Section, Course
from calvis3.scorer import course_waitlist_score

class Bulletin():
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
        return map( lambda c: filter( lambda s: s.event_dict['included_in_search'], c ),
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

    def by_group( self, section ):
        return section.event_dict['row_group']

    def get_sections_selected( self ):
        def exclusion_filter(section):
            return \
                self.compatible_with_excluded_days(section) and \
                self.compatible_with_user_events(section)
        ret = map( lambda c: filter(exclusion_filter, c), self.get_included_sections() )
        for i in range(len(ret)):
            if len(ret[i]) >= 10:#If over 10 sections in a course, only give the top-10 waitlists.
                ret[i] = sorted(ret[i], key=course_waitlist_score, reverse=True)[:10]
        return sorted( reduce( lambda x,y: x+y, ret ), key=self.by_group )
        

