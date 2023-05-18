#!/usr/bin/env bash

source ./variables.sh

az group create -n "${RG_NAME}" -l "${LOCATION}"
az storage account create -n "${STORAGE_ACCOUNT_NAME}" --location "${LOCATION}" -g "${RG_NAME}" --sku Standard_LRS
az functionapp create \
    -n "${FUNCTION_APP_NAME}" \
    -g "${RG_NAME}" \
    --consumption-plan-location "${LOCATION}" \
    --runtime python \
    --runtime-version 3.8 \
    --functions-version 4 \
    --os-type linux \
    -s "${STORAGE_ACCOUNT_NAME}"