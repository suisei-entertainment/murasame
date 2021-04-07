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
Contains the implementation of framework utilities.
"""

from murasame.utils.singleton import Singleton
from murasame.utils.systemlocator import SystemLocator, System
from murasame.utils.productversion import ProductVersion
from murasame.utils.aes import AESCipher
from murasame.utils.rsa import (
    RSAKeyLengths,
    RSAPrivate,
    RSAPublic,
    RSAKeyGenerator,
    RSASigner,
    RSAVerifier,
    RSAEncryptor,
    RSADecryptor)
from murasame.utils.jsonfile import JsonFile
from murasame.utils.yamlfile import YamlFile
from murasame.utils.secrets import Secrets
from murasame.utils.geoip import GeoIP, GeoIPData
from murasame.utils.cliprocessor import CliProcessor
from murasame.utils.dices import Dices
