import sys
#OFFLINE_MODE = len(sys.argv) > 1 and sys.argv[1] == 'offline'  
OFFLINE_MODE = True
from algorithm.schedule_algorithm import courses
from algorithm.schedule_algorithm import generate_schedules
from course_selector.selector import Selector
from calvis3.calvis import Calender
from map_page1 import MapPage
from utility.bulletin1 import Bulletin
from swipeplane2 import SwipePlane
from kivy.base import runTouchApp
from global_environment import w,h

bulletin = Bulletin()
selector = Selector( bulletin=bulletin, size=(w, h), pos=(0, 0), 
                     offline_mode=OFFLINE_MODE, courses=courses if OFFLINE_MODE else [])
calender = Calender( bulletin=bulletin, schedule_generator=generate_schedules, pos=( 1.2*w, 0) )
map_page = MapPage(  calender=calender, size=(w, h), pos=( 2*1.2*w, 0) )

pages = selector, calender, map_page
root = SwipePlane()
for page in pages:
    root.add_page( page )

runTouchApp( root )
