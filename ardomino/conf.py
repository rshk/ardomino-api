"""
Utilities to read the Ardomino configuration
"""

from ConfigParser import RawConfigParser

_parsed_conf_file = None

def get_configuration():
    if _parsed_conf_file is not None:
        return _parsed_conf_file

    from . import app
    ardomino_conf_dir = app.config['ARDOMINO_CONF_DIR']
    conf_parser = RawConfigParser()
    for filename in os.listdir(ardomino_conf_dir):
        if (not filename.startswith('.')) and \
           filename.endswith('.ini'):
            self._conf_parser.read(
                os.path.join(ardomino_conf_dir, filename))

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

    _parsed_conf_file = conf_obj
    return conf_obj
