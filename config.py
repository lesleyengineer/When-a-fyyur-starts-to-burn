import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Alexa3055!@localhost:5432/fyyurlesapp'


# DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
# DB_USER = os.getenv('DB_USER', 'postgres')
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'Alexa3055!')
# DB_NAME = os.getenv('DB_NAME', 'fyyurlesapp')

# DB_PATH = 'postgresql+psycopg2://{postgres}:{Alexa3055!}@{127.0.0.1:5432}/{fyyurlesapp}'.format(
#     DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
