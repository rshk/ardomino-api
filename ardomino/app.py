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
