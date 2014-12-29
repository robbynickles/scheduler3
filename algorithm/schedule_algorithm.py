import random
from itertools import combinations
from helpers import * 

from big_chunk import number_of_courses as N
from big_chunk import courses_selected as courses

def compatible( (sectionA, sectionB) ):
    return \
        name(sectionA.event_dict) != name(sectionB.event_dict) and \
        sectionA.event_dict['row_group'] != sectionB.event_dict['row_group'] and \
        not sectionA.overlap_with_section( sectionB ) 

def key_map( section_list ): 
    """Map the section list to a suitable dictionary key."""
    return tuple(map(lambda s: section(s.event_dict), section_list))

def generate_schedules(items, N, progressbar):
    valid = {}
    for sched in ( (sectionA, sectionB) for sectionA, sectionB in combinations( items, 2 ) ):
        valid[ key_map(sched) ] = compatible( sched ) 
    progressbar.value = 0
    for sched in ( sched for j in range( 3, N + 1 ) for sched in combinations( key_map(items), j ) ):
        progressbar.value += 1
        valid[ sched ] = valid[ sched[1:] ] and valid[ sched[:-1] ] and valid[ (sched[0], sched[-1]) ]
    def generator():
        for j in xrange(N, 0, -1):
            for schedule in combinations( items, j ):
                if len(schedule)==1 or valid[ key_map(schedule) ]:
                    yield schedule
    return generator()


