import azure.functions as func
import pymongo
import json
from bson.json_util import dumps

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        url = "mongodb://cosmos-db-account1-es81:VBq8TJoMuEZdAyOAskN5WAnz1QaKrQO7peGetkVFrwTMotAHUshw5HGZ7BPfYWEZVCnjIXsVwPMmACDbeURyFA==@cosmos-db-account1-es81.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-db-account1-es81@"
        client = pymongo.MongoClient(url)
        database = client['dbes81']
        collection = database['advertisements']


        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
    except:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb",
                                 status_code=400)

