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
Contains the various exceptions used by the framework.
"""

from murasame.exceptions.errorcodes import ErrorCodes
from murasame.exceptions.exception import FrameworkError
from murasame.exceptions.alreadyregisterederror import AlreadyRegisteredError
from murasame.exceptions.alreadyexistserror import AlreadyExistsError
from murasame.exceptions.accessviolationerror import AccessViolationError
from murasame.exceptions.notregisterederror import NotRegisteredError
from murasame.exceptions.invalidinputerror import InvalidInputError
from murasame.exceptions.uncaughtexceptionerror import UncaughtExceptionError
from murasame.exceptions.missingrequirementerror import MissingRequirementError
from murasame.exceptions.installationfailederror import InstallationFailedError
from murasame.exceptions.invalidlicensekeyerror import InvalidLicenseKeyError
from murasame.exceptions.databaseoperationerror import DatabaseOperationError
