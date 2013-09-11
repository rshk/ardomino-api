# Ardomino settings
# SETTINGS=/path/to/this_file.py python run.py

import os

#SQLALCHEMY_DATABASE_URI = \
#    "postgresql+psycopg2://user:pass@localhost/ardomino"
SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/ardomino.sqlite3"

DEBUG = True

## Ini configuration files for Ardomino
ARDOMINO_CONF_DIR = os.path.join(os.path.dirname(__file__), 'conf')
