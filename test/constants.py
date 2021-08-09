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
Contains common constants used during testing.
"""

# Runtime Imports
import os

# Path to the Murasame workspace directory in the user's home directory
WORKSPACE_DIRECTORY = os.path.abspath(os.path.expanduser('~/.murasame'))

# Path where files used during testing are located
TEST_FILES_DIRECTORY = f'{WORKSPACE_DIRECTORY}/testfiles'

# The shebang string to use in the generated Python scripts.
SHEBANG_STRING = f'#!{WORKSPACE_DIRECTORY}/.env/bin/python'

# The license key to use when retrieving the GeoIP data
GEOIP_LICENSE_KEY = 'pELDCVUneMIsHhyU'

# The link from where a new GeoIP database can be downloaded
GEOIP_DOWNLOAD_URL = \
    f'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key={GEOIP_LICENSE_KEY}&suffix=tar.gz'
