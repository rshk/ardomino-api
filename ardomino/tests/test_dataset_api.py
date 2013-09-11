"""
Tests for the Ardomino API
"""

import datetime
import json

from .fixtures import app


def post_data(app, url, data):
    return app.post(url, data=json.dumps(data),
                    content_type='application/json')


def test_objects_crud(app):
    result = app.get('/')
    assert result.status_code == 200

    ## To check that this is valid JSON
    data = json.loads(result.data)

    ## Make sure the db is empty
    assert data == []

    ## Create an object
    myobj = {
        'date': '2013-09-11 09:00:00',
        'device_name': 'device01',
        'location': 'Trento, Italy',
        'sensor_name': 'Temperature',
        'sensor_value': '16',
        'sensor_units': 'degC',
    }

    result = post_data(app, '/', myobj)
    assert result.status_code == 201  # 201 Created

    ## Make sure all the keys got stored correctly
    new_obj = json.loads(result.data)
    for key in myobj:
        assert new_obj[key] == myobj[key]

    ## Insert a bunch of readings
    dummy_data = [
        (9,  30, '16'),
        (10,  0, '17'),
        (10, 30, '17'),
        (11,  0, '18'),
        (11, 30, '19'),
        (12,  0, '20'),
        (12, 30, '20'),
    ]
    for hours, minutes, temperature in dummy_data:
        myobj = {
            'date': '2013-09-11 {:02d}:{:02d}:00'.format(hours, minutes),
            'device_name': 'device01',
            'location': 'Trento, Italy',
            'sensor_name': 'Temperature',
            'sensor_value': temperature,
            'sensor_units': 'degC',
        }
        result = post_data(app, '/', myobj)
        assert result.status_code == 201

    result = app.get('/')
    data = json.loads(result.data)

    assert len(data) == 8
    for rid, record in enumerate(data[1:]):
        dt = datetime.datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')
        ddrecord = dummy_data[rid]
        assert dt.hour == ddrecord[0]
        assert dt.minute == ddrecord[1]
        assert record['sensor_value'] == ddrecord[2]


def test_pagination(app):
    ## Create a bunch of readings

    import random

    for i in xrange(50):
        obj = {
            'device_name': 'device{:02d}'.format(random.randint(0, 99)),
            'location': random.choice(['Trento', 'Firenze', 'Como', 'Roma']),
            'sensor_name': 'temperature',
            'sensor_value': str(random.randint(15, 25)),
            'sensor_units': 'degC',
        }
        result = post_data(app, '/', obj)
        assert result.status_code == 201

    ## todo: check maximum page size
    ## todo: check Link headers (use python-requests to parse them?)
    ## todo: add support for, and check, headers with paging information

    ## First 50-items page (should include all results)
    result = app.get('/?page_size=50')
    all_data = data = json.loads(result.data)
    assert len(data) == 50

    ## First 10-items page
    result = app.get('/?page_size=10')
    data = json.loads(result.data)
    assert len(data) == 10
    assert data == all_data[:10]

    ## Second 10-items page
    result = app.get('/?page_size=10&page=1')
    data = json.loads(result.data)
    assert len(data) == 10
    assert data == all_data[10:20]

    ## Invalid page size
    result = app.get('/?page_size=NotANumber')
    assert result.status_code == 400

    ## Negative page size
    result = app.get('/?page_size=-1')
    assert result.status_code == 400

    ## Invalid page number
    result = app.get('/?page=NotANumber')
    assert result.status_code == 400

    ## Negative page number
    result = app.get('/?page=-1')
    assert result.status_code == 400

    ## Test out-of-range page
    result = app.get('/?page_size=10&page=5')
    assert result.status_code == 404
