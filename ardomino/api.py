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
        links = []

        def get_url(**kw):
            args = dict(request.args)
            args.update(kw)
            query_string = urllib.urlencode(args)
            if query_string:
                return '{0}?{1}'.format(request.base_url, query_string)
            return request.base_url

        if page > 0:
            links.append("<{0}>; rel=\"first\""
                         "".format(get_url(page=0,
                                           page_size=page_size)))
            links.append("<{0}>; rel=\"prev\""
                         "".format(get_url(page=page-1,
                                           page_size=page_size)))
        if page < max_page:
            links.append("<{0}>; rel=\"next\""
                         "".format(get_url(page=page+1,
                                           page_size=page_size)))
            links.append("<{0}>; rel=\"last\""
                         "".format(get_url(page=max_page,
                                           page_size=page_size)))

        headers = {'Link': ", ".join(links)}
        results = query.slice(page * page_size, (page + 1) * page_size)
        return [self._serialize(o) for o in results], 200, headers

    def post(self):
        new = SensorReading()
        obj = request.json
        new.device_name = obj['device_name']
        new.sensor_name = obj['sensor_name']
        new.sensor_value = obj['sensor_value']
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
