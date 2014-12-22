
types = ['1WV2A', '2WAO', '2WVA', 'CAI', 'DINT', 'DIR', 'FLXP', 'ITV', 'LAB', 'LEC', 'LECD', 'OIM', 'OIS', 'OMI', 'OPM', 'RAD', 'SINT', 'TUT', 'TXT', 'WEXP']
valid_types = types

def tmatch( lst, index ):
    for i in range(len(lst)):
        if str(lst[i]) in types:
            return i
    return ValueError
