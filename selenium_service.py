import glob
import importlib
import json
import logging
import sys
import traceback
import yaml

from definitions import *
from feature import Feature
from runtime_reference import RuntimeReference
from utils import *


class SeleniumService:
    def __init__(self, env_path):
        self.logger = logging.getLogger(LOGGER_INSTANCE)
        self.logger.info("Starting SeleniumService Module")
        self.environment = self.load_environment_from_json(env_path)
        self.locale = self.load_locale()
        self.filenames = self.find_files()
        self.runtime = RuntimeReference()
        self.loaded_steps = {}
        self.features = []

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

    def find_files(self):
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

        if features is None:
            features = self.filenames['features']

        for feature_filename in features:
            self.features.append(Feature(feature_filename, self.loaded_steps, self.environment, self.locale))
