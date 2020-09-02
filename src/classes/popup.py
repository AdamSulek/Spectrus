from kivy.uix.popup import Popup
from kivy.uix.label import Label

def invalidLoad():
    popup = Popup( title = " something went wrong ",
                   content = Label(text = "Please Load a file"),
                   size_hint = (None, None), size = (400, 400) )
    popup.open()

def invalid_from_to():
    popup = Popup(title = " something went wrong ",
                  content = Label(text = "'from' value must be lower than 'to' value"),
                  size_hint = (None, None), size = (400, 400) )
    popup.open()

def chooseLoadFile():
    popup = Popup( title = " something went wrong ",
                   content = Label(text = "Please choose a file"),
                   size_hint = (None, None), size = (400, 400) )
    popup.open()

def invalidFile():
    popup = Popup( title = " something went wrong ",
                   content = Label(text = "         File which you choose is not a spectrum\
                                           \nPlease choose a spectrum file",\
                                             halign='center'),
                   size_hint = (None, None), size = (450, 450),  )
    popup.open()

def invalidSubstract():
    popup = Popup( title = " something went wrong ",
                   content = Label(text = "Please enter substract value"),
                   size_hint = (None, None), size = (400, 400) )
    popup.open()

def invalid_enter_number():
    popup = Popup( title = " something went wrong ",
                   content = Label(text = "Please enter number"),
                   size_hint = (None, None), size = (400, 400) )
    popup.open()

def invalidVal():
    popup = Popup( title = " something went wrong ",
                   content = Label(text = "Work with numbers only"),
                   size_hint = (None, None), size = (400, 400) )
    popup.open()

def invalidVal2():
    popup = Popup( title = " something went wrong ",
                   content = Label(text = "Please Load a file"),
                   size_hint = (None, None), size = (400, 400) )
    popup.open()

def AddPopup():
    popup = Popup( title = "  Success!!! ",
                   content = Label(text = "You add properly new spectrum"),
                   size_hint = (None, None), size = (400, 400) )
    popup.open()
