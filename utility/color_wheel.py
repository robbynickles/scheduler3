some_colors = {
'aquamarine2': (118, 238, 198, 255), 
'orchid4': (139, 71, 137, 255), 
'antiquewhiteT': (250, 235, 215, 200), 
'yellow2': (238, 238, 0, 255), 
'wheat1': (255, 231, 186, 255), 
'olivedrab1': (192, 255, 62, 255),
'orangered1': (255, 69, 0, 255),
'darkturquoise': (0, 206, 209, 255),
'indianred4': (139, 58, 58, 255),
'lavenderblush4': (139, 131, 134, 255),
'steelblue1': (99, 184, 255, 255),
'deepskyblue4': (0, 104, 139, 255),
'peachpuff3': (205, 175, 149, 255),
'goldenrod': (218, 165, 32, 255),
'springgreen3': (0, 205, 102, 255),
'mediumpurple3': (137, 104, 205, 255),
'burlywood': (222, 184, 135, 255),
'darkseagreen1': (193, 255, 193, 255)
}
somet_colors = {}
opacity = lambda (r,g,b,a): (r, g, b, 1.0 * a)
percent = lambda x: x/255.0
for key, value in some_colors.items():
    some_colors[key] = map(percent, value)
    somet_colors[key] = map(percent, opacity(value))



colors = ['darkturquoise', 'aquamarine2', 'yellow2', 'indianred4', 'mediumpurple3', 'springgreen3', 'peachpuff3',
          'darkseagreen1', 'orchid4', 'orangered1' ]
_color_wheel = [ some_colors[ c ] for c in colors ]

def get_color():
    global _color_wheel
    try:
        return _color_wheel.pop(0)
    except IndexError:
        _color_wheel = [ some_colors[ c ] for c in colors ]
        return _color_wheel.pop(0)
