from utility.helpers import getavail, strToFloats

def day_density( time_list ):
    if len(time_list) > 0:
        starts, ends = zip(*sorted(map(strToFloats, time_list))) 
        starts, ends = sorted(starts), sorted(ends)
        time_spread = ends[-1] - starts[0]
        return 800 / time_spread
    else:
        return 1000#empty day

def get_time(cal, d):
    try:
        return cal[d]
    except:
        return []

def density( schedule ):
    density, wcals = 0, map( lambda c: c.weekly_calender, schedule )
    for d in ['M','T','W','Th','F']:
        time_list = reduce( lambda x,y: x+y, map( lambda cal: get_time( cal, d ), wcals ) )
        density += day_density( time_list )
    return density

def course_waitlist_score( course ):
    try:
        avail = getavail( course.event_dict ).lower()
    except:
        avail = getavail( course ).lower()
    if 'open' in avail:
        if 'waitlist' in avail:
            return 300
        else:
            return 1000
    else:
        try:#Usually something like 'Wait/3' ---> 'Wait','3'
            x, n = avail.split('/')
            return -(10*int(n)**3)
        except:
            return 0

def waitlist_score( schedule ): 
    return sum( map( course_waitlist_score, schedule ) )
    
def score_schedule( schedule ): 
    return waitlist_score( schedule ) + density( schedule )

def sort( schedules ): 
    return sorted( schedules, key=score_schedule, reverse=True )

        
