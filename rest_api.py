from flask import Flask
from flask_restful import Resource, Api, reqparse
from mongodb_utils import search_in_result_collection

app = Flask(__name__)
api = Api(app)


class Search(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, choices=['twitter', 'instagram', 'facebook'])
        parser.add_argument('author_id', type=str)
        parser.add_argument('object_text', type=str)
        parser.add_argument('language', type=str)
        parser.add_argument('keyword', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('lat', type=float, default=None)
        parser.add_argument('lon', type=float, default=None)
        parser.add_argument('distance', type=int, default=1000)
        parser.add_argument('time_start', type=int)
        parser.add_argument('time_end', type=int)
        parser.add_argument('limit', type=int, default=12)

        args = parser.parse_args()

        self.source = args['source']
        self.author_id = args['author_id']
        self.object_text = args['object_text']
        self.language = args['language']
        self.keyword = args['keyword']
        self.location = args['location']
        self.lat = args['lat']
        self.lon = args['lon']
        self.distance = args['distance']
        self.time_start = args['time_start']
        self.time_end = args['time_end']

        self.limit = args['limit']
        if self.limit > 10000:
            self.limit = 10000

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

        return result


api.add_resource(Search, '/api/search')
