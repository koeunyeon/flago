import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    DEBUG = False

class ProductConfig(Config):    
    MONGO_URI = "localhost:27017/"
    MONGO_DBNAME = "product_db"

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev_secret_key"
    MONGO_URI = "localhost:27017/"
    MONGO_DBNAME = "dev_db"


class TestConfig(Config):
    DEBUG = True
    SECRET_KEY = "test_secret_key"
    MONGO_URI = "localhost:27017/"
    MONGO_DBNAME = "test_db"


config_by_name = dict(
    prod=ProductConfig,
    dev=DevelopmentConfig,
    test=TestConfig
)


def from_object(config_name=None):
    if config_name is not None:
        return config_by_name[config_name]

    env_config_name = os.getenv("FLASK_ENV", None)
    if env_config_name is not None:
        return config_by_name[env_config_name]
        
    default_config_name = 'dev'
    return config_by_name[default_config_name]
