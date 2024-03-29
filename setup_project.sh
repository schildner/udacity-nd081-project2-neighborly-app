#!/usr/bin/env bash

YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color

# shellcheck disable=SC1091
source ./variables.sh

az group create -n "${RG_NAME}" -l "${LOCATION}"

# Create a Cosmos account for MongoDB
az cosmosdb create \
    -n "${COSMOS_DB_ACCOUNT_NAME}" \
    -g "${RG_NAME}" \
    --kind MongoDB \
    --server-version "${DB_SERVER_VERSION}" \
    --default-consistency-level Eventual \
    --enable-automatic-failover false

# Create a JSON file in the current directory defining the index policy for the collection.
# The indexing policy file defines which field to create an index on for faster search/read.
printf '
[
    {
        "key": {"keys": ["_id"]}
    }
]' > "idxpolicy-${SUFFIX}.json"

# Create a MongoDB API Collections
az cosmosdb mongodb collection create \
    -a "${COSMOS_DB_ACCOUNT_NAME}" \
    -g "${RG_NAME}" \
    -d "${DB_NAME}"  \
    -n "${COLLECTION_1}" \
    --shard '_id' \
    --throughput 400 \
    --idx "@idxpolicy-${SUFFIX}.json"

az cosmosdb mongodb collection create \
    -a "${COSMOS_DB_ACCOUNT_NAME}" \
    -g "${RG_NAME}" \
    -d "${DB_NAME}"  \
    -n "${COLLECTION_2}" \
    --shard '_id' \
    --throughput 400 \
    --idx "@idxpolicy-${SUFFIX}.json"

echo "Connection strings can be obtained as follows:"
echo "az cosmosdb keys list -n ${COSMOS_DB_ACCOUNT_NAME} -g ${RG_NAME} --type connection-strings"

# Fetch and store the connection string
DB_CONNECTION_STRING=$(az cosmosdb keys list \
    --type connection-strings \
    -n "${COSMOS_DB_ACCOUNT_NAME}" \
    -g "${RG_NAME}" \
    --query 'connectionStrings[0].connectionString' \
    --output tsv)
echo The connection string will be needed later to connect the app with the DB, so make sure to save it somewhere.
echo -e "${YELLOW}${DB_CONNECTION_STRING}${NC}"

# Import data into the collections
mongoimport --uri "${DB_CONNECTION_STRING}" \
    --db "${DB_NAME}" \
    --collection "${COLLECTION_1}" \
    --file='./sample_data/sampleAds.json' \
    --jsonArray

mongoimport --uri "${DB_CONNECTION_STRING}" \
    --db "${DB_NAME}" \
    --collection "${COLLECTION_2}" \
    --file='./sample_data/samplePosts.json' \
    --jsonArray

# Create Function App
az storage account create -n "${STORAGE_ACCOUNT_NAME}" --location "${LOCATION}" -g "${RG_NAME}" --sku Standard_LRS

az appservice plan create \
    -n "backend_asp" \
    -g "${RG_NAME}" \
    --is-linux \
    --number-of-workers 1 \
    --sku B1 \
    --location "${LOCATION}"

az functionapp create \
    -n "${FUNCTION_APP_NAME}" \
    -g "${RG_NAME}" \
    --plan "backend_asp" \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4 \
    --os-type linux \
    -s "${STORAGE_ACCOUNT_NAME}"

az functionapp config appsettings set \
    -n "${FUNCTION_APP_NAME}" \
    -g "${RG_NAME}" \
    --settings "MyDbConnection=${DB_CONNECTION_STRING}"

# Deploy the function app
cd NeighborlyAPI || exit
python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -r requirements.txt
func azure functionapp publish "${FUNCTION_APP_NAME}" \
    --python \
    --build remote

cd ..
# Deploy the web app
cd NeighborlyFrontEnd || exit

# install dependencies via pipenv
#pipenv install
#pipenv shell

# alternatively install dependencies via pip install
python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -r requirements.txt

az webapp up \
    -n "${WEB_APP_NAME}"\
    -g "${RG_NAME}" \
    -r PYTHON:3.8 \
    -p frontend_asp \
    --sku F1 \
    --os-type Linux

echo "To delete all resources, run the following command:"
echo -e "${RED}az group delete --name ${RG_NAME} --no-wait --yes${NC}"
