
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


from distutils.core import setup
import py2exe


setup(
      console=['main.py'],                                                      # Main python script file defined as console application
      name='Consum Tracker',                                                    # Name of the application
      version='1.0',                                                            # Main Version
      description='Simulator for FLG Communication',                            # Description
      author='Raphael Romann',                                                  # Autor
      author_email='admin@example.com',                                         # E-Mail
      packages=['src'],                                                         # onwn used package

      data_files=[('xml', ['xml/receive.xml', 'xml/simconfig.xml']),            # include example file to the distibution
                  ('script', ['script/down.fss', 'script/start.fss', 'script/Komp1_6.fss']),
                  ]

)
