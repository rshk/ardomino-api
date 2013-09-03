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
