from kivy.uix.gridlayout import GridLayout

def find_and_destroy_widget(gridlayout, name):
    if isinstance(gridlayout, GridLayout):
        for child in gridlayout.children:
            if child.id == name:
                gridlayout.remove_widget(child)
