"""BDD-Selenium - selenium_service.py
This file defines the principal service definition of application,
which contains all the environment variables, localization, dependency tree and so on...
"""

import glob
import importlib
import json
import logging
import sys
import traceback
import yaml

from feature import Feature
from utils import *


class SeleniumService:
    """
    Selenium Service
    This class is responsible for loading the environment and performs the testing in a abstract way
    by calling methods on other modules

    Attributes:
        logger: logger instance gathered from logging module, acts like a singleton
        environment: dictionary containing the data from environment.json
        locale: dictionary containing the translations for the language set in environment
        filenames: dictionary containing the filenames of the files found into the folders provided in environment
        runtime: dictionary mapping each entity into it's dependencies and status
        loaded_steps: dictionary mapping each step file found (using filename) into the actual imported modules
        loaded_factories: dictionary mapping each factory file found (using filename) into the actual imported modules
    """

    def __init__(self, env_path):
        self.logger = logging.getLogger(LOGGER_INSTANCE)
        self.logger.info("Starting SeleniumService Module")
        self.environment = self.load_environment_from_json(env_path)
        self.locale = self.load_locale()
        self.filenames = self.find_files()
        self.runtime = {}
        self.loaded_steps = {}
        self.loaded_factories = {}

    def load_environment_from_json(self, env_path):
        """Loads the content from environment.json

        :param env_path: file path to environment.json
        :return: JSON content, if exists, otherwise exit process with MISSING_ENVIRONMENT code
        """
        try:
            with open(env_path, 'r', encoding='utf8') as fp:
                return json.load(fp)
        except FileNotFoundError:
            self.logger.error("Could not found environment JSON at: {path}. Check the address and try again."
                              .format(path=env_path))
            exit(ErrorCodes.MISSING_ENVIRONMENT)

    def load_locale(self):
        """Loads the content of the locale specified on environment.json

        :return: yml file content, if exists, otherwise
            exit process with MISSING_PROPERTY (if language attribute is not present in environment.json)
            exit process with MISSING_LOCALE (if .yml does not exists under the folder locales/)
        """
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

    def find_files(self):
        """Performs iglob search below the paths provided by the user in environment.json

        :return: dictionary mapping each category into a array of filenames
        """
        self.logger.info("Scanning directories for testing files...")
        features_iglob_generator = glob.iglob('{path}/**/*.feature'
                                              .format(path=self.environment['paths']['features_path']), recursive=True)
        steps_iglob_generator = glob.iglob('{path}/**/*_steps.py'.format(path=self.environment['paths']['steps_path']),
                                           recursive=True)
        factories_iglob_generator = glob.iglob('{path}/**/*_factories.py'
                                               .format(path=self.environment['paths']['factories_path']),
                                               recursive=True)

        features_files = list(features_iglob_generator)
        steps_files = list(steps_iglob_generator)
        factories_files = list(factories_iglob_generator)

        self.logger.info("Scan complete.\nFiles detected:\n\t%d features\n\t%d steps\n\t%d factories"
                         % (len(features_files), len(steps_files), len(factories_files)))
        return {
            'features': features_files,
            'steps': steps_files,
            'factories': factories_files
        }

    def run(self, features=None):
        """Opens all the detected files and handles the execution by calling other modules

        :param features: array of strings specifying which features should run
        :default features: None (executes everything)
        :return: void
        """
        # Loading all steps
        self.logger.info("Loading step definitions...")
        sys.path.append(self.environment['paths']['steps_path'])

        for step in self.filenames['steps']:
            module_name = extract_module_name(step)
            self.logger.info("Loading module %s ..." % module_name)
            try:
                self.loaded_steps.setdefault(module_name, importlib.import_module(module_name, package=False))
                self.logger.info("Module %s loaded successfully" % module_name)
            except SyntaxError:
                self.logger.warning("Module %s contains errors. Ignoring...\nMore details:\n %s"
                                    % (module_name, traceback.format_exc()))
        self.logger.info("%d step modules loaded" % (len(self.loaded_steps)))

        # Loading all factories
        self.logger.info("Loading factories definitions...")
        sys.path.append(self.environment['paths']['factories_path'])

        for factory in self.filenames['factories']:
            module_name = extract_module_name(factory)
            self.logger.info("Loading module %s ..." % module_name)
            try:
                self.loaded_factories.setdefault(module_name, importlib.import_module(module_name, package=False))
                self.logger.info("Module %s loaded successfully" % module_name)
            except SyntaxError:
                self.logger.warning("Module %s contains errors. Ignoring...\nMore details:\n %s"
                                    % (module_name, traceback.format_exc()))
        self.logger.info("%d factories modules loaded" % (len(self.loaded_factories)))
        self.logger.info("Modules loaded")
        self.logger.info("Mounting dependencies...")

        # Mounting dependencies
        for feature_filename in self.filenames['features']:
            Feature(feature_filename, self.loaded_steps, self.environment, self.locale, self.runtime)

        self.logger.info("Dependency tree complete... Will init execution\n\n")
        self.logger.info("Execution started. Requested features: {features}"
                         .format(features='All' if features is None else ', '.join(features)))
