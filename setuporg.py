# -*- coding: utf-8 -*-

# An advanced setup script to create multiple executables and demonstrate a few
# of the features available to setup scripts
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import sys
from cx_Freeze import setup, Executable
import tkinter
import matplotlib
import numpy

base = 'console'
if sys.platform == 'win32':
    base = 'Win32GUI'
if sys.platform == 'win64':
    base = "Win64GUI"
options = {
    'build_exe': {
        'includes': [
            'Modulation_package',
            'create_menu',
            'diode',
            'prac'
        ],
        'path': sys.path
    }
}
executables = [Executable('main_frame.py',base=base)]

setup(name='main_frame',
      version='',
      #description='Advanced sample cx_Freeze script',
      options=options,
      executables=executables
      )