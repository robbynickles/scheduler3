from global_environment import *
from sectiondetail import SectionDetail

def draw_box(widg, pos, size, color, alpha=.3, width=1):
    (x,y), (xdim, ydim), (r,g,b,a) = pos, size, color#some_colors['aquamarine2']
    with widg.canvas:
        Color(r, g, b, alpha)
        Line( points=(x, y, x, y+ydim, x+xdim, y+ydim, x+xdim, y, x, y), width=width )

def take_over( widg, button, e ):
    # Transform_point returns points in the same coordinate space as events.
    s = widg.parent.scale
    x, y = widg.w * e.sx, widg.h * e.sy
    left, bottom, z = widg.parent.transform.transform_point( button.x, button.y, 0 )
    xdim, ydim = button.size
    if left <= x <= left + s*xdim and bottom <= y <= bottom + s*ydim:
        widg.press_button( button )
    if widg.accordion:
        widg.accordion.on_touch_down( e )

def popup_window(self, button, sections):
    button.switch_state = not button.switch_state
    if button.switch_state:
        self.popped = button
        button.oldx, button.oldy = button.x, button.y
        anim = Animation( x=button.x, y=.9*self.h-button.size[1]*.5+20, duration=.1)
        anim.start( button )
        layout = FloatLayout()
        r,g,b,a = 0,0,0,1
        border_color = some_colors['lavenderblush4']#some_colors['antiquewhite']
        width = 3
        pos, size = (self.ox,self.oy), (w,.9*h)
        with layout.canvas:
            Color(r,g,b,.85)
            Rectangle( pos=pos, size=size )
        draw_box(layout, pos, size, border_color, alpha=1, width=width)
        button.my_popup = layout
        class_closeup( self, button, pos, size, sections )
        self.add_widget( layout )
    else:

        anim = Animation( x=button.oldx, y=button.oldy, duration=.1 )
        anim.start(button)
        self.popped = None
        self.remove_widget(button.my_popup) 
        
def add_colon( t ):
    hr, m, mer = t.split(" ")
    return "{}:{} {}".format( hr, m if int(m) > 9 else "0"+m, mer )

def class_closeup( self, button, pos, size, sections ):
    renderer = button.my_popup
    (ox, oy), (xdim, ydim) = pos, size
    title = "[b][size=30]{}[/size] [size=24]{}[/size][/b]".format( sections[0]['Name'][0][1:], sections[0]['Title'][0] )
    #more_infor = "[b][size=18]{}[/size]".format( sections[0]['Info'][0] )
    sections_l = map( lambda s: s['Section'][0], sections)
    sections_string = "[size=18]\n{} has {} {}: [/size]\n".format(sections[0]['Name'][0][1:], len(sections_l), 
                                                          'section' if len(sections_l)==1 else 'sections')
    if len(sections_l) >= 10:
        warning = ""#"[color=ff3333][size=18][b]Warning:[/b][/size][i] At most 10 sections should be included in the search.[/i][/color]"
    else:
        warning = ""
    lines = [title, sections_string, warning]
    renderer.add_widget(Label(text='\n'.join( lines ), markup=True, color=(1,1,1,1),
                              pos=label_offset( (ox + w*.5, oy+ydim*.8) ) ) )
    
    # These widgets communicate their input to the calender.
    # They display options that modify the list of selected courses.

    # Remove the course from the list entirely.
    renderer.add_widget(Button( text="Remove Course", size=(.8*xdim, .06*ydim), pos=( ox+.1*xdim, oy+.46*ydim ),
                                on_press=lambda b: self.remove_course_from_selected( button.course_name ) ))
    # Either exclude or include all the sections from or in the list of selected courses.
    renderer.add_widget(Button( text="Include All Sections", size=(.4*xdim, .06*ydim), pos=( ox+.1*xdim, oy+.4*ydim ),
                                on_press=lambda b: include_all_sections()))
    renderer.add_widget(Button( text="Exclude All Sections", size=(.4*xdim, .06*ydim), pos=( ox+.5*xdim, oy+.4*ydim ),
                                on_press=lambda b: exclude_all_sections()))
    renderer.add_widget(Button( text="Sort by Section Number", size=(.4*xdim, .06*ydim), pos=( ox+.1*xdim, oy+.34*ydim ),
                                on_press=lambda b: populate_glay( lambda s: s['Section'][0], 'Section' ) ) )
    renderer.add_widget(Button( text="Sort by Professor", size=(.4*xdim, .06*ydim), pos=( ox+.5*xdim, oy+.34*ydim ),
                                on_press=lambda b: populate_glay( lambda s: s['Instructor'][0], 'Instructor' ) ) )

    ncols = 10
    nrows = len(sections_l)/ncols + 1 if len(sections_l)%ncols>0 else 0
    glay = GridLayout(cols=ncols, rows=nrows,
                      padding=(.05*xdim, .05*ydim), spacing=(.01*xdim, .01*ydim),
                      pos=pos, size=(xdim,ydim*.38))

    def include_all_sections(): 
        try:
            renderer.remove_widget( renderer.s_detail )
        except:
            pass
        for button in glay.children:
            if button.state == 'down':
                button.state = 'normal'
                section_toggle(button)
    def exclude_all_sections():
        try:
            renderer.remove_widget( renderer.s_detail )
        except:
            pass
        for button in glay.children:
            if button.state == 'normal':
                button.state = 'down'
                section_toggle(button)
    def section_toggle( button ):
        if button.state == 'normal':
            self.bulletin.include_section( button.section )
        else:
            self.bulletin.exclude_section( button.section )
    
    def section_detail( button ):
        try:
            renderer.remove_widget( renderer.s_detail )
        except:
            pass
        button.state = 'down' if button.state == 'normal' else 'normal'
        renderer.s_detail = SectionDetail( button, section_toggle, (ox+.1*xdim,oy+.52*ydim ), (.8*xdim,ydim*.25) )
        renderer.add_widget( renderer.s_detail )

    def populate_glay( sort_by, key ):
        glay.clear_widgets()
        try:
            renderer.remove_widget( glay )
        except:
            pass
        sorted_sections = sorted( sections, key=sort_by )
        for i in range( nrows ):
            if i == len(sorted_sections)/ncols:#Last row is the remainder.
                start, end = i*ncols, i*ncols+len(sections_l)%ncols
            else:
                start, end = i*ncols, (i+1)*ncols
            for j in range(start, end):
                text = sorted_sections[j][ key ][0]
                if key == 'Instructor': text = '[size=14]{}[/size]'.format( text.split(',')[0] )
                s_button = ToggleButton(text=str(text), markup=True, background_color=sections[j]['my_color'], on_press=section_detail)
                s_button.section = sorted_sections[j]
                if not s_button.section['included_in_search']:
                    s_button.state = 'down'
                    # Remove specific sections from the list of selected courses.
                glay.add_widget(s_button)
        renderer.add_widget( glay )
    populate_glay( lambda s: s['Section'][0], 'Section' )

