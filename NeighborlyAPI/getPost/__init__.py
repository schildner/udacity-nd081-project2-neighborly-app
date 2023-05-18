import azure.functions as func
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get('id')

    if id:
        try:
            url = "mongodb://cosmos-db-account-es81:Mqxk0U1ppq1aMCkCBB7yF5rG6F8gLs8ocyhyPihXkchj9i3nexJfvQs4rRzcp2Kq4qVAh7TonNOfACDbFf5FAw==@cosmos-db-account-es81.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-db-account-es81@"
            client = pymongo.MongoClient(url)
            database = client['azure']
            collection = database['posts']

            query = {'_id': ObjectId(id)}
            result = collection.find_one(query)
            result = dumps(result)

            return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
        except:
            return func.HttpResponse("Database connection error.", status_code=500)

    else:
        return func.HttpResponse("Please pass an id parameter in the query string.", status_code=400)