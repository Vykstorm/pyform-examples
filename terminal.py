
'''
Another example of pyforms
This example illustrates what can be done with the submodule pyforms-terminal
Execute the next command in a console on this working directory:
python3 example6.py terminal_mode --help  # shows command parameters description

Then try:
python3 example6.py terminal_mode --name nicola --surname tesla --address serbia --exec submit

Running the command above, the input fields name, surname and address on the GUI will be fill by the values indicated
in the terminal. Then, method submit() on the app object will be called.

Try also this example in normal GUI mode, fill manually the inputs and press the "submit" button. This will have the same
effect as the previous command.
'''


import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlText, ControlTextArea


class Foo(BaseWidget):
    def __init__(self):
        super().__init__()

        self.name = ControlText('Name: ')
        self.surname = ControlText('Surname: ')
        self.address = ControlText('Address: ')
        self.description = ControlTextArea('Write your issue here: ')
        self._submit = ControlButton('Submit')

        self.formset = [
            'name', 'surname', 'address', 'description', '=', 'submit'
        ]

        self._submit.value = self.submit


    def submit(self):
        print('Submit issue')
        print('Name: ', self.name.value if self.name.value is not None else '---')
        print('Surname: ', self.surname.value if self.surname.value is not None else '---')
        print('Address: ', self.address.value if self.address.value is not None else '---')



if __name__ == '__main__':
    pyforms.start_app(Foo, geometry=(300, 300, 200, 300))