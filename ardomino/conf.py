"""
Utilities to read the Ardomino configuration
"""

from ConfigParser import RawConfigParser


_parsed_conf_file = None


def get_configuration():
    """
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

    if _parsed_conf_file is not None:
        return _parsed_conf_file

    ARDOMINO_CONF_DIR = os.environ.get('ARDOMINO_CONF_DIR')
    if ARDOMINO_CONF_DIR is None:
        from . import app
        ARDOMINO_CONF_DIR = app.config['ARDOMINO_CONF_DIR']

    conf_parser = RawConfigParser()
    conf_files = (
        os.path.join(ARDOMINO_CONF_DIR, f)
        for f in sorted(
            f2 for f2 in os.listdir(ARDOMINO_CONF_DIR)
            if (not filename.startswith('.')) and filename.endswith('.ini')
        ))
    conf_parser.read(conf_files)

    ## Now, create a [group][name][option] dict
    ## out of the configuration file.
    ## Group names are taken from [{type}:{name}] section names.
    conf_obj = {}
    for section in conf_parser.sections():
        section_type, name = section.split(':')
        if section_type not in conf_obj:
            conf_obj[section_type] = {}
        conf_obj[section_type][name] = {
            opt: conf_parser.get(section, opt)
            for opt in conf_parser.options(section)
        }

    ## Cache this for later..
    _parsed_conf_file = conf_obj
    return conf_obj
