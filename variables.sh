#!/usr/bin/env bash

# This file contains the variables used in the project.

SUFFIX="es81" # for resources that need a unique name
RG_NAME="nd081-project2-rg"
LOCATION="eastus"
STORAGE_ACCOUNT_NAME="sa${SUFFIX}"
FUNCTION_APP_NAME="neighborlyapp-${SUFFIX}"

# cosmosDBAccountName needs to be lower case
COSMOS_DB_ACCOUNT_NAME="cosmos-db-account-${SUFFIX}"
DB_SERVER_VERSION="3.6"
DB_NAME="neighborlydb"
COLLECTION_1="advertisements"
COLLECTION_2="posts"