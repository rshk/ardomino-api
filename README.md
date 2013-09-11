# Ardomino API

Server-side application (draft) for [Ardomino](https://github.com/alfcrisci/Ardomino).

## Installation

Install in "development mode"

```
% python setup.py develop
```

Configure:

```
% cp local_settings.example.py local_settings.py
```

..and configure ``local_settings.py`` to suit your needs.

Then create database:

```
% SETTINGS=$PWD/local_settings.py ardomino initdb
```

You could also do this manually:

```
% SETTINGS=$PWD/local_settings.py python
>>> from ardomino import db
>>> db.create_all()
```

To run:

```
% SETTINGS=$PWD/local_settings.py ardomino run --debug --port 8080
```

then visit http://127.0.0.1:8080


## Trying out

To test the application:

```
% pip install httpie
% http POST http://127.0.0.1:8080 device_name="My device" sensor_name="sensor_1" sensor_value="1234"
% http GET http://127.0.0.1:8080
```


## The (basic) API

* ``GET /`` returns a (paginated) list of sensor readings. The ``Link:`` header
  of the response will contain the first/prev/next/last page URLs.

* ``POST /`` can be used to add sensor readings (as JSON objects).

  Example: ``{"device_name": "My device", "sensor_name": "sensor_1", "sensor_value": "1234"}``.

### Example usage from a Python script

We'll use the ``requests`` module to play around a bit with the API.

```python
import requests
import json

data = {
}
requests.post(
	'http://127.0.0.1:8000',
	data=json.dumps(data),
	headers={'content-type': 'application/json'})

## todo: add instructions for paginated read
```
