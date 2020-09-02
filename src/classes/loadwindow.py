from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class LoadDialog(FloatLayout):
    '''
        This class represents Loading window.

        Contains one button:
            cancel - assigned to the dissmiss_popup method found in each class
    '''
    cancel = ObjectProperty(None)
    load = ObjectProperty(None)
    x_start = ObjectProperty(None)
    x_end = ObjectProperty(None)
