#!/usr/bin/env python

## Downloads archive data from ilmeteo.it and pushes it
## to an ardomino-api application, for testing purposes

from __future__ import print_function

import csv
import datetime
import json
import os
import sys

import requests


month_names = dict(enumerate([
    'Gennaio',
    'Febbraio',
    'Marzo',
    'Aprile',
    'Maggio',
    'Giugno',
    'Luglio',
    'Agosto',
    'Settembre',
    'Ottobre',
    'Novembre',
    'Dicembre',
], 1))

label_translations = {
    'data': 'date',
    'fenomeni': 'weather',
    'localita': 'location',
    'pioggia': 'precipitation',
    'pressionemedia': 'avg_pressure',
    'pressioneslm': 'pressure',
    'puntorugiada': 'dew_point',
    'raffica': 'wind_max',
    'tmax': 'temperature_max',
    'tmedia': 'temperature_avg',
    'tmin': 'temperature_min',
    'umidita': 'humidity',
    'ventomax': 'wind_max',
    'ventomedia': 'wind_avg',
    'visibilita': 'visibility',
}

units_translations = {
    '\xc2\xb0C': 'degC',
}


url_template = "http://www.ilmeteo.it/portale/archivio-meteo/"\
               "{city}/{year}/{month}?format=csv"

cache_dir = os.path.join(os.path.dirname(__file__), '.dl-cache')


def download_data(city, year, month):
    cache_key = "{city}_{year:04d}-{month:02d}.csv".format(
        city=city, year=year, month=month)
    cached_file = os.path.join(cache_dir, cache_key)

    if os.path.isdir(cache_dir) and os.path.exists(cached_file):
        print(">>> Using file from cache", file=sys.stderr)
        ## We do this way to avoid keeping open files around..
        with open(cached_file, 'r') as f:
            text = f.read()
        text = text.splitlines()

    else:
        print(">>> Downloading file", file=sys.stderr)
        month_name = month_names[month]
        url = url_template.format(city=city, year=year, month=month_name)
        response = requests.get(url)
        assert response.ok
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        response_text = response.text.encode('utf-8')
        with open(cached_file, 'w') as f:
            f.write(response_text)
        text = response_text.splitlines()

    ## Ok, now we can read the CSV
    csvr = csv.reader(text, delimiter=';', quotechar='"')
    raw_header = csvr.next()
    header = []
    for column in raw_header:
        column = column.strip()
        if ' ' in column:
            label, units = column.rsplit(None, 1)
        else:
            label, units = column, None
        label = label.lower()
        if label in label_translations:
            label = label_translations[label]
        if units in units_translations:
            units = units_translations[units]
        header.append((label, units))

    for row in csvr:
        obj = {}
        for column_id, (col_name, col_units) in enumerate(header):
            value = row[column_id]
            if col_name == 'date':
                value = datetime.datetime.strptime(value, '%d/%m/%Y')
            obj[col_name] = {
                'value': value,
                'units': col_units,
            }
        yield obj


date_range = zip([2012] * 12, range(1, 13)) + \
             zip([2012] * 12, range(1, 10))

cities = ['Trento', 'Firenze', 'Como', 'Milano']

for city in cities:
    for year, month in date_range:
        for line in download_data(city, year, month):
            print(line)
