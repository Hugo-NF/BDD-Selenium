"""BDD-Selenium - definitions.py
This file contains all the constants needed to run the program accordingly
"""

# built-in package for Enumeration
from enum import Enum

# Macro definitions
""" The following variables are used as macros across the program """
VERSION = '0.9.0beta'
LOGGER_INSTANCE = "SeleniumBDD.root"
LOCALES_ROOT = "locales/"
TARGET_BROWSER = 'firefox'


# Program Error Codes Enumeration
class ErrorCodes(Enum):
    """
    The ErrorCodes class defines all possible errors that can occur during the application runtime
    It's main purpose is providing a more legible error interface with the programmer and user
    """
    OK = 0
    MISSING_PROPERTY = 1
    MISSING_SETTINGS = 2
    MISSING_ENVIRONMENT = 3
    MISSING_LOCALE = 4
    UNSPECIFIED_PARENT = 5
    MISSING_TRANSLATION = 6
    UNKNOWN_TRANSLATION = 7
    SYNTAX_ERROR = 8
    SEMANTIC_ERROR = 9


# Execution status codes for a step
class ExecutionStatus(int, Enum):
    """
    The ExecutionStatus class defines an Enumeration of all possible states of the entities of the software
    These status codes are used in Features, Factories and Steps
    """
    PASSED = 0
    FAILED = 1
    PENDING_EXECUTION = 2
    PENDING_SOLVING = 3
    MISSING_REF = 4
    SKIPPED = 5
    PENDING = 6
    RUNNING = 7


# Regular expressions lookup table (EDIT CAREFULLY)
class RegularExpressions:
    """
    The RegularExpressions class works like an lookup table for regular expressions

    Attributes:
        regexps: static member consisting of a python dictionary that takes strings into regexps
    """
    regexps = {
        'blank_line': r'^\s*$',
        'comment': r'#.*',
        'line_break': r'\n',
        'statement': r'^(\s*)(\w+):\s*(.*)$',
        'verb': r'^(\s*)([\w]+)[^:](.*)',
        'table': r'^(\s*)\|(.*)\|(.*)\|',
        'step_args': r'"([^"]+)"',
        'spaces': r'\s+'
    }
