
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
Contains the unit tests of the Localizer class.
"""

# Runtime Imports
import os
import sys
import shutil

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils import SystemLocator, YamlFile
from murasame.pal.vfs import VFS, DefaultVFS
from murasame.localization import Localizer

LANGUAGE_FILES_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/localizer/'))
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

class TestLocalizer:

    """
    Contains the unit tests of the Localizer class.
    """

    @classmethod
    def setup_class(cls):

        if os.path.isfile(f'{LOCALIZATIONS_PATH}/en.yaml'):
            os.remove(f'{LOCALIZATIONS_PATH}/en.yaml')

        if os.path.isfile(f'{LOCALIZATIONS_PATH}/de.yaml'):
            os.remove(f'{LOCALIZATIONS_PATH}/de.yaml')

        if os.path.isfile(f'{LOCALIZATIONS_PATH}/ja.yaml'):
            os.remove(f'{LOCALIZATIONS_PATH}/ja.yaml')

        if os.path.isdir(LOCALIZATIONS_PATH):
            os.rmdir(LOCALIZATIONS_PATH)

        if os.path.isdir(LANGUAGE_FILES_PATH):
            os.rmdir(LANGUAGE_FILES_PATH)

        os.mkdir(LANGUAGE_FILES_PATH)
        os.mkdir(LOCALIZATIONS_PATH)

        en = YamlFile(path=f'{LOCALIZATIONS_PATH}/en.yaml')
        en.overwrite_content(content=EN)
        en.save()
        de = YamlFile(path=f'{LOCALIZATIONS_PATH}/de.yaml')
        de.overwrite_content(content=DE)
        de.save()
        ja = YamlFile(path=f'{LOCALIZATIONS_PATH}/ja.yaml')
        ja.overwrite_content(content=JA)
        ja.save()

        SystemLocator.instance().register_provider(VFS, DefaultVFS())
        vfs = SystemLocator.instance().get_provider(VFS)
        vfs.register_source(path=LANGUAGE_FILES_PATH)

    @classmethod
    def teardown_class(cls):

        SystemLocator.instance().reset()

    def test_creation(self):

        """
        Tests that a Localizer instance can be created.
        """

        # STEP #1 - Localizer can be created with default parameters
        sut = Localizer()

        # STEP #2 - Localizer can be created with custom language
        sut = Localizer(language='hu', default_language='ja', cache_default=True)

        # STEP #3 - Localizer can be created with Google Translate enabled.
        sut = Localizer(language='de', auto_translate=True)

    def test_retrieving_entries(self):

        """
        Tests that localized texts can be retrieved from the Localizer.
        """

        # STEP #1 - Simple retrieval
        sut = Localizer()
        assert sut.get(key='test_key') == 'test_data_en'

    def test_switching_language(self):

        """
        Tests that language can be switched at runtime.
        """
        sut = Localizer()
        assert sut.get(key='test_key') == 'test_data_en'
        sut.switch_language(new_language='de')
        assert sut.get(key='test_key') == 'test_data_de'

    def test_autotranslate(self):

        """
        Tests that non-existent entries can be localized using Google
        Translate.
        """

        sut = Localizer(language='de', auto_translate=True)
        assert sut.get(key='autotranslate_key') == 'Schiff'

    def test_update(self):

        """
        Tests the update of localization files.
        """

        # STEP #1 - Test with reloading the default language as well
        sut = Localizer(language='en', default_language='en', cache_default=True)
        sut.update_localizations()
        assert sut.get(key='test_key') == 'test_data_en'

        # STEP #2 - Test without reloading the default language
        sut = Localizer(language='en', default_language='en', cache_default=False)
        sut.update_localizations()
        assert sut.get(key='test_key') == 'test_data_en'
