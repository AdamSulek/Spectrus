# Spectrus
is the software to spectra analysis which present data in a graph way.

It is open-source, non-commercial, user friendly, the software is written in
Python and kivy.

Spectrus offers a load file method, which grab two
the column of data but without the trash (e.g. spectrum noise), automatically.

The Spectrus gives the ability to easy-to-use spectrum subtraction with define
value, set to zero, as well as normalization the spectrum (Absorbance value, 0-1).

This program provides only a single spectra display on one time, but after
adding the prepared spectra is possible to load the next spectra. After adding
all spectra it is an easy way to save a prepared file.
## Setup

### Install packages
`pip3 install -r requirements.txt`

### Run the program
You simply run command:
`python3 App.py` from root directory

### Testing the application
Choosing:
- "Load" button, and choose /docs/examples/84.dx

- you can change the range of spectra by changing range in label `rangefrom:` `to:` and use btn DRAW

- mouse position (x,y) is display in right upper corner. You can glance the value which you want substract with `substract` button

- default `substract min` button use very often use substrating to zero

- additionally, `normalize` substract to min and set maximum to 1.0

- if you don't want to save each spectra, use clear button or just load new spectra

- if you set up properly the spectra, click add button and you can use name of this spectra

- in the left panel you can observe which spectra you add, and also in right corner but only as a number

- if you process all needed data you can save it with `save` button. Please choose location and filename

#### Screens from the program
![](spectrus_screenshots.png)
