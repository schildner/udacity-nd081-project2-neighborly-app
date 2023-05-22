import logging
import azure.functions as func
import pymongo
import json
from bson.json_util import dumps


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python getPosts trigger function processed a request.')

    try:
        url = "mongodb://cosmos-db-account-es81:9n6ytBSPTUdj5W6Ne7ywfnUsV9AbLKSJegjKWl2PhjV0PAJ58pgQKKCkKRPFB2ZrXfum4BFdHTuVACDbeZVYfQ==@cosmos-db-account-es81.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-db-account-es81@"
        client = pymongo.MongoClient(url)
        database = client['dbes81']
        collection = database['posts']

        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8', status_code=200)
    except:
        return func.HttpResponse("Bad request.", status_code=400)