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
