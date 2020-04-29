from flask import Flask
from flask_restful import Resource, Api, reqparse
from mongodb_utils import search_in_result_collection

app = Flask(__name__)
api = Api(app)


class Search(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, choices=['twitter', 'instagram', 'facebook', ''])
        parser.add_argument('author_id', type=str)
        parser.add_argument('object_text', type=str)
        parser.add_argument('language', type=str)
        parser.add_argument('keyword', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('lat', type=str)
        parser.add_argument('lon', type=str)
        parser.add_argument('distance', type=str, default='1000')
        parser.add_argument('time_start', type=str)
        parser.add_argument('time_end', type=str)
        parser.add_argument('limit', type=str, default='12')

        args = parser.parse_args()

        self.source = args['source']
        self.author_id = args['author_id']
        self.object_text = args['object_text']
        self.language = args['language']
        self.keyword = args['keyword']
        self.location = args['location']

        _lat = args['lat']
        if _lat:
            self.lat = float(_lat)
        else:
            self.lat = None
        _lon = args['lon']
        if _lon:
            self.lon = float(_lon)
        else:
            self.lon = None
        _distance = args['distance']
        if _distance:
            self.distance = int(_distance)
        else:
            self.distance = 1000

        _time_start = args['time_start']
        if _time_start:
            self.time_start = int(_time_start)
        else:
            self.time_start = None
        _time_end = args['time_end']
        if _time_end:
            self.time_end = int(_time_start)
        else:
            self.time_end = None

        _limit = args['limit']
        if _limit:
            self.limit = int(_limit)
            if self.limit > 10000:
                self.limit = 10000
        else:
            self.limit = 12

        super(Search, self).__init__()

    def get(self):
        result = search_in_result_collection(
            source=self.source,
            author_id=self.author_id,
            object_text=self.object_text,
            language=self.language,
            keyword=self.keyword,
            lat=self.lat,
            lon=self.lon,
            distance=self.distance,
            time_start=self.time_start,
            time_end=self.time_end,
            limit=self.limit,
        )
        if isinstance(result, list):
            return {'result': result}
        return result


api.add_resource(Search, '/api/search')
