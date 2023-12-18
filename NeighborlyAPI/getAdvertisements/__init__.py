import logging
import os

import azure.functions as func
import pymongo
import pymongo.errors
from bson.json_util import dumps


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function getAdvertisements processing a request...')

    try:
        uri = os.getenv('MyDbConnection')
        if uri is None:
            logging.error("DB connection string must be set in MyDbConnection env var.")
            return func.HttpResponse("Database connection string is not set.", status_code=500)

        client = pymongo.MongoClient(uri)
        database = client['dbes81']
        collection = database['advertisements']

        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result,
                                 mimetype="application/json",
                                 charset='utf-8',
                                 status_code=200)

    except pymongo.errors.ConnectionFailure as e:
        logging.error(e)
        return func.HttpResponse("Database connection error.", status_code=500)
    except Exception as e:
        logging.error(e)
        return func.HttpResponse("An error occurred.", status_code=500)
