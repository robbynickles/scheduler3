from global_environment import w,h

days = ['M','T','W','Th','F']
hrs = ['12'] + [str(x+1) for x in range(11)]
XGAP, YGAP = float(w)/len(days), float(h)/(2*len(hrs))
def cal_map(day, time): 
    """(day, time) --> (x,y),
    where day is a work-week day and time is something like 6 31 AM."""
    try:
        hr, m, meridiem = time.split(' ')
        m = float(m)
        return XGAP*days.index(day), \
            h - (YGAP*hrs.index(hr) + m/60.0*YGAP + 12*YGAP*int(meridiem == 'PM'))
    except:
        pass

def inverse_cal_map(x, y):
    """(x,y) --> (day, time),
    where day is a work-week day and time is like 6 31 AM."""
    day = days[int(x) / int(XGAP)]
    rev_hrs = hrs[::-1]
    hr = (rev_hrs+rev_hrs)[(int(y)) / int(YGAP)]
    m = ((h - int(y)) % int(YGAP) / YGAP) * 60
    meridiem = 'AM' if int(y) / int(YGAP) >= len(hrs) else 'PM'
    return day, "{} {} {}".format(hr, '0'+str(int(m)) if 0<=m<10 else int(m), meridiem)

def label_offset((x, y)): 
    """The coordinates of labels are offset."""
    XOFF, YOFF = -30, -40
    return x + XOFF, y + YOFF

def convert_time( t ):
    t = t.split(":")#'06:40A'-->['06','40A']
    hr, m, meridiem = str(int(t[0])), t[1][:2], t[1][2]
    meridiem = 'AM' if meridiem == 'A' else 'PM'
    return " ".join([hr, m, meridiem])

def extract_times( time_string ):
    """ 06:40A - 12:45P --> 6 40 AM, 12 45 PM """
    try:
        return map(convert_time, time_string.split('-'))
    except:
        return '6 00 AM', '6 00 AM'
    
