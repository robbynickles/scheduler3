from itertools import combinations
from helpers import * 
from calvis3.calvis.scorer import course_waitlist_score
import random

def compatible( sectionA, sectionB ):
    return \
        name(sectionA.event_dict) != name(sectionB.event_dict) and \
        sectionA.event_dict['row_group'] != sectionB.event_dict['row_group'] and \
        not sectionA.overlap_with_section( sectionB ) 

def generate_schedules(courses_selected, number_of_courses_selected, PB1, PB2):
    #random.shuffle(courses_selected)
    items = courses_selected 
    N = number_of_courses_selected
    section_object_doubles = [ (sectionA, sectionB) for sectionA, sectionB in combinations( items, 2 ) ]
    section_numbers = map( lambda s: section(s.event_dict), items )
    all_section_numbers_no_doubles = [ sched for j in range( 3, N + 1 ) for sched in combinations( section_numbers, j ) ]

    valid = {}
    for sched in section_object_doubles:
        valid[ tuple(map(lambda s: section(s.event_dict), sched)) ] = compatible(*sched) 
    PB1.value = 0
    for i in range(len(all_section_numbers_no_doubles)):
        PB1.value = int(float(i)/len(all_section_numbers_no_doubles) * PB1.max)
        schedule = all_section_numbers_no_doubles[i]
        valid[ schedule ] = valid[ schedule[1:] ] and valid[ schedule[: -1] ] and valid[ (schedule[0], schedule[-1]) ]
    
    isValid = lambda schedule: valid[ tuple(map(lambda s: section(s.event_dict), schedule)) ]

    def generator():
        for j in xrange(N, 0, -1):
            for schedule in combinations( items, j ):
                if len(schedule)==1 or isValid(schedule):
                    yield schedule
    return generator()

from big_chunk import number_of_courses as N
from big_chunk import courses_selected as courses

#courses = [{'Name': ['MCHEM-112'], 'Title': ['Organic Chemistry 1', '08/25/14-12/13/14'], 'Section': ['3124'], 'Days': [['M'], ['M', 'W'], ['T']], 'Times': ['02:50P - 03:55P', '11:40A - 01:05P', '07:20A - 11:30A'], 'Avail': ['Wait/2'], 'Location': ['MSCC 305, West', 'MSCC 314, West', 'MSCC 324, West'], 'Units': ['5'], 'Instructor': ['Roslanie, Mar'], 'Type': ['LEC', 'LEC', 'LAB'], 'Important Notes': [''], 'Max/': ['16/0']}, {'Name': ['MCHEM-112'], 'Title': ['Organic Chemistry 1', '08/25/14-12/13/14'], 'Section': ['3126'], 'Days': [['M', 'W'], ['M'], ['TH']], 'Times': ['11:40A - 01:05P', '02:50P - 03:55P', '07:20A - 11:30A'], 'Avail': ['Wait/2'], 'Location': ['MSCC 314, West', 'MSCC 305, West', 'MSCC 324, West'], 'Units': ['5'], 'Instructor': ['Roslanie, Mar'], 'Type': ['LEC', 'LEC', 'LAB'], 'Important Notes': [''], 'Max/': ['16/0']}, {'Name': ['MEASCI-162'], 'Title': ['Intro to Oceanography', '08/25/14-12/13/14'], 'Section': ['4667'], 'Days': [['M', 'W'], ['M', 'W']], 'Times': ['10:05A - 11:30A', '11:40A - 01:05P'], 'Avail': ['Wait/12'], 'Location': ['MSCC 322, West', 'MSCC 322, West'], 'Units': ['4'], 'Instructor': ['Hughes, Noa'], 'Type': ['LEC', 'LAB'], 'Important Notes': [''], 'Max/': ['24/1']}, {'Name': ['MMATH-171'], 'Title': ['Calculus: First Course', '08/25/14-12/13/14'], 'Section': ['2237'], 'Days': [['M', 'W', 'F']], 'Times': ['07:50A - 09:25A'], 'Avail': ['Open'], 'Location': ['MFND 151, East'], 'Units': ['5'], 'Instructor': ['Jarrett, Elz'], 'Type': ['LEC'], 'Important Notes': [''], 'Max/': ['38/8']}, {'Name': ['MMATH-171'], 'Title': ['Calculus: First Course', '08/25/14-12/13/14'], 'Section': ['2245'], 'Days': [['M', 'T', 'W', 'TH']], 'Times': ['01:15P - 02:25P'], 'Avail': ['Wait/17'], 'Location': ['MSCC 325, West'], 'Units': ['5'], 'Instructor': ['Cripe, Pau'], 'Type': ['LEC'], 'Important Notes': [''], 'Max/': ['38/0']}, {'Name': ['MMATH-171'], 'Title': ['Calculus: First Course', '08/25/14-12/13/14'], 'Section': ['4673'], 'Days': [['M', 'T', 'W', 'TH']], 'Times': ['01:15P - 02:25P'], 'Avail': ['Wait/24'], 'Location': ['MSER B133, West'], 'Units': ['5'], 'Instructor': ['Payvar, Kam'], 'Type': ['LEC'], 'Important Notes': [''], 'Max/': ['38/1']}, {'Name': ['MHIST-119'], 'Title': ['Hist 20th Century America', '08/25/14-12/13/14'], 'Section': ['4546'], 'Days': [['T', 'TH']], 'Times': ['02:20P - 03:45P'], 'Avail': ['Open'], 'Location': ['MFND 134, East'], 'Units': ['3'], 'Instructor': ['Kehoe, Mic'], 'Type': ['LEC'], 'Important Notes': [''], 'Max/': ['40/10']}]


