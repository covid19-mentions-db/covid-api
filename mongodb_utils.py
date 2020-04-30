import os
import pymongo
from pymongo.errors import ExecutionTimeout
import re
from bson.json_util import dumps


mongodb_host = os.getenv('MONGODB_HOST')
mongodb_port = int(os.getenv('MONGODB_PORT'))
mongodb_db = os.getenv('MONGODB_DB')
mongodb_result_collection = os.getenv('MONGODB_RESULT_COLLECTION')
mongodb_user = os.getenv('MONGODB_USER')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_auth_db = os.getenv('MONGODB_AUTH_DB')


print('connect mongodb')
# MONGODB config
client = pymongo.MongoClient(
    mongodb_host,
    mongodb_port,
    username=mongodb_user,
    password=mongodb_password,
    authSource=mongodb_auth_db
)
db = client[mongodb_db]
result_collection = db[mongodb_result_collection]
print('create author_id index')
result_collection.create_index([("author_id", pymongo.ASCENDING)])
print('create object_text index')
result_collection.create_index([("object_text", pymongo.TEXT)],
                               default_language='english',
                               language_override='index_lang')
print('create keyword index')
result_collection.create_index([("keyword", pymongo.ASCENDING)])
print('create location 2d index')
result_collection.create_index([("location.coordinates", pymongo.GEO2D)])
print('create time index')
result_collection.create_index([("time", pymongo.ASCENDING)])
print('create location.name index')
result_collection.create_index([("location.name", pymongo.ASCENDING)])
print('end create')


def search_in_result_collection(source=None, author_id=None, object_text=None, language=None, keyword=None, location=None,
                                lat=None, lon=None, distance=None, time_start=None, time_end=None, limit=12):

    search_query = {}
    explicit_fields = {'_id': 0}
    if source:
        search_query['source'] = source
    if author_id:
        search_query['author_id'] = author_id
    if object_text:
        search_query['$text'] = {'$search': object_text}
        if language:
            search_query['$text']['$language'] = language
        # explicit_fields['score'] = {'$meta': 'textScore'}
    if keyword:
        keyword = keyword.replace(',', ' ')
        keyword = re.sub(' +', ' ', keyword)
        keywords = keyword.split(' ')
        search_query['keyword'] = {'$in': keywords}
    if lat and lon and distance:
        # distance in meters
        search_query['location.coordinates'] = {'$geoWithin': {'$centerSphere': [[lon, lat], distance / 6378100]}}

    if location:
        search_query['location.name'] = location

    if time_start or time_end:
        search_query['time'] = {}
        if time_start:
            search_query['time']['$gte'] = time_start
        if time_end:
            search_query['time']['$lte'] = time_end

    if not search_query:
        raise Exception('you need to specify at least one parameter')

    print(search_query)
    try:
        search_result = result_collection.find(search_query, explicit_fields).limit(limit).max_time_ms(120000)
        # if object_text:
        #     search_result = search_result.sort([('score', {'$meta': 'textScore'})])
        return [elem for elem in search_result]
    except ExecutionTimeout:
        return {'error': 'ExecutionTimeout'}


if __name__ == '__main__':
    # res = search_in_result_collection(source='instagram',
    #                                   object_text='moving',
    #                                   language='en',
    #                                   keyword='covidkindness,coronavairus',
    #                                   time_start=1586034330,
    #                                   time_end=1586245522)
    res = search_in_result_collection(lat=54.7534496, lon=56.0306028, distance=100)
    print(dumps(res))
