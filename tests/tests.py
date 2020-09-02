import unittest
import os
import sys
from src.classes.welcome import Welcome
import unittest.mock as mock
from kivy_garden.graph import Graph, MeshLinePlot, SmoothLinePlot
import tempfile
from kivy.properties import ObjectProperty

class TestWelcomeMethods(unittest.TestCase):

    def mock_empty(self):
        pass

    def setUp(self):
        self.welcome = Welcome()
        self.test_dir = tempfile.TemporaryDirectory(prefix='temp_dir')
        self.test_file = os.path.join(self.test_dir.name, 'test_file')
        with open(self.test_file, 'w') as test_file:
            test_file.write("351 174.3 \n")
            test_file.write("352 14.3124")
        self.adres = []
        self.adres.append(self.test_file)

    @mock.patch("src.classes.welcome.Welcome.x_start")
    @mock.patch("src.classes.welcome.Welcome.x_end")
    @mock.patch("src.classes.welcome.Welcome.y_start")
    @mock.patch("src.classes.welcome.Welcome.y_end")
    @mock.patch("src.classes.welcome.Welcome.draw")
    @mock.patch("src.classes.welcome.Welcome.dismiss_popup")
    def test_load_ok(self, mock_x, mock_xx, mock_y, mock_yy, mock_draw, mock_dismiss):
        mock_draw = self.mock_empty()
        mock_x = "350"
        mock_xx = "700"
        mock_y = "0"
        mock_yy = "2.0"
        mock_dismiss = self.mock_empty()
        self.welcome.load(self.test_dir.name, self.adres, "340", "750")

    def test_load_notdigit(self):
        with self.assertRaises(ValueError):
            self.welcome.load(self.test_dir.name, self.adres, "340", "as")

    def test_load_notdigit2(self):
        with self.assertRaises(ValueError):
            self.welcome.load(self.test_dir.name, self.adres, "a", 740)

    def test_standardize(self):
        '''
            This test function check if nested list with different length
            after using standardize_list function has the same length
        '''
        nested_list = []
        list_x_1 = [x for x in range(350, 370)]
        list_y_1 = [y for y in range(350, 370)]
        list_x_2 = [x for x in range(350, 570)]
        list_y_2 = [y for y in range(350, 570)]
        nested_list.append(list_x_1)
        nested_list.append(list_y_1)
        nested_list.append(list_x_2)
        nested_list.append(list_y_2)
        expectation = self.welcome.standardize_list(nested_list)
        self.assertEqual(len(expectation[0]), len(expectation[2]))

    @mock.patch("src.classes.welcome.Welcome.draw")
    @mock.patch("src.classes.welcome.Welcome.list_x")
    @mock.patch("src.classes.welcome.Welcome.list_y")
    def test_sub_min_ok(self, mock_list_y, mock_list_x, mock_draw):
        mock_list_x.__iter__.return_value = [320, 321, 322]
        mock_list_y.__iter__.return_value = [117.05, -13.3, 22]
        mock_draw = self.mock_empty()
        self.welcome.sub_min()

    @mock.patch("src.classes.welcome.Welcome.sub_min")
    @mock.patch("src.classes.welcome.Welcome.draw")
    @mock.patch("src.classes.welcome.Welcome.list_x")
    @mock.patch("src.classes.welcome.Welcome.list_y")
    def test_normalize_ok(self, mock_list_y, mock_list_x, mock_draw, mock_sub_min):
        mock_list_x.__iter__.return_value = [320, 321, 322]
        mock_list_y.__iter__.return_value = [117.05, -13.3, 22]
        mock_sub_min = self.mock_empty()
        mock_draw = self.mock_empty()
        self.welcome.normalize()

    @mock.patch("src.classes.welcome.Welcome.sub_down")
    @mock.patch("src.classes.welcome.Welcome.draw")
    @mock.patch("src.classes.welcome.Welcome.list_x")
    @mock.patch("src.classes.welcome.Welcome.list_y")
    def test_substract(self, mock_list_y, mock_list_x, mock_draw, mock_sub_min):
        mock_list_x.__iter__.return_value = [320, 321, 322]
        mock_list_y.__iter__.return_value = [117.05, -13.3, 22]
        mock_sub_down = "2.0"
        mock_draw = self.mock_empty()
        self.welcome.substract()

    def tearDown(self):
        del self.adres
        del self.welcome
        del self.test_file
        self.test_dir.cleanup()

if __name__ == '__main__':
    unittest.main()
