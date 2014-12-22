import traceback
def normal_find( lst, pat ): return lst.index( pat )

def compress( lst, start, end, replacement=None ):
    s = ""
    try:
        for i in range(end - 1, start - 1, -1):
            s = str(lst.pop(i)) + s
    except TypeError:
        print start, end
        print lst
        print traceback.format_exc()#more informative error log

    if replacement != None: 
        s = replacement
    lst.insert( start, s )

def itemcompress( lst, start, end, startoffset=0, endoffset=0, fill=" ", \
                      startfinder=normal_find, endfinder=normal_find ):
    """Compress consecutive items in @lst into a single item.
    @start and @end are indices or patterns that determine the start and end of item compression,
    @startoffset, and @endoffset allow manipulation of endpoints,
    @fill determines the separator for the joining of the items compressed,
    @startfinder, and @endfinder are the functions used to find the start and end patterns.
    """
    temp_s = []
    pattern_start = start if isinstance(start, int) else startfinder( lst, start ) + startoffset
    pattern_end = end if isinstance(end, int) else endfinder(lst, end ) + endoffset
    for i in range(pattern_end, pattern_start - 1, -1):
        temp_s += [lst.pop(i)]
    lst.insert( pattern_start, fill.join(temp_s[::-1]) )
