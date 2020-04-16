from enum import Enum

# Macro definitions
VERSION = '0.0.2beta'

LOGGER_INSTANCE = "SeleniumBDD.root"
LOCALES_ROOT = "locales/"


# Program Error Codes Enumeration
class ErrorCodes(Enum):
    OK = 0
    MISSING_PROPERTY = 1
    MISSING_SETTINGS = 2
    MISSING_ENVIRONMENT = 3
    MISSING_LOCALE = 4
    UNSPECIFIED_PARENT = 5
    MISSING_TRANSLATION = 6
    UNKNOWN_TRANSLATION = 7
    SYNTAX_ERROR = 8


# Execution status codes for a step
class ExecutionStatus(Enum):
    PASSED = 0
    FAILED = 1
    PENDING_EXECUTION = 2
    PENDING_SOLVING = 3
    MISSING_STEP = 4
    RUNTIME_ERROR = 5
    SKIPPED = 6
    PENDING = 7


# Regular expressions lookup table (EDIT CAREFULLY)
class RegularExpressions:
    regexps = {
        'blank_line': r'^\s*$',
        'comment': r'#.*',
        'line_break': r'\n',
        'statement': r'^(\s*)(\w+):\s*(.*)$',
        'verb': r'^(\s*)([\w]+)[^:](.*)',
        'table': r'^(\s*)\|(.*)\|(.*)\|',
        'step_args': r'"(\w+)"',
        'spaces': r'\s+'
    }
