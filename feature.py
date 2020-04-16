import logging
from definitions import *
from utils import *
import re


class Feature:

    def __init__(self, file_path, steps, env_variables, locale, features_dict):
        self.logger = logging.getLogger(LOGGER_INSTANCE)
        self.file_content = pre_process_file(file_path)

        self.process_file(steps, env_variables, locale, features_dict)

    def process_file(self, steps, env_variables, locale, features_dict):
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
                            current_feature = self.process_feature(name, features_dict)
                        else:
                            self.logger.error("Unexpected indent at statement:\n\t%s\n\u2191\u2191\u2191\u2191" % line)
                            return ErrorCodes.SYNTAX_ERROR

                    elif localized_statement == 'scenario':
                        if len(current_feature):
                            if check_indentation((indentation, env_variables['tab_size'], 1)):
                                current_scenario = self.process_scenario(name, features_dict, current_feature)
                            else:
                                self.logger.error("Unexpected indent at statement:\n\t%s\n\u2191\u2191\u2191\u2191"
                                                  % line)
                                return ErrorCodes.SYNTAX_ERROR
                        else:
                            self.logger.error("Scenario statement (%s) without a previous Feature" % line)

                    elif localized_statement == 'factory':
                        self.logger.warning('Factories are not implemented yet')

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
                print(verb, step_name)
                if Feature.is_verb(locale, verb):
                    verb = locale['verbs'][verb]
                    if check_indentation((indentation, env_variables['tab_size'], 2)):
                        scenario = features_dict[current_feature]['scenarios'][current_scenario]

                        if verb == 'do':
                            cmd = step_name.lower()
                            if cmd == 'skip':
                                print("%s scenario skipped", current_scenario)
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
                                self.logger.warning("Undefined step (below feature %s): %s" % (current_feature, step_name))
                                step_attr['status'] = ExecutionStatus.MISSING_STEP

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
        if candidate in locale['verbs']:
            return True
        else:
            return False

    @staticmethod
    def update_feature_desc(verb, name, features_dict, parent_feature):
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
        module_key = current_feature.lower() + '_steps'

        di_module = steps[module_key]
        verb_class = getattr(di_module, verb.capitalize())
        return getattr(verb_class, step_name)

    @staticmethod
    def process_step_name(step_name):
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

    def process_feature(self, name, features_dict):
        if name not in features_dict:
            features_dict[name] = {'description': None, 'scenarios': {}, 'status': ExecutionStatus.PENDING}
        else:
            self.logger.warning("Feature %s is defined in more than once" % name)
        return name

    def process_scenario(self, name, features_dict, parent_feature):
        if name not in features_dict[parent_feature]:
            features_dict[parent_feature]['scenarios'][name] = {'steps': [], 'status': ExecutionStatus.PENDING}
        else:
            self.logger.error("Scenario %s was redeclared. Ignoring redeclaration..." % name)
        return name
