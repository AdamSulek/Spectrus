import os
import re
import numpy as np
import sys
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory
from kivy_garden.graph import Graph, MeshLinePlot, SmoothLinePlot
from kivy.uix.label import Label
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from matplotlib.widgets import Cursor
from ..functions.util import str_checker
from ..functions.popup import invalidLoad, invalidVal, invalidVal2, chooseLoadFile, \
  invalidFile, invalid_from_to, invalidSubstract, invalid_enter_number, AddPopup, \
  invalidSave

class Welcome(Screen):

    list_x = ListProperty([])
    list_y = ListProperty([])
    title_list = ListProperty([])
    lists_of_lists = ListProperty([])
    position = ObjectProperty(None)
    plot = ObjectProperty(None)
    y_start = ObjectProperty(None)
    y_end = ObjectProperty(None)
    x_start = ObjectProperty(None)
    x_end = ObjectProperty(None)
    sub_down = ObjectProperty(None)
    graph = ObjectProperty(None)
    text_input = ObjectProperty(None)
    number_of_spectra = ObjectProperty(None)
    text_name = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Welcome, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.number_of_column = 0
        self.norm = []

    def mouse_pos(self, window, pos):
        '''
            This function return mouse position value in the area of spectrum,
            even if window size is changed.
        '''
        ax_x_began = int(Window.size[0] / 4) + 76
        ax_x_finish = Window.size[0] - 20
        ax_y_began = 65
        ax_y_finish = int(Window.size[1] * 0.9) - 20
        if pos[0] >= ax_x_began and pos[0] <= ax_x_finish and pos[1] >= ax_y_began \
                                                           and pos[1] <= ax_y_finish:
            pixX_per_nm = (ax_x_finish - ax_x_began) / (self.graph.xmax - self.graph.xmin)
            pixX = pos[0] - ax_x_began
            pixY_per_nm = (ax_y_finish - ax_y_began) / (self.graph.ymax - self.graph.ymin)
            pixY = pos[1] - ax_y_began
            resultX = pixX / pixX_per_nm
            resultY = pixY / pixY_per_nm
            wynikX = round(self.graph.xmin + resultX)
            wynikY = round(self.graph.ymin + resultY, 4)
            poz_x = str(wynikX)
            poz_y = str(wynikY)
            self.position.text = poz_x + " : " + poz_y
        #to check min and max mouse position in different boxlayout
        #self.position.text = str(pos)

    def dismiss_popup(self):
        '''
            This function dissmiss Popup window.
        '''
        self._popup.dismiss()

    def show_load(self):
        '''
            This function trigger Load Dialog window.
        '''
        content = Factory.LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def load(self, path, filename, x_start, x_end):
        '''
            This function load file in that way ommitted non digit value
            (regex also catch -+ value on the beggining and one dot in the middle).

            Program starts reading a file after find 2 digit separeted
            by white space. Findings of fragment not matching finished
            reading a file in case of many spectrometer generate noises
            of spectra to the file.
        '''
        #reset x_list, y_list if load different file without clear
        pattern = '[-+]?\d+\.?\d*\s[-+]?\d+\.?\d*'
        self.list_y = []
        self.list_x = []

        try:
            if filename != []:
                # print("tu wlazlem")
                with open(os.path.join(path, filename[0]), 'r') as stream:
                    first = False
                    for index, line_val in enumerate(stream.readlines()):
                        print("index: {}, line_val: {}".format(index, line_val))
                        if re.match(pattern, line_val):
                            print("tu wlazlem")
                            x_val = int(line_val.split()[0])
                            if x_val >= int(x_start) and x_val <= int(x_end):
                                self.list_x.append(int(line_val.split()[0]))
                                self.list_y.append(round(float(line_val.split()[1]), 3))
                                first = True
                        if not re.match(pattern, line_val) and first:
                            break
                    if self.list_x:
                        #set Textinput variables
                        self.x_end.text = str((max(self.list_x) + 10))
                        self.x_start.text = str((min(self.list_x) - 10))
                        self.y_start.text = str((min(self.list_y) - 0.1))
                        self.y_end.text = str((max(self.list_y) + 0.1))
                        self.draw()
                    else:
                        invalidFile()
                    self.dismiss_popup()
            else:
                chooseLoadFile()

        except ValueError:
            invalidLoad()
        # print("jetsem w welcome.load i wyswietlam self.x_start".format(self.x_start.text))

    def show_save(self):
        '''
            This function trigger Save Dialog window.
        '''
        content = Factory.SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def save(self, path, filename):
        '''
            This function save a file created from add spectrum
            in order of adding.

            NaN value is write as white space.
        '''
        try:
            self.norm = self.standardize_list(self.lists_of_lists)
            for lists in self.lists_of_lists:
                max_val = len(self.lists_of_lists[0])
                if len(lists) > max_val:
                    max_val = len(lists)
            with open(os.path.join(path, filename), 'w') as stream:
                index = 0
                for lines in range(0, max_val-1):
                    line = ""
                    for single_list in self.norm:
                        if np.isnan(single_list[index]):
                            line += '           '
                        else:
                            line += '%.3f' % single_list[index] + ' '
                    line += '\n'
                    index += 1
                    stream.write(line)

            self.list_x = []
            self.list_y = []
            self.dismiss_popup()

        except UnboundLocalError or PermissionError:
            invalidSave()

    def standardize_list(self, nested_list):
        '''
            This function takes nested list in order: list_of_x values,
            list_of_y values with the same length.

            In the case when another two list has different length,
            this function return list with shape
            (number of list : max length lists) and missing spaces are
            filled in NaN.
        '''
        try:
            lengths = [i for i in map(len, nested_list)]
            shape = (len(nested_list), max(lengths))
            standard = np.full(shape, np.nan)
            for i, r in enumerate(nested_list):
                standard[i, :lengths[i]] = r
            # print("===================")
            # print(standard)
            return standard
        except ValueError:
            invalidSave()

    def show_addname(self):
        '''
            This function trigger Addspectraname Window.
        '''
        content = Factory.Addspectraname(cancel=self.dismiss_popup,
                                         add_name=self.add_name)
        self._popup = Popup(title="Add spectrum name", content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def add_name(self, spectra_name):
        '''
            This function add spectra name.
        '''
        self.title_list.append(spectra_name)
        self.update_text_name()
        AddPopup()
        self.dismiss_popup()

    def update_text_name(self):
        '''
            This function add the last spectra name into user Window.
        '''
        self.text_name.text += self.title_list[-1] + '\n'

    def add(self):
        '''
            This function append new spectrum to collective spectra which
            will be saved to the file when spectrum is loading.

            Click on add button when spectrum is not loading trigger
            loading window.
        '''
        if self.list_x:
            self.lists_of_lists.append(self.list_x)
            self.lists_of_lists.append(self.list_y)
            self.list_x = []
            self.list_y = []
            self.x_start.text = ""
            self.x_end.text = ""
            self.y_start.text = ""
            self.y_end.text = ""
            self.sub_down.text = ""
            self.graph.remove_plot(self.plot)
            self.number_of_column += 2
            self.show_addname()
            self.number_of_spectra.text = str(int(self.number_of_column/2))
        else:
            self.show_load()

    def draw_btn(self):
        '''
            This function is trigger by draw button not automatically like draw
            function after loading the file.

            Using of this function after loading a spectrum allows to cut
            unnecessary part of spectra by choosing range of spectra in
            TextInput window and this part will be saved in prepared file.

            Cutting a part of specta is irreversible. Only loading again the file
            restore whole original spectra.

            Using of higher value in 'from: ' TextInput window instead of 'to: '
            turn on WARNING popup window instead of raise ValueError.
        '''
        if self.list_x:
            new_x = []
            new_y = []
            try:
                x_start_int = int(self.x_start.text)
                x_end_int = int(self.x_end.text)
                if x_start_int < x_end_int:
                    for ind, x_val in enumerate(self.list_x):
                        if x_val >= x_start_int and x_val <= x_end_int:
                                new_x.append(x_val)
                                new_y.append(self.list_y[ind])
                    self.list_x = new_x
                    self.list_y = new_y
                    self.graph.remove_plot(self.plot)
                    if str_checker(x_start_int) and str_checker(x_end_int):
                        self.graph.xmin = float(self.x_start.text)
                        self.graph.xmax = float(self.x_end.text)
                    else:
                        invalidVal()
                    if str_checker(self.y_start.text) and \
                       str_checker(self.y_end.text):
                        self.graph.ymin = float(self.y_start.text)
                        self.graph.ymax = float(self.y_end.text)
                    else:
                        invalidVal()
                    self.plot = MeshLinePlot()
                    self.plot.points = [(self.list_x[index], self.list_y[index])
                                       for index in range(0, len(self.list_x)-1)]
                    self.graph.add_plot(self.plot)
                    self.graph.x_ticks_major = ((self.graph.xmax - self.graph.xmin) / 8)
                else:
                    invalid_from_to()
            except ValueError:
                invalid_enter_number()
        else:
            invalidLoad()

    def draw(self):
        '''
            This function is trigger automatically after loading
            the file.
        '''
        self.graph.remove_plot(self.plot)
        if str_checker(self.x_start.text) and str_checker(self.x_end.text):
            self.graph.xmin = self.list_x[0] - 10
            self.graph.xmax = self.list_x[len(self.list_x)-1] + 10
        else:
            invalidVal()
        if str_checker(self.y_start.text) and str_checker(self.y_end.text):
            self.graph.ymin = min(self.list_y) - 0.1
            self.graph.ymax = max(self.list_y) + 0.1
        else:
            invalidVal()
        self.plot = MeshLinePlot()
        self.plot.points = [(self.list_x[index], self.list_y[index])
                             for index in range(0, len(self.list_x)-1)]
        self.graph.add_plot(self.plot)
        self.graph.x_ticks_major = ((self.graph.xmax - self.graph.xmin) / 8)
        self.x_start.text = str(self.graph.xmin)
        self.x_end.text = str(self.graph.xmax)
        self.y_start.text = str(round(self.graph.ymin, 4))
        self.y_end.text = str(round(self.graph.ymax, 4))

    def clear(self):
        '''
            This function clear all text input fields, remove a graph and
            new spectrum could be drawn and add as a new spectrum
            to collective spectra.
        '''
        self.list_x = []
        self.list_y = []
        self.graph.remove_plot(self.plot)
        self.x_start.text = ""
        self.x_end.text = ""
        self.y_start.text = ""
        self.y_end.text = ""
        self.sub_down.text = ""

    def sub_min(self):
        '''
            This function substract y value that min value is zero.
        '''
        if self.list_x:
            min_val = min(self.list_y)
            for i in range(0, len(self.list_y)):
                self.list_y[i] = round((self.list_y[i] - min_val), 3)
            self.draw()
        else:
            invalidLoad()

    def normalize(self):
        '''
            This function scale (normalize) y value from 0 to 1.
        '''
        if self.list_x:
            self.sub_min()
            max_val = max(self.list_y)
            for i in range(0, len(self.list_y)):
                self.list_y[i] = round((self.list_y[i] / max_val), 3)
            self.draw()
        else:
            invalidLoad()

    def substract(self):
        '''
            Using of non-digit value in TextInput turn on WARNING popup window
            instead of raise ValueError.
        '''
        if self.list_x:
            if str_checker(self.sub_down.text):
                value = float(self.sub_down.text)
                for i in range(0, len(self.list_y)):
                    self.list_y[i] = round((self.list_y[i] - value), 3)
                self.draw()
            else:
                invalid_enter_number()
        else:
            invalidLoad()
            self.sub_down.text = ""
