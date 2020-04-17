import logging
from utils import *
import re


class Feature:
    """
    Feature
    This class is responsible for processing a entire .feature file
    Each file should build an instance of this class

    Attributes:
        logger: logger instance gathered from logging module, acts like a singleton
        file_content: array of strings containing the file after pre-processing
    """

    def __init__(self, file_path, steps, factories, env_variables, locale, features_dict):
        """
        Class Feature constructor

        :param file_path: file path to feature file
        :param steps: dictionary with loaded_steps (read-only)
        :param factories: dictionary with loaded_factories (read-only)
        :param env_variables: dictionary with environment variables (read-only)
        :param locale: dictionary of the loaded locale (read-only)
        :param features_dict: dictionary with the traceback of the features (modified by reference)
        """
        self.logger = logging.getLogger(LOGGER_INSTANCE)
        self.file_content = pre_process_file(file_path)

        self.process_file(steps, factories, env_variables, locale, features_dict)

    def process_file(self, steps, factories, env_variables, locale, features_dict):
        """
        Iterates through each line of the file_content variable and takes the correct action

        :param steps: dictionary with loaded_steps (read-only)
        :param factories: dictionary with loaded_factories (read-only)
        :param env_variables: dictionary with environment variables (read-only)
        :param locale: dictionary of the loaded locale (read-only)
        :param features_dict: dictionary with the traceback of the features (modified by reference)
        :return: void
        """
        current_feature = ""
        current_scenario = ""
        current_skipped = ""

        for line in self.file_content:
            statement_match = re.match(RegularExpressions.regexps['statement'], line, re.IGNORECASE | re.MULTILINE)
            verb_match = re.match(RegularExpressions.regexps['verb'], line, re.IGNORECASE | re.MULTILINE)
            table_match = re.match(RegularExpressions.regexps['table'], line, re.IGNORECASE | re.MULTILINE)

            if statement_match:
                groups = statement_match.groups()
                indentation = len(groups[0])
                statement = groups[1]
                name = groups[2]

                try:
                    localized_statement = locale['statements'][statement.lower()]
                    if localized_statement == 'feature':
                        if check_indentation((indentation, env_variables['tab_size'], 0)):
                            self.logger.info("New feature %s detected. Processing..." % name)
                            current_feature = self.process_feature(name, features_dict)
                        else:
                            self.logger.error("Unexpected indent at statement:\n\t%s\n\u2191\u2191\u2191\u2191" % line)
                            return ErrorCodes.SYNTAX_ERROR

                    elif localized_statement == 'scenario':
                        if len(current_feature):
                            if check_indentation((indentation, env_variables['tab_size'], 1)):
                                self.logger.info("New scenario %s detected for feature %s" % (name, current_feature))
                                current_scenario = self.process_scenario(name, features_dict, current_feature)
                            else:
                                self.logger.error("Unexpected indent at statement:\n\t%s\n\u2191\u2191\u2191\u2191"
                                                  % line)
                                return ErrorCodes.SEMANTIC_ERROR
                        else:
                            self.logger.error("Scenario statement (%s) without a previous Feature" % line)

                    elif localized_statement == 'factory':
                        if len(current_scenario):
                            if check_indentation((indentation, env_variables['tab_size'], 2)):
                                self.logger.info('New reference to factory "%s" detected (below scenario %s)...'
                                                 ' Solving pending' % (name, current_scenario))
                                scenario_steps = features_dict[current_feature]['scenarios'][current_scenario]['steps']
                                factory_class_name = Feature.generate_factory_name(name)

                                try:
                                    factory_ref = Feature.get_factory_ref(factory_class_name, factories,
                                                                          current_feature)
                                    self.logger.info("Factory %s reference found." % name)
                                    scenario_steps.append({
                                        'name': name,
                                        'args': [],
                                        'status': ExecutionStatus.PENDING_EXECUTION,
                                        'ref': factory_ref,
                                        'details': None,
                                        'method_name': factory_class_name,
                                        'verb': 'factory'
                                    })

                                except (AttributeError, KeyError):
                                    self.logger.error("Could not solve reference to %s factory..." % name)
                                    scenario_steps.append({
                                        'name': name,
                                        'args': [],
                                        'status': ExecutionStatus.MISSING_REF,
                                        'ref': None,
                                        'details': None,
                                        'method_name': factory_class_name,
                                        'verb': 'factory'
                                    })
                            else:
                                self.logger.error("Unexpected indent at statement:\n\t%s\n\u2191\u2191\u2191\u2191"
                                                  % line)
                        else:
                            self.logger.error("Factory statement (%s) without a previous Scenario" % line)

                    else:
                        self.logger.critical(
                            'Unknown translation "%s" for statement %s' % (localized_statement, statement))
                        return ErrorCodes.UNKNOWN_TRANSLATION

                except KeyError:
                    self.logger.critical('Missing translation for "%s". Locale: %s', statement, env_variables['language'])
                    return ErrorCodes.MISSING_TRANSLATION

            elif verb_match:
                groups = verb_match.groups()
                indentation = len(groups[0])
                verb = groups[1].lower()
                step_name = groups[2]

                if Feature.is_verb(locale, verb):
                    verb = locale['verbs'][verb]
                    if check_indentation((indentation, env_variables['tab_size'], 2)):
                        scenario = features_dict[current_feature]['scenarios'][current_scenario]

                        if verb == 'do':
                            cmd = step_name.lower()
                            if cmd == 'skip':
                                self.logger.info("Skipping %s scenario (below feature: %s)"
                                                 % (current_scenario, current_feature))
                                current_skipped = current_scenario
                                scenario['status'] = ExecutionStatus.SKIPPED

                        if current_skipped != current_scenario:
                            step_attr = Feature.process_step_name(step_name)

                            try:
                                step_ref = self.get_step_ref(current_feature, steps, locale['verbs'][verb],
                                                             step_attr['method_name'])
                                step_attr['verb'] = verb
                                step_attr['ref'] = step_ref
                                step_attr['status'] = ExecutionStatus.PENDING_EXECUTION
                            except (AttributeError, KeyError):
                                self.logger.warning("Undefined step (below feature %s): %s"
                                                    % (current_feature, step_name))
                                step_attr['status'] = ExecutionStatus.MISSING_REF

                            finally:
                                scenario['steps'].append(step_attr)

                    else:
                        self.logger.error("Unexpected indent at verb:\n\t%s\n\u2191\u2191\u2191\u2191" % line)
                        return ErrorCodes.SYNTAX_ERROR

                else:
                    if check_indentation((indentation, env_variables['tab_size'], 1)):
                        self.update_feature_desc(verb, step_name, features_dict, current_feature)
                    else:
                        self.logger.error("Unexpected indent at description:\n\t%s\n\u2191\u2191\u2191\u2191" % line)
                        return ErrorCodes.SYNTAX_ERROR
            elif table_match:
                if current_skipped != current_scenario:
                    groups = table_match.groups()
                    indentation = len(groups[0])
                    key = groups[1]
                    value = groups[2]
                    if check_indentation((indentation, env_variables['tab_size'], 3)):
                        steps_arr = features_dict[current_feature]['scenarios'][current_scenario]['steps']
                        last_args_arr = steps_arr[len(steps_arr)-1]['args']
                        if len(last_args_arr):
                            last_args_arr[len(last_args_arr)-1][key] = value
                        else:
                            last_args_arr.append({key: value})
            else:
                self.logger.error("Syntax error at expression %s" % line)

    @staticmethod
    def is_verb(locale, candidate):
        """
        Tests (True or False) if the candidate word is a verb present in locale
        :param locale: locale dictionary
        :param candidate: string to be checked
        :return: True if is valid verb, False otherwise
        """
        if candidate in locale['verbs']:
            return True
        else:
            return False

    @staticmethod
    def update_feature_desc(verb, name, features_dict, parent_feature):
        """
        Updates features dictionary runtime with feature description
        :param verb: verb (second group)
        :param name: remaning line (third group)
        :param features_dict: dictionary with the traceback of the features (modified by reference)
        :param parent_feature: reference to the feature that we'll modify inside features_dict
        :return: void
        """
        if parent_feature in features_dict:
            line = verb.capitalize() + ' ' + name
            # First line
            if features_dict[parent_feature]['description'] is None:
                features_dict[parent_feature]['description'] = line
            # Other lines
            else:
                features_dict[parent_feature]['description'] += '\n' + line

    @staticmethod
    def get_step_ref(current_feature, steps, verb, step_name):
        """
        Search for a step definition inside feature_steps module
        If step is not found inside feature_steps, search inside common_steps
        If not found inside common_steps, raise AttributeError

        :param current_feature: name of feature
        :param steps: dictionary with loaded_steps (read-only)
        :param verb: verb of the step in .feature file
        :param step_name: name of the step in .feature file
        :raise AttributeError (Step undefined)
        :raise KeyError (Module not loaded)
        :return: staticmethod reference pointer
        """
        module_key = current_feature.lower() + '_steps'
        try:
            di_module = steps[module_key]
            verb_class = getattr(di_module, verb.capitalize())
            return staticmethod(getattr(verb_class, step_name))
        except (AttributeError, KeyError):
            di_module = steps['common_steps']
            verb_class = getattr(di_module, verb.capitalize())
            return staticmethod(getattr(verb_class, step_name))

    @staticmethod
    def get_factory_ref(factory_class_name, factories, parent_feature):
        """
        Search for a factory definition inside feature_factories module
        If factory is not found inside feature_factories, search inside common_factories
        If not found inside common_factories, raise AttributeError

        :param factory_class_name: name of the factory class (Python PEP 8 standardization)
        :param factories: dictionary with loaded_factories (read-only)
        :param parent_feature: current feature where the factory is being used
        :raise AttributeError (Step undefined)
        :raise KeyError (Module not loaded)
        :return: staticmethod reference pointer
        """
        module_key = parent_feature.lower() + '_factories'

        try:
            di_module = factories[module_key]
            factory_class = getattr(di_module, factory_class_name)
            run_method = getattr(factory_class, 'run')
            return staticmethod(run_method)
        except (AttributeError, KeyError):
            di_module = factories['common_factories']
            factory_class = getattr(di_module, factory_class_name)
            run_method = getattr(factory_class, 'run')
            return staticmethod(run_method)

    @staticmethod
    def process_step_name(step_name):
        """
        Text processing step_name to Python PEP 8 naming conventions which should be used to write steps
        :param step_name: step name written in .feature file
        :return: dictionary describing a 'empty' step
        """
        step_name = step_name.lstrip()
        step_name = step_name.rstrip()
        step_dict = {
            'name': step_name,
            'args': re.findall(RegularExpressions.regexps['step_args'], step_name),
            'status': ExecutionStatus.PENDING_SOLVING,
            'ref': None,
            'details': None
        }

        step_name = step_name.lower()
        step_name = re.sub(RegularExpressions.regexps['step_args'], '', step_name)
        step_dict['method_name'] = re.sub(RegularExpressions.regexps['spaces'], '_', step_name)
        return step_dict

    @staticmethod
    def generate_factory_name(factory_name):
        """
        Generates the PEP 8 name for factories
        :param factory_name: string with the factory_name from .feature
        :return: corrected string
        """

        split_names = re.split(r'\s+', factory_name)
        split_names = list(map(lambda x: x.capitalize(), split_names))
        return ''.join(split_names)

    def process_feature(self, name, features_dict):
        """
        Returns a dictionary describing an empty feature
        :param name: name of the feature (note that an file may contain multiple features)
        :param features_dict: dictionary with the traceback of the features (modified by reference)
        :return: param: name
        """
        if name not in features_dict:
            features_dict[name] = {'description': None, 'scenarios': {}, 'status': ExecutionStatus.PENDING}
        else:
            self.logger.warning("Feature %s is defined in more than once" % name)
        return name

    def process_scenario(self, name, features_dict, parent_feature):
        """
        Returns a dictionary describing an empty scenario

        :param name: name of the scenario in .feature file
        :param features_dict: dictionary with the traceback of the features (modified by reference)
        :param parent_feature: reference to the feature that we'll modify inside features_dict
        :return: param: name
        """
        if name not in features_dict[parent_feature]:
            features_dict[parent_feature]['scenarios'][name] = {'steps': [], 'status': ExecutionStatus.PENDING}
        else:
            self.logger.warning("Scenario %s was redeclared. Ignoring redeclaration..." % name)
        return name
