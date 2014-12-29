from helpers import *

class Section():
    def __init__(self, event_dict):
        self.event_dict = event_dict
        self.weekly_calender = weekly_calender( event_dict )
    def overlap( self, day, time ):
        try:
            times = self.weekly_calender[day]
            for t in times:
                if overlap(t, time):
                    return True
            else:
                return False
        except:
            False
    def overlap_with_section( self, section ):
        shared_days = set(self.weekly_calender.keys()).intersection(set(section.weekly_calender.keys()))
        for day in shared_days:
            for time in section.weekly_calender[day]:
                if self.overlap( day, time ):
                    return True
        return False
            
class Course():
    def __init__(self, name, sections, row_group):
        self.name = name
        self.sections = []
        for s in sections:
            s['row_group'] = row_group
            self.sections += [Section( s )]

    def find_section( self, section_number ):
        for s in self.sections:
            if getsection(s.event_dict) == section_number:
                return s
        else:
            return {}

    def exclude_all_but(self, section_dict, state):
        if state == 'down':
            for s in self.sections: 
                s.event_dict['old_included_in_search'] = s.event_dict['included_in_search'] 
                s.event_dict['included_in_search'] = False
            section_dict['included_in_search'] = True
            section_dict['kept_section'] = True
        else:
            for s in self.sections:
                s.event_dict['included_in_search'] = s.event_dict['old_included_in_search']
            section_dict['kept_section'] = False

    def include_section( self, section_number ):
        self.find_section( section_number ).event_dict['included_in_search'] = True
    def exclude_section( self, section_number ):
        self.find_section( section_number ).event_dict['included_in_search'] = False

