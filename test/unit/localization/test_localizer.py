
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
from murasame.api import VFSAPI
from murasame.pal.vfs import VFS
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

    Authors:
        Attila Kovacs
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

        SystemLocator.instance().register_provider(VFSAPI, VFS())
        vfs = SystemLocator.instance().get_provider(VFSAPI)
        vfs.register_source(path=LANGUAGE_FILES_PATH)

    @classmethod
    def teardown_class(cls):

        SystemLocator.instance().reset()

    def test_creation_with_default_parameters(self):

        """
        Tests that a Localizer instance can be created with default parameters.

        Authors:
            Attila Kovacs
        """

        sut = Localizer()

        assert sut is not None

    def test_creation_with_custom_language(self):

        """
        Tests that a Localizer instance can be created with a custom language.

        Authors:
            Attila Kovacs
        """

        sut = Localizer(language='hu', default_language='ja', cache_default=True)

        assert sut is not None

    def test_creation_with_google_translate_enabled(self):

        """
        Tests that a Localizer instance can be created with Google Translate
        enabled.

        Authors:
            Attila Kovacs
        """

        sut = Localizer(language='de', auto_translate=True)

        assert sut is not None

    def test_retrieving_entries(self):

        """
        Tests that localized texts can be retrieved from the Localizer.

        Authors:
            Attila Kovacs
        """

        sut = Localizer()
        assert sut.get(key='test_key') == 'test_data_en'

    def test_switching_language(self):

        """
        Tests that language can be switched at runtime.

        Authors:
            Attila Kovacs
        """

        sut = Localizer()
        assert sut.get(key='test_key') == 'test_data_en'
        sut.switch_language(new_language='de')
        assert sut.get(key='test_key') == 'test_data_de'

    def test_autotranslate(self):

        """
        Tests that non-existent entries can be localized using Google
        Translate.

        Authors:
            Attila Kovacs
        """

        sut = Localizer(language='de', auto_translate=True)
        assert sut.get(key='autotranslate_key') == 'Schiff'

    def test_update_with_reloading_default_language(self):

        """
        Tests the update of localization files with reloading the default
        language.

        Authors:
            Attila Kovacs
        """

        sut = Localizer(language='en', default_language='en', cache_default=True)
        sut.update_localizations()
        assert sut.get(key='test_key') == 'test_data_en'

    def test_update_without_reloading_default_language(self):

        """
        Tests the update of localization files without reloading the default
        language.

        Authors:
            Attila Kovacs
        """

        sut = Localizer(language='en', default_language='en', cache_default=False)
        sut.update_localizations()
        assert sut.get(key='test_key') == 'test_data_en'
