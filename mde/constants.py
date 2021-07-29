## ============================================================================
##             **** Murasame Application Development Framework ****
##                Copyright (C) 2019-2021, Suisei Entertainment
## ============================================================================
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
## ============================================================================

"""
Contains common constants used by MDE.
"""

# Runtime Imports
import os

"""
The log level used by MDE.
"""
MDE_LOG_LEVEL = 'INFO'

"""
Name of the logger used by MDE.
"""
MDE_LOGGER_NAME = 'murasame.mde'

"""
Name of the repository on GitHub.
"""
REPOSITORY_NAME = 'suisei-entertainment/murasame'

"""
The template file used to generate the version file.
"""
VERSION_TEMPLATE_PATH = \
    os.path.abspath(os.path.expanduser('./scripts/version.conf.in'))

"""
The input file used to generate the version constant file.
"""
VERSION_CONSTANTS_TEMPLATE_PATH = \
    os.path.abspath(os.path.expanduser('./scripts/version.py.in'))

"""
The input file used to generate the setup script.
"""
SETUP_SCRIPT_TEMPLATE_PATH = \
    os.path.abspath(os.path.expanduser('./scripts/setup.py.in'))

"""
Path to the version file.
"""
VERSION_FILE_PATH = \
    os.path.abspath(os.path.expanduser('./version.conf'))

"""
Path to the version constants file.
"""
VERSION_CONSTANTS_PATH = \
    os.path.abspath(os.path.expanduser('./murasame/version.py'))

"""
Path to the setup script to use when building the Python wheel.
"""
SETUP_SCRIPT_PATH = \
    os.path.abspath(os.path.expanduser('./setup.py'))

"""
Path to the log file of the build script.
"""
LOG_FILE_PATH = \
    os.path.abspath(os.path.expanduser('~/.murasame/logs/build.log'))

"""
Path to the directory where the build output will be placed.
"""
DIST_PATH = \
    os.path.abspath(os.path.expanduser('~/.murasame/dist'))

MDE_BANNER = \
'\n@@@@@@@@@@   @@@  @@@  @@@@@@@    @@@@@@    @@@@@@    @@@@@@   @@@@@@@@@@   @@@@@@@@\n' + \
'@@@@@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@@  @@@@@@@@@@@  @@@@@@@@\n' + \
'@@! @@! @@!  @@!  @@@  @@!  @@@  @@!  @@@  !@@       @@!  @@@  @@! @@! @@!  @@!\n' + \
'!@! !@! !@!  !@!  @!@  !@!  @!@  !@!  @!@  !@!       !@!  @!@  !@! !@! !@!  !@!\n' + \
'@!! !!@ @!@  @!@  !@!  @!@!!@!   @!@!@!@!  !!@@!!    @!@!@!@!  @!! !!@ @!@  @!!!:!\n' + \
'!@!   ! !@!  !@!  !!!  !!@!@!    !!!@!!!!   !!@!!!   !!!@!!!!  !@!   ! !@!  !!!!!:\n' + \
'!!:     !!:  !!:  !!!  !!: :!!   !!:  !!!       !:!  !!:  !!!  !!:     !!:  !!:\n' + \
':!:     :!:  :!:  !:!  :!:  !:!  :!:  !:!      !:!   :!:  !:!  :!:     :!:  :!:\n' + \
':::     ::   ::::: ::  ::   :::  ::   :::  :::: ::   ::   :::  :::     ::    :: ::::\n' + \
':      :     : :  :    :   : :   :   : :  :: : :     :   : :   :      :    : :: ::   \n\n'


"""
Description string of the MDE tool.
"""
MDE_DESCRIPTION = 'Utility tool used for development of the Murasame framework.'

"""
Epilog string of the MDE tool.
"""
MDE_EPILOG = ''