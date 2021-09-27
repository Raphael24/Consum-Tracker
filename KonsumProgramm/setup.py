# Usage of this setup Script to generate an exe
#
# 0. Install the normal Python interpretor!
# 1. Install py3exe vom the folder ..\py3exe\
# 2. Open new Console
# 3. Navigate to this Folder, where this file is stored
# 4. Enter command "python setup.py py2exe"
# 5. OR: Oben file ant_build.xml and make target!
#
# Author: Raphael Romann
# 24.09.2021


#from setuptools import setup
from cx_Freeze import setup, Executable

setup(
      name='Consum Tracker',                                                    # Name of the application
      version='1.0',                                                            # Main Version
      description='Simulator for FLG Communication',                            # Description
      author='Raphael Romann',                                                  # Autor
      author_email='admin@example.com',                                         # E-Mail
      py_modules = ["main", "dbconsum"],                                        # onwn used package
      package_data = {"main" : ["consum.ui"]},                                  #other addicted files for the programm
      executables = [Executable("main.py")]                                     # Main python script file defined as console application


)
