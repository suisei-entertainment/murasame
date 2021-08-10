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
Contains the utilities for X.509 certificate handling.
"""

# Runtime Imports
import os

import datetime
from pathlib import Path
from typing import Callable, Union

# Dependency Imports
import cryptography.x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils.rsa import RSAPrivate

class X509GenericCertificateFields:

    """Container for a list of common name fields in a certificate.

    Attributes:
        _common_name (str): The common name of the certificate.

        _country (str): The country of the certificate.

        _state (str): The state of the certificate.

        _locality (str): The locality of the certificate.

        _address (str): The address of the certificate.

        _organization (str): The organization of the certificate.

        _org_unit (str): The organization unit of the certificate.

        _serial (int): The serial of the certificate.

        _surname (str): The surname of the certificate.

        _given_name (str): The given name of the certificate.

        _title (str): The title of the certificate.

        _email (str): The email address of the certificate.

        _san (str): The Subject Alternate Name of the certificate.

    Authors:
        Attila Kovacs
    """

    @property
    def CommonName(self) -> str:

        """The common name stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._common_name

    @property
    def Country(self) -> str:

        """The country name stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._country

    @property
    def State(self) -> str:

        """The state name stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._state

    @property
    def Locality(self) -> str:

        """The locality name stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._locality

    @property
    def Address(self) -> str:

        """The postal address stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._address

    @property
    def Organization(self) -> str:

        """The organization name stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._organization

    @property
    def OrganizationalUnit(self) -> str:

        """The organization unit name stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._org_unit

    @property
    def Serial(self) -> int:

        """The serial number stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._serial

    @property
    def Surname(self) -> str:

        """The surname stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._surname

    @property
    def GivenName(self) -> str:

        """The given name stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._given_name

    @property
    def Title(self) -> str:

        """The title stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._title

    @property
    def Email(self) -> str:

        """The email address stored in the certificate.

        Authors:
            Attila Kovacs
        """

        return self._email

    @property
    def SAN(self) -> str:

        """Returns the Subject Alternate Name of the certificate.

        Authors:
            Attila Kovacs
        """

        return self._san

    @property
    def Subject(self) -> 'cryptography.x509.Name':

        """Returns the content as a Name object.

        Authors:
            Attila Kovacs
        """

        return self._build_name()

    def __init__(
        self,
        common_name: str = None,
        country: str = None,
        state: str = None,
        locality: str = None,
        address: str = None,
        organization: str = None,
        org_unit: str = None,
        serial: str = None,
        surname: str = None,
        given_name: str = None,
        title: str = None,
        email: str = None,
        san: str = None) -> None:

        """
        Creates a new X509GenericCertificateFields instance.

        Args:
            common_name (str): The common name of the certificate.

            country (str): The country of the certificate.

            state (str): The state of the certificate.

            locality (str): The locality of the certificate.

            address (str): The address of the certificate.

            organization (str): The organization of the certificate.

            org_unit (str): The organization unit of the certificate.

            serial (str): The serial number of the certificate.

            surname (str): The surname of the certificate.

            given_name (str): The given name of the certificate.

            title (str): The title of the certificate.

            email (str): The email address of the certificate.

            san (str): The subject alternate name of the certificate.

        Authors:
            Attila Kovacs
        """

        self._common_name = common_name
        self._country = country
        self._state = state
        self._locality = locality
        self._address = address
        self._organization = organization
        self._org_unit = org_unit
        self._serial = serial
        self._surname = surname
        self._given_name = given_name
        self._title = title
        self._email = email
        self._san = san

    def _build_name(self) -> 'cryptography.x509.Name':

        """Builds an X.509 name object out of the content stored in the class.

        Returns:
            cryptography.x509.Name: The generated name object.

        Authors:
            Attila Kovacs
        """

        oid_list = []

        # Common name
        if self._common_name is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.COMMON_NAME,
                value=self._common_name))

        # Country
        if self._country is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.COUNTRY_NAME,
                value=self._country))

        # State
        if self._state is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.STATE_OR_PROVINCE_NAME,
                value=self._state))

        # Locality
        if self._locality is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.LOCALITY_NAME,
                value=self._locality))

        # Address
        if self._address is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.STREET_ADDRESS,
                value=self._address))

        # Organization
        if self._organization is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.ORGANIZATION_NAME,
                value=self._organization))

        # Organization Unit
        if self._org_unit is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.ORGANIZATIONAL_UNIT_NAME,
                value=self._org_unit))

        # Serial
        if self._serial is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.SERIAL_NUMBER,
                value=str(self._serial)))

        # Surname
        if self._surname is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.SURNAME,
                value=self._surname))

        # Given Name
        if self._given_name is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.GIVEN_NAME,
                value=self._given_name))

        # Title
        if self._title is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.TITLE,
                value=self._title))

        # Email
        if self._email is not None:
            oid_list.append(cryptography.x509.NameAttribute(
                oid=cryptography.x509.NameOID.EMAIL_ADDRESS,
                value=self._email))

        return cryptography.x509.Name(oid_list)

