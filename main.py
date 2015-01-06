import sys
#OFFLINE_MODE = len(sys.argv) > 1 and sys.argv[1] == 'offline'  
OFFLINE_MODE = False
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

#import cProfile
from kivy.app import App
class MyApp(App):
    """
    def on_start(self):
        self.profile = cProfile.Profile() 
        self.profile.enable()
    """
    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass
    """
    def on_stop(self):
        self.profile.disable() 
        self.profile.dump_stats('myapp.profile')
    """
    def build(self):
        return root

MyApp().run()
