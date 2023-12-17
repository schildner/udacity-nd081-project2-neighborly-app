import datetime
import logging
import pymongo
import os
import azure.functions as func


def main(req: func.HttpRequest,
         eventGridEvent: func.EventGridEvent,
         outputEvent: func.Out[func.EventGridOutputEvent]) -> func.HttpResponse:

    request = req.get_json()

    if request:
        try:
            url = "mongodb://cosmos-db-account-es81:9ViJPEBPVrmgwFfQacsKvX2FRJJiNP6ijT8Yv5RqCKgIgZNzFpg0ZaEulmafCPD3LoXTrsMixbQVACDbLrsGBQ==@cosmos-db-account-es81.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-db-account-es81@"
            client = pymongo.MongoClient(url)
            database = client['dbes81']
            collection = database['advertisements']

            rec_id1 = collection.insert_one(eval(request))

            # create test EventGridEvent
            logging.log("eventGridEvent: ", eventGridEvent)

            outputEvent.set(
                func.EventGridOutputEvent(
                    id="test-id",
                    data={"tag1": "value1", "tag2": "value2"},
                    subject="test-subject",
                    event_type="test-event-1",
                    event_time=datetime.datetime.utcnow(),
                    data_version="1.0"))

            return func.HttpResponse(req.get_body())

        except ValueError:
            print("could not connect to mongodb")
            return func.HttpResponse('Could not connect to mongodb', status_code=500)

    else:
        return func.HttpResponse(
            "Please pass name in the body",
            status_code=400