class X509Certificate:

    """Utility class that represents a single X.509 certificate.

    Attributes:

       _certificate (object): The actual certificate object.

        _private_key (RSAPrivate): The private key associated with the
            certificate.

        _certificate_path (str): Path to the certificate.

        _private_key_path (str): Path to the private key associated with the
            certificate.

        _cb_retrieve_password (Callable): Callback function used to retrieve
            the password to decrypt the private key.

    Authors:
        Attila Kovacs
    """

    @property
    def Version(self) -> Union[int, None]:

        """Provides access to the version of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.version

        return None

    @property
    def Fingerprint(self) -> Union[bytes, None]:

        """Returns the fingerprint of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.fingerprint(
                cryptography.hazmat.primitives.hashes.SHA256())

        return None

    @property
    def SerialNumber(self) -> Union[int, None]:

        """Returns the serial number of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.serial_number

        return None

    @property
    def PublicKey(self) -> Union[bytes, None]:

        """Returns the public key of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.public_key().public_bytes(
                cryptography.hazmat.primitives.serialization.Encoding.PEM,
                cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo)

        return None

    @property
    def NotValidBefore(self) -> Union['datetime', None]:

        """Returns the beginning of the validity period of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.not_valid_before

        return None

    @property
    def NotValidAfter(self) -> Union['datetime', None]:

        """Returns the end of the validity period of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.not_valid_after

        return None

    @property
    def IsValid(self) -> bool:

        """Returns whether or not the certificate is valid.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            time = datetime.datetime.now()
            return self.NotValidAfter >= time >= self.NotValidBefore

        return False

    @property
    def CommonName(self) -> Union[str, None]:

        """Returns the common name of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.subject.get_attributes_for_oid(
                oid=cryptography.x509.NameOID.COMMON_NAME)[0].value

        return None

    @property
    def Issuer(self) -> Union[str, None]:

        """Returns the issuer of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.issuer.get_attributes_for_oid(
                oid=cryptography.x509.NameOID.COMMON_NAME)[0].value

        return None

    @property
    def Signature(self) -> Union[bytes, None]:

        """Returns the signature of the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.signature

        return None

    @property
    def SignatureHashAlgorithm(self) -> Union['HashAlgorithm', None]:

        """Returns the signature hash algorithm used in the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.signature_hash_algorithm

        return None

    @property
    def SignatureAlgorithmOID(self) -> Union['ObjectIdentifier', None]:

        """Returns the OID of the signature algorithm used in the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.signature_algorithm_oid

        return None

    @property
    def Extensions(self) -> Union['Extensions', None]:

        """Returns the extensions encoded in the certificate.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.extensions

        return None

    @property
    def CertificateBytes(self) -> Union[bytes, None]:

        """Returns the certificate bytes.

        Authors:
            Attila Kovacs
        """

        if self._certificate is not None:
            return self._certificate.tbs_certificate_bytes

        return None

    def __init__(
        self,
        certificate_path: str = None,
        private_key_path: str = None,
        cb_retrieve_password: Callable = None):

        """Creates a new X509Certificate object.

        Args:
            certificate_path (str): Path to the file containing the certificate.

            private_key_path (str): Path to the file containing the private key
                associated with the certificate.

            cb_retrieve_password (Callable): Callback function that when
                called, should return the password to be used to decrypt the
                private key.

        Authors:
            Attila Kovacs
        """

        self._certificate = None
        self._private_key = None
        self._certificate_path = certificate_path
        self._private_key_path = private_key_path
        self._cb_retrieve_password = cb_retrieve_password

        if self._certificate_path is not None:
            self.load(
                certificate_path=self._certificate_path,
                private_key_path=self._private_key_path,
                cb_retrieve_password=self._cb_retrieve_password)

    def load(
        self,
        certificate_path: str = None,
        private_key_path: str = None,
        cb_retrieve_password: Callable = None) -> None:

        """Loads the certificate from disk.

        Args:
            certificate_path (str): Path to the file containing the certificate.

            private_key_path (str): Path to the file containing the private key
                associated with the certificate.

            cb_retrieve_password (Callable): Callback function that when
                called, should return the password to be used to decrypt the
                private key.

        Raises:
            InvalidInputError: Raised when an invalid certificate path is
                provided.

            InvalidInputError: Raised when an invalid private key path is
                provided.

        Authors:
            Attila Kovacs
        """

        # Load the certificate itself
        real_cert_path = Path(os.path.abspath(
            os.path.expanduser(certificate_path)))

        if not real_cert_path.exists():
            raise InvalidInputError(
                f'The certificate file {real_cert_path} does not exist.')

        try:
            with open(real_cert_path, 'rb') as file:
                self._certificate = cryptography.x509.load_pem_x509_certificate(
                    data=file.read(), backend=default_backend())
        except ValueError as error:
            raise InvalidInputError(
                f'The certificate file {real_cert_path} cannot be loaded, it '
                f'appears to be invalid.') from error

        # Load the private key if a path is provided
        if private_key_path is not None:
            self._private_key = RSAPrivate(
                key_path=private_key_path,
                cb_retrieve_password=cb_retrieve_password)

    def save(
        self,
        certificate_path: str = None,
        private_key_path: str = None,
        cb_retrieve_password: Callable = None) -> None:

        """Saves the certificate to disk.

        Args:
            certificate_path (str): Path to the file containing the certificate.

            private_key_path (str): Path to the file containing the private key
                associated with the certificate.

            cb_retrieve_password (Callable): Callback function that when
                called, should return the password to be used to encrypt the
                    private key.

        Authors:
            Attila Kovacs
        """

        if self._certificate is None:
            return

        # Update certificate path if requested
        if certificate_path is not None:
            self._certificate_path = certificate_path

        # Update private key path if requested
        if private_key_path is not None:
            self._private_key_path = private_key_path

        # Update password retrieval function if requested
        if cb_retrieve_password is not None:
            self._cb_retrieve_password = cb_retrieve_password

        # Save certificate
        real_cert_path = Path(os.path.abspath(
            os.path.expanduser(self._certificate_path)))

        with open(real_cert_path, 'wb') as cert_file:
            cert_file.write(self._certificate.public_bytes(
                encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM))

        # Save private key
        pem = None

        if self._cb_retrieve_password is not None:

            pem = self._private_key.Key.private_bytes(
                encoding = cryptography.hazmat.primitives.serialization.Encoding.PEM,
                format=cryptography.hazmat.primitives.serialization.PrivateFormat.PKCS8,
                encryption_algorithm=cryptography.hazmat.primitives.serialization.BestAvailableEncryption(
                    self._cb_retrieve_password))

        else:

            pem = self._private_key.Key.private_bytes(
                encoding = cryptography.hazmat.primitives.serialization.Encoding.PEM,
                format=cryptography.hazmat.primitives.serialization.PrivateFormat.PKCS8,
                encryption_algorithm=cryptography.hazmat.primitives.serialization.NoEncryption())

        lines = pem.splitlines()

        with open(self._private_key_path, 'wb') as private_key_file:
            for line in lines:
                private_key_file.write(line)
                private_key_file.write(b'\n')

    def generate(
        self,
        certificate_path: str,
        descriptor: 'X509GenericCertificateFields',
        private_key: 'RSAPrivate' = None,
        not_valid_before: datetime.datetime = None,
        not_valid_after: datetime.datetime = None) -> None:

        """Generates a new self signed certificate.

        Args:
            certificate_path (str): Path where the new certificate will be
                saved.

            descriptor (X509GenericCertificateFields): The certificate
                descriptor.

            private_key (RSAPrivate): The private key to use to generate the
                certificate.

            not_valid_before (datetime): The time when the certificate becomes
                valid.

            not_valid_after (datetime): The time when the certificate expires.

        Authors:
            Attila Kovacs
        """

        self._private_key = private_key

        # If there is no start date specified, use the current date
        if not_valid_before is None:
            not_valid_before = datetime.datetime.utcnow()

        # If there is no expiry date specified, use 30 days
        if not_valid_after is None:
            not_valid_after = not_valid_before+datetime.timedelta(days=30)

        self._certificate = \
            cryptography.x509.CertificateBuilder().subject_name(descriptor.Subject)\
                .issuer_name(descriptor.Subject)\
                .public_key(self._private_key.Key.public_key())\
                .serial_number(descriptor.Serial)\
                .not_valid_before(not_valid_before)\
                .not_valid_after(not_valid_after)\
                .add_extension(cryptography.x509.SubjectAlternativeName([cryptography.x509.DNSName(descriptor.SAN)]), critical=False)\
            .sign(self._private_key.Key, hashes.SHA256())

        with open(certificate_path, 'wb') as file:
            file.write(self._certificate.public_bytes(Encoding.PEM))
