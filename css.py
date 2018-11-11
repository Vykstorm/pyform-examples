
'''
Usage example of pyforms library.
This example illustrates how to use css on your pyforms gui components.
This scripts reads the file styles/example5.css and applies the loaded stylesheet to the GUI. To indicate pyforms where
to read the stylesheet css file, you must create your local_settings.py file in your working directory and set
the config variable PYFORMS_STYLESHEET
Another way (used on this example) is to define your settings in any place (config/example5_settings.py) and load configuration
before starting the app using the conf object from the confapp module
'''

import pyforms
from pyforms.controls import ControlText, ControlLabel, ControlTextArea, ControlButton
from pyforms.basewidget import BaseWidget
from confapp import conf

class Foo(BaseWidget):
    def __init__(self):
        super().__init__()

        self.name = ControlText('Name: ')
        self.surname = ControlText('Surname: ')
        self.address = ControlText('Address: ')
        self.description = ControlTextArea('Write your issue here: ')
        self.submit = ControlButton('Submit')

        self.formset = [
            'name', 'surname', 'address', 'description', '=', 'submit'
        ]

if __name__ == '__main__':
    conf += 'config.example5_settings'
    app = pyforms.start_app(Foo, geometry=(300, 300, 300, 300))