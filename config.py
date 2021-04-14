import os


class Config:
    """
    Common Configuration
    """
    T_USERNAME = os.getenv('T_USERNAME')
    T_CLIENT_ID = os.getenv('T_CLIENT_ID')
    T_TOKEN = os.getenv('T_TOKEN')
    T_CHANNEL = os.getenv('T_CHANNEL')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'testing': TestingConfig,
    'production': ProductionConfig
}

CONFIGURATION_NAME = os.getenv('TWITCH_BOT_CONFIG', 'testing')

if CONFIGURATION_NAME not in app_config:
    raise RuntimeError(f'Invalid configuration string {CONFIGURATION_NAME}')

config: Config = app_config[CONFIGURATION_NAME]()
