import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.input.providers.mouse import MouseMotionEvent
from kivy_garden.graph import Graph, MeshLinePlot, SmoothLinePlot
from kivy.lang import Builder
from kivy.factory import Factory
from src.classes.loadwindow import LoadDialog
from src.classes.savewindow import SaveDialog
from src.classes.addspectraname import Addspectraname
from src.classes.welcome import Welcome
from src.classes.windowmenager import WindowManager
from src.functions.util import str_checker
from kivy.lang import Builder

file = Builder.load_file("gui/interface.kv")
Window.size = (1240, 700)

class SpecApp(App):
    title = "Spectrus"
    def build(self):
        return file

if __name__ == '__main__':
    SpecApp().run()
