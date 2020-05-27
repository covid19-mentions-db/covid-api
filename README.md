# covid-api

It's just a simple flask-restful project. You can simply run on your local computer  
'python3 runserver.py'  
or organize something like "nginx + uwsgi + app", or even use it in docker container  

<b>REQUIRED ENVIRONMENT VARIABLES</b>

\# Mongo DB to store posts
- `MONGODB_HOST`
- `MONGODB_PORT`
- `MONGODB_DB`
- `MONGODB_USER`
- `MONGODB_PASSWORD`
- `MONGODB_AUTH_DB`
- `MONGODB_RESULT_COLLECTION` - collection to store posts  

### How to use:
Api call example
- `https://covid19-mentions-db.com/api/search?object_text=Microsoft&limit=20&source=&author_id&object_text=&language&keyword&lat=&lon=&distance=&time_start=&time_end=&location=Canada`


### All the supported parameters:
- `source` - source of posts, possible values ['twitter', 'instagram', 'facebook']  
- `object_text` - post text(full text search)  
- `language` - language of post text(specified with object_text, need for stemming support, default value - en)  
- `keyword` - keyoword, used to find this post  
- `lat` - latitude of post  
- `lon` - longitude of post  
- `distance` - distance in metest, default=1000  
- `time_start` - posts older than specified timestamp  
- `time_end` - posts younger than specified timestamp  
- `limit` - limit of results, default=12, max=10000  
