import logging
from definitions import *


class Summary:

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_INSTANCE)
        self.stats = {'features': {}}

    def add_feature_or_default(self, name, description):
        self.stats['features'].setdefault(name, {'desc': description, 'passed': True, 'scenarios': {}})
        return ErrorCodes.OK

    def add_scenario_or_default(self, name, parent_feature):
        try:
            feature = self.stats['features'][parent_feature]
            feature.setdefault(name, {
                'passed': True,
                'steps': {}
            })
            return ErrorCodes.OK
        except KeyError:
            self.logger.error("Unspecified feature: %s" % parent_feature)
            return ErrorCodes.UNSPECIFIED_PARENT

    def add_step_or_default(self, index, definition, step_ref, parent_feature, parent_scenario):
        try:
            scenario = self.stats['features'][parent_feature][parent_scenario]
            scenario.setdefault(index, {
                                    'def': definition,
                                    'passed': True,
                                    'error_code': 0,
                                    'error_desc': '',
                                    'step_ref': step_ref
                                })
            return ErrorCodes.OK
        except KeyError:
            self.logger.error("Unspecified scenario: %s" % parent_scenario)
            return ErrorCodes.UNSPECIFIED_PARENT
