from enum import Enum

class Tag(str, Enum):
    MISC = 'Miscellaneous'
    AUTHENTICATION = 'Authentication'
    USER = 'Users'


class Environment(str, Enum):
    TEST = 'test'
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'

class ApiResponseMessage(str, Enum):
    AUTHENTICATION_FAILED = "Authentication Failed"