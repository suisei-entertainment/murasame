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
Contains the test data for the localization tests.
"""

# Runtime Imports
import os

# Murasame Imports
from murasame.utils import YamlFile

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

LANGUAGE_FILES_PATH = f'{TEST_FILES_DIRECTORY}/localizer'
LOCALIZATIONS_PATH = f'{LANGUAGE_FILES_PATH}/localization'

EN = \
{
    'test_key': 'test_data_en',
    'autotranslate_key': 'ship'
}

DE = \
{
    'test_key': 'test_data_de'
}

JA = \
{
    'test_key': 'test_data_ja'
}

def create_localizer_data():

    # Create directories
    os.mkdir(LANGUAGE_FILES_PATH)
    os.mkdir(LOCALIZATIONS_PATH)

    # Create files
    en = YamlFile(path=f'{LOCALIZATIONS_PATH}/en.yaml')
    en.overwrite_content(content=EN)
    en.save()

    de = YamlFile(path=f'{LOCALIZATIONS_PATH}/de.yaml')
    de.overwrite_content(content=DE)
    de.save()

    ja = YamlFile(path=f'{LOCALIZATIONS_PATH}/ja.yaml')
    ja.overwrite_content(content=JA)
    ja.save()
