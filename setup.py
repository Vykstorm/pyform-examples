
'''
Installation script
'''

from setuptools import setup



if __name__ == '__main__':
    setup(
        name = 'Pyform examples',
        version = '1.0.0',
        description = 'Basic examples of using the python library Pyforms to create python GUIs',
        author = 'Vykstorm',
        author_email = 'victorruizgomezdev@gmail.com',
        python_requires = '>=2.7',
        install_requires = ['pyforms-gui', 'pyforms-web', 'pyforms-terminal'],
        dependency_links = [''],
        keywords = ['gui', 'pyforms', 'examples']
    )
