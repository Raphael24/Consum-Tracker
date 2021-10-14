# Usage of this setup Script to generate an exe
#
# 0. Install the normal Python interpretor!
# 0.1 Install cx_Freeze by running this command: "pip install --upgrade cx_Freeze"
# 1. Install py3exe vom the folder ..\py3exe\
# 2. Open new Console
# 3. Navigate to this Folder, where this file is stored
# 4. Enter command "python setup.py build"
#
# Author: Raphael Romann
# 24.09.2021
#
#
# ------ Verison directory -----
#
# Version 0.1 , 24.09.2021 : Init setup
#
# Version 0.2, 14.10.2021 : Improve Loaddata function, Add consum per month
#


#from setuptools import setup

from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {"build_exe":"../dist",
                     "include_files":["KonsumProgramm/consum.ui",
                                      "Icon_Main.jpg"],
		             "excludes":["tkinter"],
                    }



setup(  name = "consumtracker",
        version = "0.2",
        author='Raphael Romann',
        description = "A Tracker for your daily consums for different things",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
