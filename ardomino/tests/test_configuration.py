"""
Tests for configuration file parsers, ...
"""

from ConfigParser import RawConfigParser
import io
import os
import textwrap

import pytest

from ardomino.conf import (process_conf_files,
                           find_configuration_files,
                           create_conf_parser)


@pytest.fixture
def conf_dir(tmpdir):
    with open(str(tmpdir.join('food.ini')), 'w') as f:
        f.write(textwrap.dedent("""
        [food:Egg]
        taste = Great

        [food:Bacon]
        taste = Delicious

        [food:Spam]
        taste = Sublime
        """))
    with open(str(tmpdir.join('beverages.ini')), 'w') as f:
        f.write(textwrap.dedent("""
        [beverage:Coffee]
        color = black

        [beverage:Milk]
        color = white

        [beverage:Tea]
        color = brown
        """))
    with open(str(tmpdir.join('pets.ini')), 'w') as f:
        f.write(textwrap.dedent("""
        [pet:Cat]
        says = Meow

        [pet:Dog]
        says = Bark

        [pet:Snake]
        says =
        """))
    with open(str(tmpdir.join('not-a-conf-file.txt')), 'w') as f:
        f.write(textwrap.dedent("""
        [this-is:not]
        what = a configuration file!
        """))
    return tmpdir


def test_create_conf_parser(conf_dir):
    conf_parser = create_conf_parser(str(conf_dir))
    assert 'pet:Cat' in conf_parser.sections()
    assert 'food:Bacon' in conf_parser.sections()
    assert 'beverage:Coffee' in conf_parser.sections()
    assert 'this-is:not' not in conf_parser.sections()


def test_find_configuration_files(conf_dir):
    found = find_configuration_files(str(conf_dir))
    assert sorted(found) == [
        str(conf_dir.join(n))
        for n in 'beverages.ini', 'food.ini', 'pets.ini'
    ]


def test_process_conf_files():
    example_conf = textwrap.dedent("""
    [food:Egg]
    description = A nice round egg

    [food:Spam]
    description = Spam Spam Spam Spam Spam!

    [person:JohnDoe]
    first_name = John
    last_name = Doe
    """)
    expected_result = {
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
    conf_parser = RawConfigParser()
    conf_parser.readfp(io.BytesIO(example_conf))
    result = process_conf_files(conf_parser)
    assert result == expected_result
    pass


def test_process_conf_dir(conf_dir):
    parser = create_conf_parser(str(conf_dir))
    obj = process_conf_files(parser)
    assert sorted(obj.keys()) == ['beverage', 'food', 'pet']
    assert sorted(obj['beverage'].keys()) == ['Coffee', 'Milk', 'Tea']
    assert sorted(obj['food'].keys()) == ['Bacon', 'Egg', 'Spam']
    assert sorted(obj['pet'].keys()) == ['Cat', 'Dog', 'Snake']
    assert obj['food']['Bacon'] == {'taste': 'Delicious'}
    assert obj['food']['Spam'] == {'taste': 'Sublime'}
