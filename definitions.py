from enum import Enum

# Macro definitions
LOGGER_INSTANCE = "SeleniumBDD.root"


# Program Error Codes Enumeration
class ErrorCodes(Enum):
    MISSING_PROPERTY = 1
    MISSING_SETTINGS = 2
    MISSING_ENVIRONMENT = 3
