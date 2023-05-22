#!/usr/bin/env bash

# This file contains the variables used in the project.

SUFFIX="es81" # for resources that need a unique name
RG_NAME="nd081-project-02-deploy-app-with-azure-functions-rg"
LOCATION="eastus"

# SA naming: Only lowercase letters and numbers, 3-24 characters
# and unique across all existing storage account names in Azure!!
STORAGE_ACCOUNT_NAME="sa${SUFFIX}"
FUNCTION_APP_NAME="app-${SUFFIX}"

# cosmosDBAccountName needs to be lower case
COSMOS_DB_ACCOUNT_NAME="cosmos-db-account-${SUFFIX}"
DB_SERVER_VERSION="4.2"
DB_NAME="db${SUFFIX}"
COLLECTION_1="advertisements"
COLLECTION_2="posts"

# Frontend
WEB_APP_NAME="frontend-${SUFFIX}"

# Dockerize app
ACR_REGISTRY="registry${SUFFIX}"
AKS_CLUSTER="aks-cluster-${SUFFIX}"

# Loci App
LOGIC_APP_NAME="logic-app-${SUFFIX}"
