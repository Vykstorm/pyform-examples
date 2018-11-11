
'''
Another example of pyforms. This example demonstrates how to create a menu inside our GUI application.
Some code extracted from: https://pyforms-gui.readthedocs.io/en/v4/getting-started/the-basic.html

The GUI application created  by this script is a small file editor that has a menu to handle some basic file operations like
open, save, save as file, ...

Also a text area is shown in the window, and it will reflect the contents of the opened file and its also editable.
'''


import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlLabel, ControlText, ControlTextArea, ControlFile

class FileEditor(BaseWidget):
    def __init__(self):
        super().__init__()

        # mainmenu attribute can be specified to create the GUI menu
        self.mainmenu = [
            {
                'File' : [
                    {'Open' : self.__openEvent},
                    {'Save' : self.__saveEvent},
                    {'Save as' : self.__saveAsEvent},
                    {'Reload' : self.__reloadEvent}
                ]
            }
        ]

        # Create text area to edit file contents
        self.editor = ControlTextArea()

        # Create file dialog control object.
        self.filedialog = ControlFile()
        self.filedialog.hide()

        # This attribute will hold the path to the current file being edited
        self.current_file = None

    def select_file(self, use_save_dialog = False):
        '''
        This function opens up the file dialog and waits for user input.
        :return: Returns the selected user file or None if no file was selected.
        '''
        self.filedialog.use_save_dialog = use_save_dialog
        self.filedialog.click()
        value = self.filedialog.value
        if len(value) == 0:
            return None
        return value

    def read_file(self, path):
        '''
        Read file contents of a file and update editor text with its content
        :param path:
        :return:
        '''
        with open(path, 'r') as file:
            self.editor.value = file.read()

    def write_file(self, path):
        '''
        Write current editor content to a file
        :param path:
        :return:
        '''
        with open(path, 'w') as file:
            file.write(self.editor.value)


    def __openEvent(self):
        # This is called when menu "Open..." is clicked
        try:
            selected_file = self.select_file()
            if selected_file is None:
                raise ValueError()
            self.read_file(selected_file)
            self.current_file = selected_file
        except:
            pass

    def __saveEvent(self):
        # Called when menu "Save" is opened
        try:
            if self.current_file is None:
                self.__saveAsEvent()
            else:
                self.write_file(self.current_file)
        except:
            pass

    def __saveAsEvent(self):
        try:
            selected_file = self.select_file(use_save_dialog=True)
            if selected_file is None:
                raise ValueError()
            self.write_file(selected_file)
            self.current_file = selected_file
        except:
            pass

    def __reloadEvent(self):
        try:
            self.read_file(self.current_file)
        except:
            self.current_file = None

if __name__ == '__main__':
    pyforms.start_app(FileEditor, geometry=(300, 300, 640, 480))
