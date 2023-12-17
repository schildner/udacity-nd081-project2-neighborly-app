#!/usr/bin/env bash

# This file contains the variables used in the project.

SUFFIX="es81" # for resources that need a unique name
export RG_NAME="nd081-project-02-deploy-app-with-azure-functions-rg"
export LOCATION="eastus"

# SA naming: Only lowercase letters and numbers, 3-24 characters
# and unique across all existing storage account names in Azure!!
export STORAGE_ACCOUNT_NAME="sa${SUFFIX}"
export FUNCTION_APP_NAME="app-${SUFFIX}"

# cosmosDBAccountName needs to be lower case
export COSMOS_DB_ACCOUNT_NAME="cosmos-db-account-${SUFFIX}"
export DB_SERVER_VERSION="4.2"
export DB_NAME="db${SUFFIX}"
export COLLECTION_1="advertisements"
export COLLECTION_2="posts"

export # Frontend
export WEB_APP_NAME="frontend-${SUFFIX}"

export # Dockerize app
export ACR_REGISTRY="registry${SUFFIX}"
export AKS_CLUSTER="aks-cluster-${SUFFIX}"

export # Logic App & Event Grid
export LOGIC_APP_NAME="logic-app-${SUFFIX}"
export EVENT_GRID_TOPIC="event-grid-topic-${SUFFIX}"
