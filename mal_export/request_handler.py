import gzip
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PAGE_URL = 'https://myanimelist.net/'

logger = logging.getLogger(__name__)

MAL_ERROR_MESSAGES = [
    'Your username or password is incorrect.'
]


class RequestHandler(object):
    def __init__(self, username, password):
        self._session = requests.session()
        self._username = username
        self._password = password

    def login(self):
        logger.info(f'Logging in to MAL with user "{self._username}"')

        url = urljoin(PAGE_URL, 'login.php')

        data = {'user_name': self._username, 'password': self._password, 'csrf_token': self._get_csrf_token(url)}
        response = self._session.post(url, data=data)
        self._check_response(response)

    def _get_csrf_token(self, url):
        response = self._session.get(PAGE_URL)
        self._check_response(response)

        soup = BeautifulSoup(response.content, 'html.parser')

        csrf_token = soup.find('meta', attrs={'name': 'csrf_token'}).attrs['content']

        if csrf_token:
            return csrf_token
        else:
            raise ValueError('No csrf token found')

    def logout(self):
        logger.info('Logging out of MAL')

        url = urljoin(PAGE_URL, 'logout.php')

        response = self._session.post(url, data={'csrf_token': self._get_csrf_token(url)})
        self._check_response(response)

    def get_xml_content(self, export_type):
        url = self._get_xml_download_url_by_type(export_type)
        return self._download_xml_and_decompress(export_type, url)

    def _download_xml_and_decompress(self, export_type, url):
        logger.info(f'Downloading {export_type.name} xml')

        response = self._session.get(url)
        self._check_response(response)

        return gzip.decompress(response.content)

    def _get_xml_download_url_by_type(self, export_type):
        logger.info(f'Getting {export_type.name} xml download url')

        url = urljoin(PAGE_URL, '/panel.php?go=export')

        data = {'type': export_type.value, 'subexport': 'Export+My+List', 'csrf_token': self._get_csrf_token(url)}
        response = self._session.post(url, data=data)
        self._check_response(response)

        soup = BeautifulSoup(response.content, 'html.parser')

        url_path_query = soup.find('div', class_='goodresult') \
            .find('a').attrs['href']

        return urljoin(PAGE_URL, url_path_query)

    def _check_response(self, response):
        self._check_response_status_code(response)
        self._check_response_content(response)

    @staticmethod
    def _check_response_content(response):
        content = str(response.content)
        for error_message in MAL_ERROR_MESSAGES:
            if error_message in content:
                raise ValueError(f'MAL returned error message "{error_message}"')

    @staticmethod
    def _check_response_status_code(response):
        if not response.ok:
            raise ValueError(f'MAL returned status code "{response.status_code}" with reason "{response.reason}"')
