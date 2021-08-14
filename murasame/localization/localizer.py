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
Contains the implementation of the Localizer class.
"""

# Runtime Imports
from string import Template

# Dependency Imports
import httpx
from googletrans import Translator

# Murasame Imports
from murasame.constants import (
    MURASAME_LOCALIZER_LOG_CHANNEL,
    MURASAME_DEFAULT_LOCALIZATION_PATH)
from murasame.log.logwriter import LogWriter
from murasame.api import VFSAPI
from murasame.utils import SystemLocator

"""
List of supported languages as specified by Google at
https://cloud.google.com/translate/docs/languages.
"""
SUPPORTED_LANGUAGES = \
[
    'af',   # Afrikaans
    'sq',   # Albanian
    'am',   # Amharic
    'ar',   # Arabic
    'hy',   # Armenian
    'az',   # Azerbaijani
    'eu',   # Basque
    'be',   # Belarusian
    'bn',   # Bengali
    'bs',   # Bosnian
    'bg',   # Bulgarian
    'ca',   # Catalan
    'ceb',  # Cebuano
    'zh',   # Chinese (Simplified)
    'zh-TW',# Chinese (Traditional)
    'co',   # Corsican
    'hr',   # Croatian
    'cs',   # Czech
    'da',   # Danish
    'nl',   # Dutch
    'en',   # English
    'eo',   # Esperanto
    'et',   # Estonian
    'fi',   # Finnish
    'fr',   # French
    'fy',   # Frisian
    'gl',   # Galician
    'ka',   # Georgian
    'de',   # German
    'el',   # Greek
    'gu',   # Gujarati
    'ht',   # Haitian Creole
    'ha',   # Hausa
    'haw',  # Hawaiian (ISO-639-2)
    'he',   # Hebrew
    'iw',   # Hebrew
    'hi',   # Hindi
    'hmn',  # Hmong (ISO-639-2)
    'hu',   # Hungarian
    'is',   # Icelandic
    'ig',   # Igbo
    'id',   # Indonesian
    'ga',   # Irish
    'it',   # Italian
    'ja',   # Japanese
    'jv',   # Javanese
    'kn',   # Kannada
    'kk',   # Kazakh
    'km',   # Khmer
    'rw',   # Kinyarwanda
    'ko',   # Korean
    'ku',   # Kurdish
    'ky',   # Kyrgyz
    'lo',   # Lao
    'la',   # Latin
    'lv',   # Latvian
    'lt',   # Lithuanian
    'lb',   # Luxembourgish
    'mk',   # Macedonian
    'mg',   # Malagasy
    'ms',   # Malay
    'ml',   # Malayalam
    'mt',   # Maltese
    'mi',   # Maori
    'mr',   # Marathi
    'mn',   # Mongolian
    'my',   # Myanmar (Burmese)
    'ne',   # Nepali
    'no',   # Norwegian
    'ny',   # Nyanja (Chichewa)
    'or',   # Odia (Oriya)
    'ps',   # Pashto
    'fa',   # Persian
    'pl',   # Polish
    'pt',   # Portuguese (Portugal, Brazil)
    'pa',   # Punjabi
    'ro',   # Romanian
    'ru',   # Russian
    'sm',   # Samoan
    'gd',   # Scots Gaelic
    'sr',   # Serbian
    'st',   # Sesotho
    'sn',   # Shona
    'sd',   # Sindhi
    'si',   # Sinhala (Sinhalese)
    'sk',   # Slovak
    'sl',   # Slovenian
    'so',   # Somali
    'es',   # Spanish
    'su',   # Sundanese
    'sw',   # Swahili
    'sv',   # Swedish
    'tl',   # Tagalog (Filipino)
    'tg',   # Tajik
    'ta',   # Tamil
    'tt',   # Tatar
    'te',   # Telugu
    'th',   # Thai
    'tr',   # Turkish
    'tk',   # Turkmen
    'uk',   # Ukrainian
    'ur',   # Urdu
    'ug',   # Uyghur
    'uz',   # Uzbek
    'vi',   # Vietnamese
    'cy',   # Welsh
    'xh',   # Xhosa
    'yi',   # Yiddish
    'yo',   # Yoruba
    'zu'    # Zulu
]

class Localizer(LogWriter):

    """Utility class to translate strings and fill in optional variables inside
    them.

    It also supports automatic translation of strings through the Google
    Translate API.

    This localizer will load localization files from the virtual file system
    node /localization.

    Attributes:
        _language (str): The selected language of the application.

        _default_language (str): The default language to use.

        _auto_translate (bool): Whether or not missing translations should be
            automatically translated through Google Translate.

        _cache_default (bool): Whether or not the default language file should
            also be loaded into memory.

        _data (dict): The loaded language data.

        _default_data (dict): The loaded default language data.

        _localization_directory (str): The directory in the virtual file system
            that contains the localization files.


    Authors:
        Attila Kovacs
    """

    def __init__(
        self,
        language: str = 'en',
        default_language: str = 'en',
        cache_default: bool = False,
        auto_translate: bool = False,
        localization_directory=MURASAME_DEFAULT_LOCALIZATION_PATH) -> None:

        """Creates a new Localizer instance.

        Args:
            language (str): The selected language of the application.

            default_language (str): The default locale to use when looking for
                texts.

            cache_default (bool): Whether or not the default language file
                should also be loaded.

            auto_translate (bool): Automatically translate the text from the
                default language if no translated version was found.

            localization_directory (str): The VFS directory in which the
                language files are located.
        """

        super().__init__(channel_name=MURASAME_LOCALIZER_LOG_CHANNEL,
                         cache_entries=True)

        self._language = language
        self._default_language = default_language
        self._auto_translate = auto_translate
        self._cache_default = cache_default
        self._data = None
        self._default_data = None
        self._localization_directory = localization_directory

        self._load_language()
        if self._cache_default:
            self._cache_default_language()

    def get(self, key: str, attributes: dict = None) -> str:

        """Retrieves the localized version of the given localization key and
        also fills any dynamic variables in the text.

        Args:
            key (str): The localization key to retrieve.
            attributes (dict): List of dynamic attributes to substitute.
        """

        self.debug(f'Retrieving localized text for key {key}...')

        localized_text = None

        try:
            localized_text = self._data[key]
        except KeyError:
            self.debug(f'Localization key {key} was not found in the current '
                       f'language.')
            localized_text = self._load_default_text(key=key)
            if self._auto_translate:
                self.debug(f'Attempting to translate {key}({localized_text}) '
                           f'to language {self._language}.')
                localized_text = self._translate_text(text=localized_text)
                self.debug(f'Received translation for {key}: {localized_text}')

        if attributes:
            self.debug(f'Substituting supplied attributes in localized text '
                       f'for {key}.')
            localized_text = Template(localized_text).safe_substitute(
                mapping=attributes)

        self.debug(f'Final localized text for {key}: {localized_text}')

        return localized_text

    @staticmethod
    def is_valid_language(language: str) -> bool:

        """Returns whether or not a given language code is valid.

        Args:
            language (str): The language code to check.

        Returns:
            bool: 'True' if the given language code is supported, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        return language in SUPPORTED_LANGUAGES

    def switch_language(self, new_language: str) -> None:

        """Changes the language of the localizer.

        Args:
            new_language: (str) The new language to set in the localizer.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Switching localization language from {self._language} '
                   f'to {new_language}.')

        self._language = new_language
        self._load_language()

        self.debug(f'Localization language was set to {new_language}.')

    def update_localizations(self) -> None:

        """Reloads the localization files to pick up updates.

        Authors:
            Attila Kovacs
        """

        self._data = self._load_language_file(language=self._language)
        if self._cache_default:
            self._default_data = self._load_language_file(
                language=self._default_language)

    def _load_language_file(self, language: str) -> dict:

        """Loads a language file from the virtual file system.

        Args:
            language (str): The language file to load.

        Returns:
            dict: The contents of the language file as a dictionary.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Loading language file for language {language}...')

        # Pylint cannot see the instance() function in SystemLocator
        #pylint: disable=no-member
        vfs = SystemLocator.instance().get_provider(VFSAPI)

        if not vfs:
            raise RuntimeError(
                'Failed to retrieve the VFS from the system locator.')

        data = vfs.get_content(
            key=f'{self._localization_directory}/{language}.yaml')

        if data is None:
            self.error(f'Failed to load language file for language '
                       f'{language}.')
        else:
            self.debug(f'Language file for language {language} has been '
                       f'loaded.')

        return data

    def _load_language(self) -> None:

        """Loads the language file corresponding to the selected application
        language into memory.

        Raises:
            RuntimeError: Raised when the virtual file system cannot be
                retrieved.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Loading language {self._language}...')
        self._data = self._load_language_file(language=self._language)
        self.debug(f'Language {self._language} has been loaded.')

    def _cache_default_language(self) -> None:

        """Loads the default language file into memory to speed up retrieval of
        default language texts when the translation is missing.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Loading default language file for language '
                   f'{self._default_language} to memory.')
        self._default_data = self._load_language_file(
            language=self._default_language)
        self.debug('Default language file loaded to memory.')

    def _load_default_text(self, key: str) -> str:

        """Loads the default version of the given localization key.

        Args:
            key (str): The localization key to load.

        Returns:
            str: The text corresponding to the given localization key from the
            default language file.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Loading default localization text for {key}.')

        if self._cache_default:
            return self._default_language[key]

        data = self._load_language_file(language=self._default_language)

        text = None
        try:
            text = data[key]
        except KeyError:
            self.error(f'Localization key {key} is not found in the default '
                       f'language file.')
            text = 'KEY NOT FOUND'

        return text

    def _translate_text(self, text: str) -> str:

        """Translates the given text using Google Translate.

        Args:
            text (str): The text to translate.

        Returns:
            str: The translated text.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Attempting to translate {text} to {self._language}...')

        translator = Translator()
        try:
            translation = translator.translate(
                text,
                src=self._default_language,
                dest=self._language)
        except httpx.HTTPError as error:
            self.error(
                f'Failed to translate text {text}. Reason: {error}')
            return text

        self.debug(f'Received translation for {text}: {translation.text}.')

        return translation.text
