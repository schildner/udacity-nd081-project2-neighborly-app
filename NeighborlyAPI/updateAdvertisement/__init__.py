import logging
import os

import azure.functions as func
import pymongo
import pymongo.errors
from bson.objectid import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function updateAdvertisement processing a request.')

    id = req.params.get('id')
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

            filter_query = {'_id': ObjectId(id)}
            # filter_query = {'_id': id}
            update_query = {"$set": eval(request)}

            rec_id1 = collection.update_one(filter_query, update_query)
            if rec_id1 is None or rec_id1.modified_count == 0:
                return func.HttpResponse(f"No document with _id = {id} found in the {db} DB",
                                         status_code=404)

            logging.info(f"record {rec_id1} updated successfully")

            return func.HttpResponse(status_code=200)

        except pymongo.errors.ConnectionFailure as e:
            logging.error(e)
            return func.HttpResponse("Database connection error.", status_code=500)
        except Exception as e:
            logging.error(e)
            return func.HttpResponse("An error occurred.", status_code=500)
    else:
        return func.HttpResponse("Please pass an id on the query string", status_code=400)