# Tests    
if __name__ == '__main__':
    course_dict = {'Name': ['MCHEM-101'], 'Title': ['General Chemistry 1', '08/25/14-12/13/14'], 'Section': ['1704'], 'Days': [['W'], ['F'], ['M'], ['TH']], 'Times': ['11:40A - 01:05P', '01:40P - 02:30P', '11:40A - 12:45P', '08:25A - 11:30A'], 'Avail': ['Wait/11'], 'Location': ['MSCC 114, West', 'MSCC 305, West', 'MSCC 114, West', 'MSCC 312, West'], 'Units': ['5'], 'Instructor': ['Maki, Lau'], 'Type': ['LEC', 'LEC', 'LAB', 'LAB', 'DINT'], 'Important Notes': ['HYBRID.  Part of Lecture is online.  Required on-campus lecture and laboratory class attendance.  Contact instructor makil@mjc.ed   u'], 'Max/': ['24/2']}
    course_dict2 = {'Name': ['MPHYS-102'], 'Title': ['Ge\
neral Phys: Waves, Ther & Op', '08/25/14-12/13/14'], 'Section': ['3712'], 'Days': [['T', 'TH'], ['T'], ['T']], 'Times': [\
'11:40A - 01:05P', '02:50P - 03:40P', '03:50P - 06:55P'], 'Avail': ['Open'], 'Location': ['MSCC 351, West', 'MSCC 311, We\
st', 'MSCC 311, West'], 'Units': ['5'], 'Instructor': ['Gariety, Mic'], 'Type': ['LEC', 'LEC', 'LAB'], 'Important Notes':\
 [''], 'Max/': ['24/7']}
    
    from time import time

    N = 4
    print "Building valid schedules from {} different sections:".format(len(courses))
    for n in set(map(name, courses)):
        print "     {} different {} sections.".format(map(name, courses).count(n), n)
    t1 = time()
    valid_schedules = generate_schedules(courses, N)
    t2 = time() 
    print "Found {} different {}-course valid schedules in {} seconds.".format(len(valid_schedules), len(valid_schedules[0]), t2-t1)
    """t = time()
    while time() - t < 5: pass
    for sched in valid_schedules:
        print "#" * 100
        for course in sched:
            print name(course), days(course), times(course)
    """
