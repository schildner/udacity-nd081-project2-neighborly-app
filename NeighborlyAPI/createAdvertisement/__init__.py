import azure.functions as func
import pymongo

def main(req: func.HttpRequest) -> func.HttpResponse:

    request = req.get_json()

    if request:
        try:
            url = "mongodb://cosmos-db-account-es81:9n6ytBSPTUdj5W6Ne7ywfnUsV9AbLKSJegjKWl2PhjV0PAJ58pgQKKCkKRPFB2ZrXfum4BFdHTuVACDbeZVYfQ==@cosmos-db-account-es81.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-db-account-es81@"
            client = pymongo.MongoClient(url)
            database = client['dbes81']
            collection = database['advertisements']

            rec_id1 = collection.insert_one(eval(request))

            return func.HttpResponse(req.get_body())

        except ValueError:
            print("could not connect to mongodb")
            return func.HttpResponse('Could not connect to mongodb', status_code=500)

    else:
        return func.HttpResponse(
            "Please pass name in the body",
            status_code=400
        )