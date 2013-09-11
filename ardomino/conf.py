"""
Utilities to read the Ardomino configuration

Load ardomino-specific settings, from ini files
contained in ARDOMINO_CONF_DIR.

Path to the directory containing settings files can be
passed via the ARDOMINO_CONF_DIR application setting
or the ARDOMINO_CONF_DIR environment variable (which,
if specified, takes precedence).

Configuration is then converted by creating "groups"
by splitting section names on ':'.

Example::

    [food:Egg]
    description = A nice round egg

    [food:Spam]
    description = Spam Spam Spam Spam Spam!

    [person:JohnDoe]
    first_name = John
    last_name = Doe

Becomes::

    {
        'food': {
            'Egg': {'description': 'A nice round egg'},
            'Spam': {'description': 'Spam Spam Spam Spam Spam!'},
        },
        'person': {
            'JohnDoe': {
                'first_name': 'John',
                'last_name': 'Doe',
            }
        }
    }
"""

from ConfigParser import RawConfigParser
import os


_parsed_conf_file = None


def get_configuration():
    global _parsed_conf_file
    if _parsed_conf_file is None:
        _parsed_conf_file = _get_configuration()
    return _parsed_conf_file


def _get_configuration():
    ARDOMINO_CONF_DIR = os.environ.get('ARDOMINO_CONF_DIR')
    if ARDOMINO_CONF_DIR is None:
        from . import app
        ARDOMINO_CONF_DIR = app.config['ARDOMINO_CONF_DIR']

    conf_parser = create_conf_parser(ARDOMINO_CONF_DIR)
    return process_conf_files(conf_parser)


def create_conf_parser(basedir):
    conf_parser = RawConfigParser()
    conf_parser.read(find_configuration_files(basedir))
    return conf_parser


def find_configuration_files(basedir):
    return (
        os.path.join(basedir, f)
        for f in sorted(
            f2 for f2 in os.listdir(basedir)
            if (not f2.startswith('.')) and f2.endswith('.ini')
        ))


def process_conf_files(conf_parser):
    conf_obj = {}
    for section in conf_parser.sections():
        section_type, name = section.split(':')
        if section_type not in conf_obj:
            conf_obj[section_type] = {}
        conf_obj[section_type][name] = {
            opt: conf_parser.get(section, opt)
            for opt in conf_parser.options(section)
        }
    return conf_obj
