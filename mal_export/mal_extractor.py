import logging
import os
import sys
from datetime import datetime

import yaml

from mal_export.export_type import ExportType
from mal_export.request_handler import RequestHandler

logger = logging.getLogger(__name__)


class MALExtractor(object):
    def __init__(self):
        self._content = self._read_config()

    def get_anime_and_manga_xml_content(self):
        request_handler = RequestHandler(self._content['username'], self._content['password'])

        try:
            request_handler.login()

            anime_xml_content = request_handler.get_xml_content(ExportType.ANIME)
            mange_xml_content = request_handler.get_xml_content(ExportType.MANGA)
        finally:
            request_handler.logout()

        return anime_xml_content, mange_xml_content

    def save_xml(self, export_type, xml_content):
        save_path = self._content['save_path']

        if not os.path.isdir(save_path):
            raise ValueError(f'save_path "{save_path}" does not exist')

        username = self._content['username']

        file_name = f'{username}_{export_type.name.lower()}_{datetime.now().isoformat("_", "seconds")}.xml'
        file_path = os.path.join(save_path, file_name)

        logger.info(f'Saving {export_type.name} xml to "{file_path}"')

        with open(file_path, 'w+', errors='ignore') as file:
            file.write(xml_content.decode("utf-8"))

    @staticmethod
    def _get_config_path():
        if len(argv := sys.argv) >= 2:
            if os.path.isabs(argv[1]):
                return argv[1]
            else:
                return os.path.join(os.getcwd(), argv[1])
        else:
            return os.path.join(os.getcwd(), 'config.yaml')

    def _read_config(self):
        config_path = self._get_config_path()

        if not os.path.exists(config_path):
            raise ValueError(f'Config path \'{config_path}\' does not exist')

        logger.info(f'Reading {config_path}')

        with open(config_path, 'r') as stream:
            content = yaml.safe_load(stream)

            if "username" not in content or content['username'] is None:
                raise ValueError('username is empty in config.yaml')

            if "password" not in content or content['password'] is None:
                raise ValueError('password is empty in config.yaml')

            if "save_path" not in content or content['save_path'] is None:
                content['save_path'] = os.path.join(os.getcwd())
            else:
                if not os.path.exists(content['save_path']):
                    raise ValueError(f'Config path \'{content["save_path"]}\' does not exist')

            return content
