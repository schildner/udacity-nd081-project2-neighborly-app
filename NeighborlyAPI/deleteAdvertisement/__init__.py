import logging
import os

import azure.functions as func
import pymongo
import pymongo.errors
from bson.objectid import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get('id')

    if id:
        try:
            uri = os.getenv('MyDbConnection')
            if uri is None:
                logging.error("DB connection string must be set in MyDbConnection env var.")
                return func.HttpResponse("Database connection string is not set.", status_code=500)

            client = pymongo.MongoClient(uri)
            db = client.dbes81
            collection = db.advertisements

            # query = {'_id': id}
            query = {'_id': ObjectId(id)}
            result = collection.delete_one(query)
            logging.info(f"Deletion from {db} result: {result}")
            return func.HttpResponse("")

        except pymongo.errors.ConnectionFailure as e:
            logging.error(e)
            return func.HttpResponse("Database connection error.", status_code=500)
        except Exception as e:
            logging.error(e)
            return func.HttpResponse("An error occurred.", status_code=500)

    else:
        return func.HttpResponse("Please pass an id in the query string",
                                 status_code=400)
