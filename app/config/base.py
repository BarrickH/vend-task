import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """
    Base application configuration
    """
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    ENV = os.getenv('ENV')
    DEBUG = os.getenv('DEBUG', False)
    TESTING = os.getenv('TESTING', False)

    AWS_REGION = os.getenv('AWS_REGION_ZAPPA')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID_ZAPPA')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_ZAPPA')

