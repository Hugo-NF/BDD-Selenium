"""BDD-Selenium - execution_service.py
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
import pickle

from datetime import datetime
from feature import Feature
from selenium_runtime import selenium_runtime
from utils import *


class ExecutionService:
    """
    Execution Service
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
            selenium_runtime.browser.quit()
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
            selenium_runtime.browser.quit()
            exit(ErrorCodes.MISSING_PROPERTY)
        except FileNotFoundError:
            self.logger.error("Could not found locale file: {locale_path}. Check the address and try again."
                              .format(locale_path=locale_path))
            selenium_runtime.browser.quit()
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

    def display_results(self, selected_features):
        """Pretty printer of the results, dumps to JSON if requested in environment"""
        self.logger.info("Testing session completed. Displaying results:")
        self.logger.info(self.runtime)

        display_names = {
            ExecutionStatus.PASSED: 'PASSED',
            ExecutionStatus.SKIPPED: 'SKIPPED'
        }
        features = {
            'total': 0,
            'passed': 0,
            'failed': 0
        }
        scenarios = {
            'total': 0,
            'passed': 0,
            'skipped': 0,
            'failed': 0
        }
        steps = {
            'total': 0,
            'passed': 0,
            'skipped': 0,
            'failed': 0
        }

        ran_features = dict(filter(lambda item: item[0] in selected_features, self.runtime.items()))
        for feature_name, feature_value in ran_features.items():
            features['total'] += 1
            if feature_value['status'] == ExecutionStatus.PASSED:
                features['passed'] += 1
                print("[{status}][{elapsed} ms] - Feature {name}\n\t{description}".format(
                    status=display_names.get(feature_value['status'], 'FAILED'),
                    elapsed=round(feature_value['exec_time'], 2),
                    name=feature_name,
                    description=description_display(feature_value['description'])))
            else:
                features['failed'] += 1
                print("[{status}] - Feature {name}\n\t{description}".format(
                    status=display_names.get(feature_value['status'], 'FAILED'),
                    name=feature_name,
                    description=description_display(feature_value['description'])))

            print("\tScenarios:")
            for scenario_name, scenario_value in feature_value['scenarios'].items():
                scenarios['total'] += 1
                if scenario_value['status'] == ExecutionStatus.PASSED:
                    scenarios['passed'] += 1
                    print("\t[{status}][{elapsed} ms] - Scenario: {name}".format(
                        status=display_names.get(scenario_value['status'], 'FAILED'),
                        elapsed=round(scenario_value['exec_time'], 2),
                        name=scenario_name
                    ))
                elif scenario_value['status'] == ExecutionStatus.SKIPPED:
                    scenarios['skipped'] += 1
                    print("\t[{status}] - Scenario: {name}".format(
                        status=display_names.get(scenario_value['status'], 'FAILED'),
                        name=scenario_name
                    ))
                else:
                    scenarios['failed'] += 1
                    print("\t[{status}] - Scenario: {name}".format(
                        status=display_names.get(scenario_value['status'], 'FAILED'),
                        name=scenario_name
                    ))
                    print("\t\tSteps:")
                    for step in scenario_value['steps']:
                        steps['total'] += 1
                        if step['status'] == ExecutionStatus.PASSED:
                            steps['passed'] += 1
                            print("\t\t[{status}][{elapsed} ms] - {name}".format(
                                status=display_names.get(step['status'], 'FAILED'),
                                elapsed=round(step['details'], 2),
                                name=' '.join([step['verb'], step['name']])
                            ))
                        elif step['status'] == ExecutionStatus.SKIPPED:
                            steps['skipped'] += 1
                            print("\t\t[{status}] - {name}".format(
                                status=display_names.get(step['status'], 'FAILED'),
                                name=' '.join([step['verb'], step['name']])
                            ))
                        else:
                            steps['failed'] += 1
                            print("\t\t[{status}] - {name}. Exception details:\n{exception}".format(
                                status=display_names.get(step['status'], 'FAILED'),
                                name=' '.join([step['verb'], step['name']]),
                                exception=step['details'] if step['details'] is not None else step['status']
                            ))
        print("\nResults summary:")
        print("Features:\n%d detected\n\t%d passed\n\t%d failed"
              % (features['total'], features['passed'], features['failed']))

        print("Scenarios:\n%d detected\n\t%d passed\n\t%d skipped\n\t%d failed"
              % (scenarios['total'], scenarios['passed'], scenarios['skipped'], scenarios['failed']))

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
            self.logger.info("Loading module %s..." % module_name)
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
            Feature(feature_filename, self.loaded_steps, self.loaded_factories,
                    self.environment, self.locale, self.runtime)

        self.logger.info("Dependency tree complete... Will init execution\n\n")
        self.logger.info("Execution started. Requested features: {features}"
                         .format(features='All' if features is None else ', '.join(features)))

        # Actually executing the tests
        features = self.runtime.keys() if features is None else features
        for feature in features:
            if feature in self.runtime:
                feature_obj = self.runtime[feature]
                feature_obj['status'] = ExecutionStatus.RUNNING
                for scenario in feature_obj['scenarios'].keys():
                    scenario_obj = self.runtime[feature]['scenarios'][scenario]
                    if scenario_obj['status'] != ExecutionStatus.SKIPPED:
                        scenario_obj['status'] = ExecutionStatus.RUNNING
                        for step in scenario_obj['steps']:
                            if step['status'] == ExecutionStatus.PENDING_EXECUTION:
                                step['status'] = ExecutionStatus.RUNNING
                                step_method = step['ref']
                                step_args = step['args']
                                try:
                                    step_start = datetime.now()
                                    step_method(*step_args)
                                    step['status'] = ExecutionStatus.PASSED
                                    step['details'] = (datetime.now() - step_start).microseconds / 1e3
                                    scenario_obj['exec_time'] += step['details']
                                except:
                                    step['status'] = ExecutionStatus.FAILED
                                    scenario_obj['status'] = ExecutionStatus.FAILED
                                    feature_obj['status'] = ExecutionStatus.FAILED
                                    step['details'] = traceback.format_exc()
                            else:
                                scenario_obj['status'] = step['status']
                                feature_obj['status'] = step['status']
                        if scenario_obj['status'] == ExecutionStatus.RUNNING:
                            scenario_obj['status'] = ExecutionStatus.PASSED
                            feature_obj['exec_time'] += scenario_obj['exec_time']
                    else:
                        feature_obj['status'] = ExecutionStatus.SKIPPED
                if feature_obj['status'] == ExecutionStatus.RUNNING:
                    feature_obj['status'] = ExecutionStatus.PASSED

            else:
                self.logger.error('Requested feature "%s" was not present on test files' % feature)
        self.display_results(features)
