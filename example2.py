'''
Another example of pyforms GUI application.
This will demonstrate how to create a simple application with some label texts, inputs, buttons, interact with this components
and make actions.

Similar to https://pyforms-gui.readthedocs.io/en/v4/getting-started/the-basic.html
'''


import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlButton


# You can define your GUI application as a class inherited from BaseWidget
class PrimeFactorizer(BaseWidget):
    def __init__(self):
        # Call BaseWidget constructor
        super().__init__(title=self.__class__.__name__)

        # Now we create internal GUI elements
        self.input = ControlText('Write a number: ')
        self.startButton = ControlButton('Factorize')
        self.output = ControlText('Output: ')

        # Add this instance __buttonAction method as a callback handler that will be called
        # when button is pressed
        self.startButton.value = self.__buttonAction

        # This member can be used to indicate how GUI components will layout.
        # Horizontal and vertical splitters are '=' and '||'
        # Dictionaries can be specified to create different tabs
        self.formset = [('input', 'startButton'), '=', 'output']

    def __buttonAction(self):
        # Called when startButton is pressed
        try:
            num = int(self.input.value)
            if num == 0:
                raise ValueError()

            factors = self.factorize(abs(num))
            self.output.value = ('-' if num < 0 else '')+' * '.join(['{}^{}'.format(prime, exp) for prime, exp in factors])

        except ValueError:
            self.output.value = 'Invalid input'


    def factorize(self, num):
        if num == 1:
            return [(1, 1)]
        if num == 2:
            return [(2, 1)]

        for a in range(2,num):
            if num % a == 0:
                num //= a
                y = 1
                while num > 1 and num % a == 0:
                    num //= a
                    y += 1
                if num == 1:
                    return [(a, y)]
                return [(a, y)] + self.factorize(num)
        return [(num, 1)]

if __name__ == '__main__':
    # Start GUI application passing your class to the start_app function
    pyforms.start_app(PrimeFactorizer, geometry=(250, 250, 100, 100))