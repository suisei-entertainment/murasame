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

# Platform Imports
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
        Contains tests for the base FrameworkError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise FrameworkError('test')
        except FrameworkError as error:
            assert error.errorcode == ErrorCodes.NOT_SET
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise FrameworkError('test', inspect_caller=False)
        except FrameworkError as error:
            assert error.errorcode == ErrorCodes.NOT_SET
            assert error.errormessage == 'test'

    def test_access_violation_error(self):

        """
        Contains tests for the AccessViolationError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise AccessViolationError('test')
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise AccessViolationError('test', inspect_caller=False)
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

    def test_already_registered_error(self):

        """
        Contains tests for the AlreadyRegisteredError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise AlreadyRegisteredError('test')
        except AlreadyRegisteredError as error:
            assert error.errorcode == ErrorCodes.ALREADY_REGISTERED
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise AlreadyRegisteredError('test', inspect_caller=False)
        except AlreadyRegisteredError as error:
            assert error.errorcode == ErrorCodes.ALREADY_REGISTERED
            assert error.errormessage == 'test'

    def test_already_exists_error(self):

        """
        Contains tests for the AlreadyExistsError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise AlreadyExistsError('test')
        except AlreadyExistsError as error:
            assert error.errorcode == ErrorCodes.ALREADY_EXISTS
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise AlreadyExistsError('test', inspect_caller=False)
        except AlreadyExistsError as error:
            assert error.errorcode == ErrorCodes.ALREADY_EXISTS
            assert error.errormessage == 'test'

    def test_input_error(self):

        """
        Contains tests for the InvalidInputError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise InvalidInputError('test')
        except InvalidInputError as error:
            assert error.errorcode == ErrorCodes.INPUT_ERROR
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise InvalidInputError('test', inspect_caller=False)
        except InvalidInputError as error:
            assert error.errorcode == ErrorCodes.INPUT_ERROR
            assert error.errormessage == 'test'

    def test_not_registered_error(self):

        """
        Contains tests for the NotRegisteredError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise NotRegisteredError('test')
        except NotRegisteredError as error:
            assert error.errorcode == ErrorCodes.NOT_REGISTERED
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise NotRegisteredError('test', inspect_caller=False)
        except NotRegisteredError as error:
            assert error.errorcode == ErrorCodes.NOT_REGISTERED
            assert error.errormessage == 'test'

    def test_permission_error(self):

        """
        Contains tests for the AccessViolation class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise AccessViolationError('test')
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise AccessViolationError('test', inspect_caller=False)
        except AccessViolationError as error:
            assert error.errorcode == ErrorCodes.PERMISSION_ERROR
            assert error.errormessage == 'test'

    def test_installation_failed_error(self):

        """
        Contains tests for the InstallationFailedError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise InstallationFailedError('test')
        except InstallationFailedError as error:
            assert error.errorcode == ErrorCodes.INSTALL_FAILED
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise InstallationFailedError('test', inspect_caller=False)
        except InstallationFailedError as error:
            assert error.errorcode == ErrorCodes.INSTALL_FAILED
            assert error.errormessage == 'test'

    def test_missing_requirement_error(self):

        """
        Contains tests for the MissingRequirementError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise MissingRequirementError('test')
        except MissingRequirementError as error:
            assert error.errorcode == ErrorCodes.MISSING_REQUIREMENT
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise MissingRequirementError('test', inspect_caller=False)
        except MissingRequirementError as error:
            assert error.errorcode == ErrorCodes.MISSING_REQUIREMENT
            assert error.errormessage == 'test'

    def test_uncaught_exception_error(self):

        """
        Contains tests for the UncaughtExceptionError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise UncaughtExceptionError('test')
        except UncaughtExceptionError as error:
            assert error.errorcode == ErrorCodes.UNCAUGHT_EXCEPTION
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise UncaughtExceptionError('test', inspect_caller=False)
        except UncaughtExceptionError as error:
            assert error.errorcode == ErrorCodes.UNCAUGHT_EXCEPTION
            assert error.errormessage == 'test'

    def test_invalid_license_key_error(self):

        """
        Contains tests for the InvalidLicenseKeyError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise InvalidLicenseKeyError('test')
        except InvalidLicenseKeyError as error:
            assert error.errorcode == ErrorCodes.LICENSE_ERROR
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise InvalidLicenseKeyError('test', inspect_caller=False)
        except InvalidLicenseKeyError as error:
            assert error.errorcode == ErrorCodes.LICENSE_ERROR
            assert error.errormessage == 'test'

    def test_database_operation_error(self):

        """
        Contains tests for the DatabaseOperationError class.
        """

        # STEP 1 - Test that the exception can be raised.
        try:
            raise DatabaseOperationError('test')
        except DatabaseOperationError as error:
            assert error.errorcode == ErrorCodes.DATABASE_ERROR
            assert error.errormessage == 'test'

        # STEP 2 - Test that the exception can be raised without caller
        # inspection.
        try:
            raise DatabaseOperationError('test', inspect_caller=False)
        except DatabaseOperationError as error:
            assert error.errorcode == ErrorCodes.DATABASE_ERROR
            assert error.errormessage == 'test'
