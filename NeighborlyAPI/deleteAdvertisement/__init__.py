import azure.functions as func
import pymongo
from bson.objectid import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get('id')

    if id:
        try:
            url = "mongodb://cosmos-db-account1-es81:VBq8TJoMuEZdAyOAskN5WAnz1QaKrQO7peGetkVFrwTMotAHUshw5HGZ7BPfYWEZVCnjIXsVwPMmACDbeURyFA==@cosmos-db-account1-es81.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-db-account1-es81@"
            client = pymongo.MongoClient(url)
            database = client['dbes81']
            collection = database['advertisements']

            query = {'_id': ObjectId(id)}
            result = collection.delete_one(query)
            return func.HttpResponse("")

        except:
            print("could not connect to mongodb")
            return func.HttpResponse("could not connect to mongodb", status_code=500)

    else:
        return func.HttpResponse("Please pass an id in the query string",
                                 status_code=400)
