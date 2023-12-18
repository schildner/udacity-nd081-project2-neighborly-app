import logging
import os

import azure.functions as func
import pymongo
import pymongo.errors
from bson.json_util import dumps

# from bson.objectid import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function getPost processing a request...')

    id = req.params.get('id')

    if id:
        try:
            uri = os.getenv('MyDbConnection')
            if uri is None:
                logging.error("DB connection string must be set in MyDbConnection env var.")
                return func.HttpResponse("Database connection string is not set.", status_code=500)

            client = pymongo.MongoClient(uri)
            db = client.dbes81
            collection = db.posts

            # If there is a document where '_id' is an object, then use this:
            # query = {'_id': ObjectId(id)}

            # If there is a document where '_id' is a string, then use this:
            query = {'_id': id}
            document = collection.find_one(query)

            if document is None:
                return func.HttpResponse(f"No document with _id = {id} found in the {db} DB",
                                         status_code=404)

            result = dumps(document)
            return func.HttpResponse(result, mimetype="application/json", charset='utf-8')

        except pymongo.errors.ConnectionFailure as e:
            logging.error(e)
            return func.HttpResponse("Database connection error.", status_code=500)
        except Exception as e:
            logging.error(e)
            return func.HttpResponse("An error occurred.", status_code=500)
    else:
        return func.HttpResponse("Please pass an id on the query string", status_code=400)
