import logging
import os

import azure.functions as func
import pymongo
import pymongo.errors


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function createAdvertisement processing a request.')

    request = req.get_json()

    if request:
        try:
            uri = os.getenv('MyDbConnection')
            if uri is None:
                logging.error("DB connection string must be set in MyDbConnection env var.")
                return func.HttpResponse("Database connection string is not set.", status_code=500)

            client = pymongo.MongoClient(uri)
            db = client.dbes81
            collection = db.advertisements

            rec_id1 = collection.insert_one(eval(request))
            if rec_id1 is None or rec_id1.inserted_id is None:
                return func.HttpResponse(f"The following entry could not be inserted into the {db} DB: {request}",
                                         status_code=404)

            logging.info(f"The record {rec_id1} has been inserted successfully to the {db} DB.")

            return func.HttpResponse(req.get_body())

        except pymongo.errors.ConnectionFailure as e:
            logging.error(e)
            return func.HttpResponse("Database connection error.", status_code=500)
        except ValueError as e:
            logging.error(e)
            return func.HttpResponse('Could not connect to mongodb', status_code=500)
        except Exception as e:
            logging.error(e)
            return func.HttpResponse("An error occurred.", status_code=500)

    else:
        return func.HttpResponse("Please pass name in the body", status_code=400)
