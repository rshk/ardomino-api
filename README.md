# Ardomino API

Server-side application (draft) for [Ardomino](https://github.com/alfcrisci/Ardomino).

## Installation

```
% python setup.py develop
```

Configure:

```
% cp local_settings.example.py
```

..and configure ``local_settings.py`` to your needs.

Then create database:

```
% python
>>> from ardomino import db
>>> db.create_all()
```

To run:

```
% SETTINGS=$PWD/local_settings.py ardomino --debug --port 8080
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
