import os
from ConfigParser import RawConfigParser

from flask import Flask

app = Flask(__name__)

## Configuration
app.config['DEBUG'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = \
#    'postgresql+psycopg2://user:pass@pg.example.com/my-database'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:////tmp/ardomino.sqlite'

app.config.from_envvar('SETTINGS')


## Load ardomino-specific settings, from ini files

ARDOMINO_CONF_DIR = os.environment.get('ARDOMINO_SETTINGS')
if ARDOMINO_CONF_DIR is None:
    ARDOMINO_CONF_DIR = app.config['ARDOMINO_CONF_DIR']

ardomino_settings = RawConfigParser()
for filename in os.listdir(ARDOMINO_CONF_DIR):
    if (not filename.startswith('.')) and filename.endswith('.ini'):
        ardomino_settings.read(os.path.join(ARDOMINO_CONF_DIR, filename))
