import sys
#OFFLINE_MODE = len(sys.argv) > 1 and sys.argv[1] == 'offline'  
OFFLINE_MODE = True
from algorithm.schedule_algorithm import courses
from algorithm.schedule_algorithm import generate_schedules
from course_selector.selector import Selector
from calvis3.calvis.calvis import Calender
from utility.bulletin1 import Bulletin
from kivy.uix.scatter import ScatterPlane
from kivy.base import runTouchApp
from global_environment import w,h

bulletin = Bulletin()
calender = Calender( bulletin=bulletin, schedule_generator=generate_schedules )
selector = Selector( bulletin=bulletin, size=(w, h), pos=(-1.2*w, 0), 
                     offline_mode=OFFLINE_MODE, courses=courses if OFFLINE_MODE else [])

page1, page2 = selector, calender
root = ScatterPlane(do_rotation=False, do_translation_y=False, do_scaling=False)
root.add_widget( page1 )
root.add_widget( page2 )
root.apply_transform( root.transform.inverse().translate(1.2*w, 0, 0) )# Start on page 1.
runTouchApp( root )
