import os

# Secret key for signing cookies
SECRET_KEY = "-\\9PI4R7?#X4@4)*8-.PZX{1[0"

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# enabling the development environment
DEBUG = True

# Defining database address
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/feature_requests"
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Application threads.
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

