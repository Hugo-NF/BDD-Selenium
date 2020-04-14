import logging
from definitions import *
from utils import *
import json
import yaml


class SeleniumService:
    def __init__(self, env_path):
        self.logger = logging.getLogger(LOGGER_INSTANCE)
        self.logger.info("Starting SeleniumService Module")
        self.environment = self.load_environment_from_json(env_path)
        self.locale = self.load_locale()

    def load_environment_from_json(self, env_path):
        try:
            with open(env_path, 'r', encoding='utf8') as fp:
                return json.load(fp)
        except FileNotFoundError:
            self.logger.error("Could not found environment JSON at: {path}. Check the address and try again."
                              .format(path=env_path))
            exit(ErrorCodes.MISSING_ENVIRONMENT)

    def load_locale(self):
        try:
            selected_locale = self.environment['language']
            locale_path = LOCALES_ROOT + correct_file_extension(selected_locale, '.yml')
            with open(locale_path, 'r', encoding='utf8') as fp:
                return yaml.safe_load(fp)

        except KeyError:
            self.logger.error("Variable language not found in environment.json")
            exit(ErrorCodes.MISSING_PROPERTY)
        except FileNotFoundError:
            self.logger.error("Could not found locale file: {locale_path}. Check the address and try again."
                              .format(locale_path=locale_path))
            exit(ErrorCodes.MISSING_LOCALE)
