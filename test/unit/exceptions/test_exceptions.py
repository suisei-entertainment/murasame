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
Contains the unit tests of the exception classes.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.exceptions import (
    AccessViolationError,
    AlreadyExistsError,
    AlreadyRegisteredError,
    ErrorCodes,
    FrameworkError,
    InstallationFailedError,
    InvalidInputError,
    MissingRequirementError,
    NotRegisteredError,
    UncaughtExceptionError,
    InvalidLicenseKeyError,
    DatabaseOperationError)

class TestExceptions:

    """
    Contains the unit tests for the exception classes.
    """

    def test_exception(self):

        """
        Tests that FrameworkError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise FrameworkError('test')
        except FrameworkError as error:
            assert error.errorcode == ErrorCodes.NOT_SET
            assert error.errormessage == 'test'

    def test_exception_without_caller_inspection(self):

        """
        Tests that FrameworkError can be raised without caller inspection
        enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise FrameworkError('test', inspect_caller=False)
        except FrameworkError as error:
            assert error.errorcode == ErrorCodes.NOT_SET
            assert error.errormessage == 'test'

    def test_access_violation_error(self):

        """
        Tests that AccessViolationError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise AccessViolationError('test')
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

    def test_access_violation_error_without_caller_inspection(self):

        """
        Tests that AccessViolationError can be raised without caller inspection
        enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise AccessViolationError('test', inspect_caller=False)
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

    def test_already_registered_error(self):

        """
        Tests that AlreadyRegisteredError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise AlreadyRegisteredError('test')
        except AlreadyRegisteredError as error:
            assert error.errorcode == ErrorCodes.ALREADY_REGISTERED
            assert error.errormessage == 'test'

    def test_already_registered_error_without_caller_inspection(self):

        """
        Tests that AlreadyRegisteredError can be raised without caller
        inspection enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise AlreadyRegisteredError('test', inspect_caller=False)
        except AlreadyRegisteredError as error:
            assert error.errorcode == ErrorCodes.ALREADY_REGISTERED
            assert error.errormessage == 'test'

    def test_already_exists_error(self):

        """
        Tests that AlreadyExistsError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise AlreadyExistsError('test')
        except AlreadyExistsError as error:
            assert error.errorcode == ErrorCodes.ALREADY_EXISTS
            assert error.errormessage == 'test'

    def test_already_exists_error_without_caller_inspection(self):

        """
        Tests that AlreadyExistsError can be raised without caller inspection
        enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise AlreadyExistsError('test', inspect_caller=False)
        except AlreadyExistsError as error:
            assert error.errorcode == ErrorCodes.ALREADY_EXISTS
            assert error.errormessage == 'test'

    def test_invalid_input_error(self):

        """
        Tests that InvalidInputError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise InvalidInputError('test')
        except InvalidInputError as error:
            assert error.errorcode == ErrorCodes.INPUT_ERROR
            assert error.errormessage == 'test'

    def test_invalid_input_error_without_caller_inspection(self):

        """
        Tests that InvalidInputError can be raised without caller inspection
        enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise InvalidInputError('test', inspect_caller=False)
        except InvalidInputError as error:
            assert error.errorcode == ErrorCodes.INPUT_ERROR
            assert error.errormessage == 'test'

    def test_not_registered_error(self):

        """
        Tests that NotRegisteredError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise NotRegisteredError('test')
        except NotRegisteredError as error:
            assert error.errorcode == ErrorCodes.NOT_REGISTERED
            assert error.errormessage == 'test'

    def test_not_registered_error_without_caller_inspection(self):

        """
        Tests that NotRegisteredError can be raised without caller inspection
        enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise NotRegisteredError('test', inspect_caller=False)
        except NotRegisteredError as error:
            assert error.errorcode == ErrorCodes.NOT_REGISTERED
            assert error.errormessage == 'test'

    def test_permission_error(self):

        """
        Tests that AccessViolation can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise AccessViolationError('test')
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

    def test_permission_error_without_caller_inspection(self):

        """
        Tests that AccessViolation can be raised without caller inspection
        enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise AccessViolationError('test', inspect_caller=False)
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

    def test_installation_failed_error(self):

        """
        Tests that InstallationFailedError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise InstallationFailedError('test')
        except InstallationFailedError as error:
            assert error.errorcode == ErrorCodes.INSTALL_FAILED
            assert error.errormessage == 'test'

    def test_installation_failed_error_without_caller_inspection(self):

        """
        Tests that InstallationFailedError can be raised without caller
        inspection enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise InstallationFailedError('test', inspect_caller=False)
        except InstallationFailedError as error:
            assert error.errorcode == ErrorCodes.INSTALL_FAILED
            assert error.errormessage == 'test'

    def test_missing_requirement_error(self):

        """
        Tests that MissingRequirementError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise MissingRequirementError('test')
        except MissingRequirementError as error:
            assert error.errorcode == ErrorCodes.MISSING_REQUIREMENT
            assert error.errormessage == 'test'

    def test_missing_requirement_error_without_caller_inspection(self):

        """
        Tests that MissingRequirementError can be raised without caller
        inspection enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise MissingRequirementError('test', inspect_caller=False)
        except MissingRequirementError as error:
            assert error.errorcode == ErrorCodes.MISSING_REQUIREMENT
            assert error.errormessage == 'test'

    def test_uncaught_exception_error(self):

        """
        Tests that UncaughtExceptionError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise UncaughtExceptionError('test')
        except UncaughtExceptionError as error:
            assert error.errorcode == ErrorCodes.UNCAUGHT_EXCEPTION
            assert error.errormessage == 'test'

    def test_uncaught_exception_error_without_caller_inspection(self):

        """
        Tests that UncaughtExceptionError can be raised without caller
        inspection enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise UncaughtExceptionError('test', inspect_caller=False)
        except UncaughtExceptionError as error:
            assert error.errorcode == ErrorCodes.UNCAUGHT_EXCEPTION
            assert error.errormessage == 'test'

    def test_invalid_license_key_error(self):

        """
        Tests that InvalidLicenseKeyError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise InvalidLicenseKeyError('test')
        except InvalidLicenseKeyError as error:
            assert error.errorcode == ErrorCodes.LICENSE_ERROR
            assert error.errormessage == 'test'

    def test_invalid_license_key_error_without_caller_inspection(self):

        """
        Tests that InvalidLicenseKeyError can be raised without caller
        inspection enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise InvalidLicenseKeyError('test', inspect_caller=False)
        except InvalidLicenseKeyError as error:
            assert error.errorcode == ErrorCodes.LICENSE_ERROR
            assert error.errormessage == 'test'

    def test_database_operation_error(self):

        """
        Tests that DatabaseOperationError can be raised.

        Authors:
            Attila Kovacs
        """

        try:
            raise DatabaseOperationError('test')
        except DatabaseOperationError as error:
            assert error.errorcode == ErrorCodes.DATABASE_ERROR
            assert error.errormessage == 'test'

    def test_database_operation_error_without_caller_inspection(self):

        """
        Tests that DatabaseOperationError can be raised without caller
        inspection enabled.

        Authors:
            Attila Kovacs
        """

        try:
            raise DatabaseOperationError('test', inspect_caller=False)
        except DatabaseOperationError as error:
            assert error.errorcode == ErrorCodes.DATABASE_ERROR
            assert error.errormessage == 'test'
