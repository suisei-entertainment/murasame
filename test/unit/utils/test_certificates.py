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
Contains the unit tests for certificate handling.
"""

# Runtime Imports
import datetime
import os
import sys
import uuid
import subprocess
from typing import Any

# Dependency Imports
import pytest
import cryptography.x509

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils.certificates import X509GenericCertificateFields, X509Certificate
from murasame.utils.rsa import RSAPrivate, RSAKeyGenerator

CERT_BASE_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles'))

class TestX509GenericCertificateFields:

    """Contains the unit tests for the X509GenericCertificateFields class.

    Authors:
        Attila Kovacs
    """

    def test_creation_of_empty_object(self):

        """Tests that an X509GenericCertificateFields object can be created empty.

        Authors:
            Attila Kovacs
        """

        sut = X509GenericCertificateFields()

        assert sut.CommonName is None
        assert sut.Country is None
        assert sut.State is None
        assert sut.Locality is None
        assert sut.Address is None
        assert sut.Organization is None
        assert sut.OrganizationalUnit is None
        assert sut.Serial is None
        assert sut.Surname is None
        assert sut.GivenName is None
        assert sut.Title is None
        assert sut.Email is None
        assert sut.SAN is None

    def test_creation_with_data(self):

        """Tests that an X509GenericCertificateFields object can be created
        with data.

        Authors:
            Attila Kovacs
        """

        testserial = uuid.uuid4()
        sut = X509GenericCertificateFields(
            common_name='testcommonname',
            country='testcountry',
            state='teststate',
            locality='testlocality',
            address='testaddress',
            organization='testorganization',
            org_unit='testorgunit',
            serial=1,
            surname='testsurname',
            given_name='testgivenname',
            title='testtitle',
            email='testemail',
            san='testsan')

        assert sut.CommonName == 'testcommonname'
        assert sut.Country == 'testcountry'
        assert sut.State == 'teststate'
        assert sut.Locality == 'testlocality'
        assert sut.Address == 'testaddress'
        assert sut.Organization == 'testorganization'
        assert sut.OrganizationalUnit  == 'testorgunit'
        assert sut.Serial == 1
        assert sut.Surname == 'testsurname'
        assert sut.GivenName  == 'testgivenname'
        assert sut.Title == 'testtitle'
        assert sut.Email == 'testemail'
        assert sut.SAN == 'testsan'

    def test_name_generation(self):

        """Tests that an X.509 name object can be generated correctly.

        Authors:
            Attila Kovacs
        """

        testserial = uuid.uuid4()
        sut = X509GenericCertificateFields(
            common_name='testcommonname',
            country='us',
            state='teststate',
            locality='testlocality',
            address='testaddress',
            organization='testorganization',
            org_unit='testorgunit',
            serial=1,
            surname='testsurname',
            given_name='testgivenname',
            title='testtitle',
            email='testemail')

        name = sut.Subject

        assert isinstance(name, cryptography.x509.Name)
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.COMMON_NAME)[0].value == 'testcommonname'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.COUNTRY_NAME)[0].value == 'us'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.STATE_OR_PROVINCE_NAME)[0].value == 'teststate'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.LOCALITY_NAME)[0].value == 'testlocality'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.STREET_ADDRESS)[0].value == 'testaddress'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.ORGANIZATION_NAME)[0].value == 'testorganization'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value == 'testorgunit'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.SERIAL_NUMBER)[0].value == str(1)
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.SURNAME)[0].value == 'testsurname'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.GIVEN_NAME)[0].value == 'testgivenname'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.TITLE)[0].value == 'testtitle'
        assert name.get_attributes_for_oid(
            cryptography.x509.NameOID.EMAIL_ADDRESS)[0].value == 'testemail'

class TestX509Certificate:

    """Contains the unit tests for the X509Certificate class.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls):

        command = f'openssl req -x509 -newkey rsa:4096 -nodes -sha256 -keyout {CERT_BASE_PATH}/key.pem -out {CERT_BASE_PATH}/cert.pem -days 365 -subj "/C=US/ST=Oregon/L=Portland/O=Company Name/OU=Org/CN=www.example.com"'

        try:
            FNULL = open(os.devnull, 'w')
            subprocess.run(command, shell=True, stdout=FNULL, check=True)
        except subprocess.CalledProcessError:
            assert False

        with open(f'{CERT_BASE_PATH}/invalid_cert.pem', 'w') as file:
            file.write('invalid')

        with open(f'{CERT_BASE_PATH}/invalid_key.pem', 'w') as file:
            file.write('invalid')

        generator = RSAKeyGenerator()
        generator.save_key_pair(
            private_key_path=f'{CERT_BASE_PATH}/cert_signing_key.pem',
            public_key_path=f'{CERT_BASE_PATH}/cert_signing_key_public.pem')

    @classmethod
    def teardown_class(cls):

        if os.path.isfile(f'{CERT_BASE_PATH}/key.pem'):
            os.remove(f'{CERT_BASE_PATH}/key.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/cert.pem'):
            os.remove(f'{CERT_BASE_PATH}/cert.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/key2.pem'):
            os.remove(f'{CERT_BASE_PATH}/key2.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/cert2.pem'):
            os.remove(f'{CERT_BASE_PATH}/cert2.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/invalid_cert.pem'):
            os.remove(f'{CERT_BASE_PATH}/invalid_cert.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/invalid_key.pem'):
            os.remove(f'{CERT_BASE_PATH}/invalid_key.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/generated.pem'):
            os.remove(f'{CERT_BASE_PATH}/generated.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/cert_signing_key.pem'):
            os.remove(f'{CERT_BASE_PATH}/cert_signing_key.pem')

        if os.path.isfile(f'{CERT_BASE_PATH}/cert_signing_key_public.pem'):
            os.remove(f'{CERT_BASE_PATH}/cert_signing_key_public.pem')

    def test_creation(self):

        """Tests that a certificate object can be created.

        Authors:
            Attila Kovacs
        """

        sut = X509Certificate()

        assert sut.Version is None
        assert sut.Fingerprint is None
        assert sut.SerialNumber is None
        assert sut.PublicKey is None
        assert sut.NotValidBefore is None
        assert sut.NotValidAfter is None
        assert not sut.IsValid
        assert sut.CommonName is None
        assert sut.Issuer is None
        assert sut.Signature is None
        assert sut.SignatureHashAlgorithm is None
        assert sut.SignatureAlgorithmOID is None
        assert sut.Extensions is None
        assert sut.CertificateBytes is None

    def test_loading_valid_certificate(self):

        """Tests that a valid certificate can be loaded from disk.

        Authors:
            Attila Kovacs
        """

        sut = X509Certificate(
            certificate_path=f'{CERT_BASE_PATH}/cert.pem',
            private_key_path=f'{CERT_BASE_PATH}/key.pem')

        assert sut.Version == cryptography.x509.Version.v3
        assert sut.Fingerprint is not None
        assert sut.SerialNumber is not None
        assert sut.PublicKey is not None
        assert sut.NotValidBefore is not None
        assert sut.NotValidAfter is not None
        assert sut.IsValid
        assert sut.CommonName == 'www.example.com'
        assert sut.Issuer == 'www.example.com'
        assert sut.Signature is not None
        assert sut.SignatureHashAlgorithm.name == 'sha256'
        assert sut.SignatureAlgorithmOID is not None
        assert sut.Extensions is not None
        assert sut.CertificateBytes is not None

    def test_loading_invalid_certificate(self):

        """Tests that loading an invalid certificate is handled correctly.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = X509Certificate(
            certificate_path=f'{CERT_BASE_PATH}/invalid_cert.pem',
            private_key_path=f'{CERT_BASE_PATH}/invalid_key.pem')

    def test_loading_non_existent_certificate(self):

        """Tests that a valid certificate can be loaded from disk.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = X509Certificate(
            certificate_path='/path/to/nonexistent/cert',
            private_key_path='/path/to/nonexistent/key')

    def test_certificate_saving(self):

        """Tests that certificates can be saved to disk.

        Authors:
            Attila Kovacs
        """

        sut = X509Certificate(
            certificate_path=f'{CERT_BASE_PATH}/cert.pem',
            private_key_path=f'{CERT_BASE_PATH}/key.pem')

        sut.save(
            certificate_path=f'{CERT_BASE_PATH}/cert2.pem',
            private_key_path=f'{CERT_BASE_PATH}/key2.pem')

        sut2 = X509Certificate(
            certificate_path=f'{CERT_BASE_PATH}/cert2.pem',
            private_key_path=f'{CERT_BASE_PATH}/key2.pem')

        assert sut.Version == sut2.Version
        assert sut.Fingerprint == sut2.Fingerprint
        assert sut.SerialNumber == sut2.SerialNumber
        assert sut.PublicKey == sut2.PublicKey
        assert sut.NotValidBefore == sut2.NotValidBefore
        assert sut.NotValidAfter == sut2.NotValidAfter
        assert sut.IsValid == sut2.IsValid
        assert sut.CommonName == sut2.CommonName
        assert sut.Issuer == sut2.Issuer
        assert sut.Signature == sut2.Signature
        assert sut.SignatureHashAlgorithm.name == sut2.SignatureHashAlgorithm.name
        assert sut.SignatureAlgorithmOID == sut2.SignatureAlgorithmOID
        assert sut.Extensions == sut.Extensions
        assert sut.CertificateBytes == sut.CertificateBytes

    def test_certificate_generation_with_default_parameters(self):

        """Tests that a new certificate can be generated with default
        parameters.

        Authors:
            Attila Kovacs
        """

        key = RSAPrivate(key_path=f'{CERT_BASE_PATH}/cert_signing_key.pem')

        sut = X509Certificate()

        testserial = uuid.uuid4()
        descriptor = X509GenericCertificateFields(
            common_name='testcommonname',
            country='US',
            state='teststate',
            locality='testlocality',
            address='testaddress',
            organization='testorganization',
            org_unit='testorgunit',
            serial=1,
            surname='testsurname',
            given_name='testgivenname',
            title='testtitle',
            email='testemail',
            san='testsan')

        sut.generate(certificate_path=f'{CERT_BASE_PATH}/generated.pem',
                     private_key=key,
                     descriptor=descriptor)

        cert = X509Certificate(
            certificate_path=f'{CERT_BASE_PATH}/generated.pem',
            private_key_path=f'{CERT_BASE_PATH}/cert_signing_key.pem')

        assert cert is not None
        assert cert.IsValid

    def test_certificate_generation_with_custom_validity(self):

        """Tests that a new certificate can be generated with custom validity
        parameters.

        Authors:
            Attila Kovacs
        """

        key = RSAPrivate(key_path=f'{CERT_BASE_PATH}/cert_signing_key.pem')

        sut = X509Certificate()

        testserial = uuid.uuid4()
        descriptor = X509GenericCertificateFields(
            common_name='testcommonname',
            country='US',
            state='teststate',
            locality='testlocality',
            address='testaddress',
            organization='testorganization',
            org_unit='testorgunit',
            serial=1,
            surname='testsurname',
            given_name='testgivenname',
            title='testtitle',
            email='testemail',
            san='testsan')

        start_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=10)

        sut.generate(certificate_path=f'{CERT_BASE_PATH}/generated.pem',
                     private_key=key,
                     descriptor=descriptor,
                     not_valid_before=start_date,
                     not_valid_after=end_date)

        cert = X509Certificate(
            certificate_path=f'{CERT_BASE_PATH}/generated.pem',
            private_key_path=f'{CERT_BASE_PATH}/cert_signing_key.pem')

        assert cert is not None
        assert not cert.IsValid