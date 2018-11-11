

'''
Example of pyforms.
In this script we create a GUI app using MVC pattern. Also it saws how to create an app with multiple windows in it.
This is based on this example: https://pyforms-gui.readthedocs.io/en/v4/getting-started/multiple-windows.html
'''

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlLabel, ControlButton, ControlList, ControlFile, ControlDockWidget, ControlEmptyWidget
from re import sub
import json
from utils.singleton import singleton

class Organism:
    '''
    This is our base entity class.
    '''
    def __init__(self, kingdom, cls, order, family, name):
        def parse(*args):
            def _parse(value):
                if type(value) != str:
                    raise TypeError('{} attribute must be a string but got {}'.format(value, type(value).__name__))
                if len(value) < 2:
                    raise ValueError('{} attribute must be a non empty string'.format(value))
                return sub('[ ]+', ' ', value[0].upper() + value[1:].lower())

            return [_parse(value) for value in args]

        self.kingdom, self.cls, self.order, self.family, self.name = parse(
            kingdom, cls, order, family, name
        )

    def to_dict(self):
        return dict((key, getattr(self, key)) for key in ['kingdom', 'cls', 'order', 'family', 'name'])

    @classmethod
    def from_dict(cls, data):
        kwargs = dict([(key, value) for key, value in data.items() if key in ['kingdom', 'cls', 'order', 'family', 'name']])
        return cls(**kwargs)

    def __str__(self):
        return self.name

# Entity examples
cat = Organism(kingdom = 'Animalia', cls='Mammalia', order='Carnivora',family='Felidae', name='Felis silvestris catus')
human = Organism(kingdom = 'Animalia', cls='Mammalia', order='Primates', family='Hominidae', name='Homo sapiens sapiens')


class Organisms:
    '''
    This class stores all the entities we created and also has two methods: save(), load() to store or read entities to/from
    a external file.
    '''
    def __init__(self):
        self._items = list()

    def save(self, fp):
        json.dump([item.to_dict() for item in self._items], fp)

    def load(self, fp):
        for item_data in json.load(fp):
            self.add(Organism.from_dict(item_data))

    def add(self, organism):
        self._items.append(organism)

    def remove(self, index):
        self._items.pop(index)


class NewOrganismGUI(BaseWidget):
    '''
    This widget is a window that shows a form to create a new entity of our model.
    '''
    def __init__(self):
        super().__init__()


        fields = [ControlText(title + ': ') for title in ('Kingdom', 'Class', 'Order', 'Family', 'Name')]
        self.kingdom, self.cls, self.order, self.family, self.name = fields
        self.cancelButton = ControlButton('Cancel')
        self.createButton = ControlButton('Accept')

        self.formset = [
            'kingdom', 'cls', 'order', 'family', 'name',
            ('cancelButton', 'createButton')
        ]

        self.createButton.value = self.__createButtonAction
        self.cancelButton.value = self.__cancelButtonAction

    def __createButtonAction(self):
        try:
            entity = Organism(**dict([(key, getattr(self, key).value) for key in ('kingdom', 'cls', 'order', 'family', 'name')]))
            # Send the new entity created
            if self.parent is not None:
                self.parent.add(entity)
            self.close()
        except TypeError:
            pass
        except ValueError:
            pass

    def __cancelButtonAction(self):
        self.close()

class OrganismsGUI(BaseWidget, Organisms):
    '''
    Main widget. Shows all entities created
    '''
    def __init__(self):
        BaseWidget.__init__(self)
        Organisms.__init__(self)

        self._list = ControlList('Organisms',
                                 add_function = self.__addOrganismBtnAction,
                                 remove_function = self.__removeOrganismBtnAction)
        self._list.horizontal_headers = ['Kingdom', 'Class', 'Order', 'Family', 'Name']
        self._panel = ControlEmptyWidget()
        self.filedialog = ControlFile()
        self.filedialog.hide()

        self.mainmenu = [
            {
                'File' : [
                    {'Open' : self.__openMenuAction},
                    {'Save' : self.__saveMenuAction}
                ]
            }
        ]


        # Add by default some entities
        self.add(cat)
        self.add(human)

    def __addOrganismBtnAction(self):
        # Popup a window to create a new entity with the user input
        win = NewOrganismGUI()
        win.parent = self
        self._panel.value = win
        win.show()

    def __removeOrganismBtnAction(self):
        if self._list.selected_row_index is not None:
            self.remove(self._list.selected_row_index)


    def add(self, organism):
        Organisms.add(self, organism)
        # Show the newly created entity in our GUI list
        self._list += [organism.kingdom, organism.cls, organism.order, organism.family, organism.name]

    def remove(self, index):
        # Remove the entity selected by user
        Organisms.remove(self, index)
        # Reflect changes in GUI
        self._list -= index

    def __saveMenuAction(self):
        self.filedialog.use_save_dialog = True
        self.filedialog.click()
        try:
            with open(self.filedialog.value, 'w') as file:
                self.save(file)
        except:
            pass

    def __openMenuAction(self):
        self.filedialog.use_save_dialog = False
        self.filedialog.click()
        try:
            with open(self.filedialog.value, 'r') as file:
                self.load(file)
        except:
            pass



if __name__ == '__main__':
    pyforms.start_app(OrganismsGUI, geometry=(200, 200, 550, 200))
