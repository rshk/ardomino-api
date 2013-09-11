import datetime
from math import ceil
import urllib

from flask import request
from flask.ext import restful
from sqlalchemy.orm.exc import NoResultFound

from .app import app
from .models import db, SensorReading


api = restful.Api(app, prefix='')


class SensorReadingResource(restful.Resource):
    def _serialize(self, obj):
        return {
            'id': obj.id,
            'device_name': obj.device_name,
            'sensor_name': obj.sensor_name,
            'sensor_value': obj.sensor_value,
            'sensor_units': obj.sensor_units,
            'date': obj.date.strftime("%F %T"),
        }

    def get(self):
        """
        Returns a list of readings
        """
        ## todo: add support for filtering, ...

        query = SensorReading.query


        ## Pagination
        page_size = 10
        page = 0
        if 'page_size' in request.args:
            try:
                page_size = int(request.args['page_size'])
            except ValueError:
                restful.abort(400, message="Page size must be an integer")
            if page_size < 1:
                restful.abort(
                    400, message="Page size must be greater than zero")
            if page_size > 100:
                page_size = 100

        pages_count = int(ceil(query.count() * 1.0 / page_size))
        max_page = pages_count - 1

        if 'page' in request.args:
            try:
                page = int(request.args['page'])
            except ValueError:
                restful.abort(400,
                              message="Page number must be an integer")
            if page < 0:
                restful.abort(
                    400, message='Page number cannot be negative')
            if page > max_page:
                restful.abort(404, message='Page number out of range')

        ## Pagination links
        links = {}

        def get_url(**kw):
            args = dict(request.args)
            args.update(kw)
            query_string = urllib.urlencode(args)
            if query_string:
                return '{0}?{1}'.format(request.base_url, query_string)
            return request.base_url

        def get_page_url(page):
            return get_url(page=page, page_size=page_size)

        if page > 0:
            links['first'] = get_page_url(0)
            links['prev'] = get_page_url(page - 1)

        if page < max_page:
            links['next'] = get_page_url(page + 1)
            links['last'] = get_page_url(max_page)

        headers = {}

        if len(links):
            links_header = ', '.join('<{0}>; rel="{1}"'.format(k, v)
                                     for k, v in links.iteritems())
            headers['Link'] = links_header

        results = query.slice(page * page_size, (page + 1) * page_size)
        return [self._serialize(o) for o in results], 200, headers

    def post(self):
        new = SensorReading()
        obj = request.json
        new.device_name = obj['device_name']
        new.sensor_name = obj['sensor_name']
        new.sensor_value = obj['sensor_value']
        if 'date' in obj:
            new.date = datetime.datetime.strptime(obj['date'], '%F %T')
        else:
            new.date = datetime.datetime.now()
        db.session.add(new)
        db.session.commit()
        return self._serialize(new)  # todo: return 201 Created instead?


api.add_resource(SensorReadingResource, '/')


# api.add_resource(DatasetDistributionsResource,
#                  '/dataset/<int:obj_id>/resources/')
# api.add_resource(DistributionResource,
#                  '/distribution/',
#                  '/distribution/<int:obj_id>/')
