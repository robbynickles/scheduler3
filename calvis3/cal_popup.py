from global_environment import *
from utility.helpers import *
from sectiondetail import SectionDetail

def add_block(self, block, layer ):
    day, start, end, ty, location, course_dict = block
    p1, p2 = cal_map(day, start), cal_map(day, end)
    if ty not in ['LEC', 'LAB', 'PERS']:
        p1, p2 = cal_map(day, '4 00 AM'), cal_map(day, '5 00 AM')
    p1 = self.x + p1[0], self.y + p1[1]
    p2 = self.x + p2[0], self.y + p2[1]
    size = XGAP,p2[1]-p1[1]
    button = Button( pos=p1, size=size, background_color=course_dict['my_color'], 
                     on_press=lambda button : popup_window(self, button, block) )
    draw_box(button, p1, size, (1, .5, 0, 1))
    type_color = "33ff33" if ty == 'DINT' else "ffffff"
    text = "{} [color={}]{}[/color]  [b]{}[/b]".format(course_dict['Name'][0][1:], type_color, ty, getsection(course_dict))
    if ty == 'PERS':
        text = "Custom"
    button.add_widget(Label(text=text, font_size=13, markup=True, pos=label_offset((p1[0]+XGAP*.3,p1[1]+3))))
    button.switch_state=False 
    button.my_popup = None
    layer.add_widget(button)

def popup_window(self, button, block):
    if self.active_button == None or self.active_button == button:
        self.parent.apply_transform( self.parent.transform.inverse().translate(-1.2*w, 0, 0) )
        (x,y), (xdim,ydim) = button.pos, button.size
        button.switch_state = not button.switch_state
        if button.switch_state:
            layout = FloatLayout()
            r,g,b,a = 0,0,0,1
            border_color = some_colors['lavenderblush4']
            width = 3
            with layout.canvas:
                if y < h/2.0:
                    pos, size = (self.x, self.y + y+ydim), (w, .95*h-(y+ydim))
                    Color(r,g,b,.8)
                    Rectangle( pos=pos, size=size )
                    draw_box(layout, pos, size, border_color, alpha=1, width=width)
                else:
                    pos, size = (self.x,self.y + .1*h), (w,y-.1*h)
                    Color(r,g,b,.8)
                    Rectangle( pos=pos, size=size )
                    draw_box(layout, pos, size, border_color, alpha=1, width=width)
            button.my_popup = layout

            detail = SectionDetail( block, pos, size )
            layout.detail = detail
            layout.add_widget( detail )

            #class_closeup( self, button.my_popup, pos, size, block )
            self.active_button = button
            self.top_layer.add_widget( layout )
            button.background_normal = button.background_down
        else:
            button.my_popup.remove_widget( button.my_popup.detail )
            self.active_button = None
            button.background_normal = 'atlas://data/images/defaulttheme/button'
            self.top_layer.remove_widget(button.my_popup)

def add_colon( t ):
    return "{}:{} {}".format(*t.split(" "))

def class_closeup( self, renderer, pos, size, block ):
    (ox, oy), (xdim, ydim) = pos, size
    day, start, end, ty, location, course_dict = block
    title = "[b][size=30]{}[/size] [size=24]{}[/size][/b]".format( course_dict['Name'][0][1:], ty )
    timechunks = []
    for typ, days, time, locate in zip(gettypes(course_dict), getdays(course_dict), gettimes(course_dict), getlocations(course_dict)):
        if typ == 'DINT': days = ''
        typ = '[b]{}[/b]'.format( typ )
        timechunks += ['   '.join([typ, ''.join(days), time, locate])]
    title_detail = '\n'.join( timechunks )
    title_detail = "[size=18]{}[/size]".format(title_detail)
    prof = "[size=18][b]{}[/b][/size]".format( course_dict['Instructor'][0] )
    units = "[size=18]{} units[/size]".format( course_dict['Units'][0] )
    raw_status = course_dict['Avail'][0].lower()
    if 'wait' in raw_status.lower():
        if 'open' in raw_status.lower():
            status = '3333ff'
        else:
            status = 'ff3333'
    else:
        status = '33ff33'
    waitlist = "[size=18]Max/Avail : {} \nStatus: [color={}]{}[/color][/size]".format( course_dict['Max/'][0], 
                                                                                       status, course_dict['Avail'][0] )
    section_string = "[size=18]Section: {}[/size]".format( course_dict['Section'][0] )
    if ty == 'PERS':
        lines = ["Custom Event", "{}  {} - {}".format( day, add_colon(start), add_colon(end) )]
    else:
        lines = ["   ".join([title, prof, units]), title_detail,
                 " ".join([waitlist, section_string]) ]
    renderer.add_widget(Label(text='\n'.join(lines), markup=True, color=(1,1,1,1), 
                              pos=label_offset( (ox + w*.5, oy+ydim*.6) ) ) )

    def remove_all_but_this(button):
        course_name = button.section['Name'][0]
        self.bulletin.exclude_all_but( button.section, button.state )

    keep = ToggleButton(text='Keep Section in Schedule', pos=(ox+.1*w, oy+ydim*.2), size=(.8*xdim, .1*ydim), 
                        group='cal_popup1', on_press=remove_all_but_this)
    keep.section = course_dict
    if keep.section['kept_section']:
        keep.state = 'down'

    def remove_section(button):
        if button.state == 'down':
            self.bulletin.exclude_section( button.section )
        else:
            self.bulletin.include_section( button.section )
    remove = ToggleButton(text='Remove Section from Search', pos=(ox+.1*w, oy+ydim*.1), size=(.8*xdim, .1*ydim), 
                          group='cal_popup1', on_press=remove_section)
    remove.section = course_dict
    # Has this been excluded earlier?
    if not remove.section['included_in_search']:
        remove.state = 'down'

    if ty == 'PERS':
        def remove_user_event(button):
            self.bulletin.remove_user_event( button.user_event['ID'] )
            self.top_layer.remove_widget(self.active_button.my_popup)
            self.user_event_layer.remove_widget(self.active_button)
            self.active_button = None
        remove_user_event_button = ToggleButton(text='Remove', pos=(ox+.1*w, oy+ydim*.1), size=(.8*xdim, .1*ydim), 
                                                group='cal_popup1', on_press=remove_user_event)
        remove_user_event_button.user_event = course_dict
        #renderer.add_widget( remove_user_event_button )
    else:
        pass
        #renderer.add_widget(keep)
        #renderer.add_widget(remove)
