"""
application configuration variable
"""
import os


class BaseConfig(object):
    # Secret key for signing cookies
    SECRET_KEY = "-\\9PI4R7?#X4@4)*8-.PZX{1[0"

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # enabling the development environment
    DEBUG = True

    # Defining database address
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:" \
                              f"{os.getenv('POSTGRES_PASS', 'postgres')}@{os.getenv('POSTGRES_HOST', 'localhost')}/" \
                              f"{os.getenv('POSTGRES_DATABASE', 'feature_requests')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Application threads.
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2


class TestConfig(BaseConfig):
    TESTING = True

    # Defining database address
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:" \
                              f"{os.getenv('POSTGRES_PASS', 'postgres')}@{os.getenv('POSTGRES_HOST', 'localhost')}/" \
                              "test_feature_requests"

    CSRF_ENABLED = False
