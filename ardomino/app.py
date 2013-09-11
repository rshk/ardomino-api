import os
from ConfigParser import RawConfigParser

from flask import Flask

app = Flask(__name__)

## Configuration
app.config.update(dict(
    DEBUG=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///tmp/ardomino.sqlite',
))
app.config.from_envvar('SETTINGS', silent=True)
