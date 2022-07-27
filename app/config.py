from os import environ
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = environ.get("SECRET_KEY")

    # Flask APScheduler
    SCHEDULER_API_ENABLED = True

    # Rapid API
    RAPID_API_KEY = environ.get("RAPID_API_KEY")
    RAPID_API_AUTOCOMPLETE_HOST = "online-movie-database.p.rapidapi.com"
    RAPID_API_CONTENT_DATA_HOST = "movie-details1.p.rapidapi.com"


class ProdConfig(BaseConfig):
    # General flask's configuration
    ENV = "production"
    FLASK_ENV = "production"
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    # Flask
    ENV = "development"
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = False

    # Redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0

    # Content manager
    CONTENT_MANAGER_HOST = "localhost:5000"


class TestConfig(BaseConfig):
    # General flask's configuration
    ENV = "development"
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = True