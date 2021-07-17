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
Contains the implementation of the GeoIP class.
"""

# Runtime Imports
import os
import tarfile
import shutil
import uuid

from urllib.error import ContentTooShortError, URLError

# Dependency Imports
import requests
import wget
import geoip2
import geoip2.database

# Path to the temporary location where the update package will be downloaded
PACKAGE_DOWNLOAD_LOCATION = '/tmp/'

class GeoIPData:

    """Represents the result of a single GeoIP search query.

    Attributes:
        _ip_address (str): The IP address whose data is stored.

        _continent (str): The continent where the IP address is located.

        _country (str): The country where the IP address is located.

        _city (str): The city where the IP address is located.

        _postal_code (str): The postal code of the city where the IP address is
            located.

        _latitude (float): The approximate latitude of the location where the
            IP address is located.

        _longitude (float): The approximate longitude of the location where the
            IP address is located.

    Authors:
        Attila Kovacs
    """

    @property
    def IPAddress(self) -> str:

        """The IP address whose data is stored.

        Authors:
            Attila Kovacs
        """

        return self._ip_address

    @property
    def Continent(self) -> str:

        """The continent where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._continent

    @property
    def Country(self) -> str:

        """The country where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._country

    @property
    def City(self) -> str:

        """The city where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._city

    @property
    def PostalCode(self) -> str:

        """The postal code of the city where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._postal_code

    @property
    def Latitude(self) -> str:

        """The approximate latitude of the location where the IP address is
        located.

        Authors:
            Attila Kovacs
        """

        return self._latitude

    @property
    def Longitude(self) -> str:

        """The approximate longitude of the location where the IP address is
        located.

        Authors:
            Attila Kovacs
        """

        return self._longitude

    def __init__(self,
                 ip_address: str,
                 continent: str = 'UNKNOWN',
                 country: str = 'UNKNOWN',
                 city: str = 'UNKNOWN',
                 postal_code: str = 'UNKNOWN',
                 latitude: str = 'UNKNOWN',
                 longitude: str = 'UNKNOWN') -> None:

        """Creates a new GeoIPData instance.

        Args:
            ip_address (str): The IP address whose data is stored.

            continent (str): The continent where the IP address is located.

            country (str): The country where the IP address is located.

            city (str): The city where the IP address is located.

            postal_code (str): The postal code of the city where the IP address
                is located.

            latitude (str): The approximate latitude of the location where the
                IP address is located.

            longitude (str): The approximate longitude of the location where
                the IP address is located.

        Authors:
            Attila Kovacs
        """

        self._ip_address = ip_address
        self._continent = continent
        self._country = country
        self._city = city
        self._postal_code = postal_code
        self._latitude = latitude
        self._longitude = longitude

class GeoIP:

    """Utility class to execute GeoIP queries and database updates.

    Attributes:
        _update_link (str): The update link from where the GeoIP database can
            be downloaded.

        _database_path (str): Path to the directory where the GeoIP database
            will be stored.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 update_link: str = None,
                 database_path: str = None) -> None:

        """Creates a new GeoIP instance.

        Args:
            update_link (str): The URL from which the GeoIP database can be
                downloaded.

            database_path (str): Path to the directory where the GeoIP database
                should be stored.
        """

        # The update link from where the GeoIP database can be downloaded.
        self._update_link = update_link

        # Path to the directory where the GeoIP database will be stored.
        self._database_path = os.path.abspath(
            os.path.expanduser(database_path))

        # Try to retrieve the database if it doesn't exist.
        if not os.path.isfile(f'{self._database_path}/GeoLite2-City.mmdb'):
            self.update_database()

    def update_database(self) -> None:

        """Updates the GeoIP database.

        Authors:
            Attila Kovacs
        """

        if not self._update_link:
            return

        # Use a random generated UUID as a temporary filename for the
        # downloaded GeoIP database to avoid it being used as a potential
        # attack vector by forcing the application to open a file with
        # malicious content if the downloaded file has been compromised.
        package_temp_name = str(uuid.uuid4())
        package_filename = f'{PACKAGE_DOWNLOAD_LOCATION}/{package_temp_name}.tar.gz'

        # Download the update package
        try:
            wget.download(url=self._update_link,
                          out=package_filename)
        except requests.exceptions.ConnectionError:
            # Failed to connect to the backend to download the database
            return
        except ContentTooShortError:
            # Failed to download the whole package.
            return
        except URLError:
            # Failed to connect to the backend to download the database
            return

        # Extract the update package
        with tarfile.open(package_filename) as tar:
            tar.extractall(path=PACKAGE_DOWNLOAD_LOCATION,
                           members=GeoIP._find_mmdb(tar))

        # Move the database to the requested location
        shutil.move(src=f'{PACKAGE_DOWNLOAD_LOCATION}/GeoLite2-City.mmdb',
                    dst=f'{self._database_path}/GeoLite2-City.mmdb')

        # Delete the update package
        os.remove(package_filename)

    def query(self, ip_address: str) -> GeoIPData:

        """Queries the data of the given IP address.

        Args:
            ip_address (str): The IP address to look up in the database.

        Returns:
            GeoIPData: A GeoIPData object containing the information about the
                IP address, or 'None', if the IP address was not found in the
                database.

        Authors:
            Attila Kovacs
        """

        result = None

        if os.path.isfile(f'{self._database_path}/GeoLite2-City.mmdb'):
            try:
                reader = geoip2.database.Reader(
                    f'{self._database_path}/GeoLite2-City.mmdb')
                response = reader.city(ip_address)
                result = GeoIPData(
                    ip_address=ip_address,
                    continent=response.continent.name,
                    country=response.country.name,
                    city=response.city.name,
                    postal_code=response.postal.code,
                    latitude=response.location.latitude,
                    longitude=response.location.longitude)
            except geoip2.errors.AddressNotFoundError:
                # Raised when the IP address is not found in the database
                result = GeoIPData(ip_address=ip_address)
            except ValueError:
                # Raised when trying to query an invalid IP address
                result = GeoIPData(ip_address=ip_address)

        return result

    @staticmethod
    def _find_mmdb(members: list) -> object:

        """Finds the GeoIP database inside the downloaded package.

        Args:
            members (list): List of files in the update package.

        Returns:
            object: The database file inside the update package.

        Authors:
            Attila Kovacs
        """

        for member in members:
            if os.path.splitext(member.name)[1] == '.mmdb':
                member.name = os.path.basename(member.name)
                yield member
