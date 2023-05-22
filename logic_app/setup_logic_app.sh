#!/usr/bin/env bash

az create logicapp \
    --name "${LOGIC_APP_NAME}" \
    --resource-group "${RG_NAME}" \
    --location "${LOCATION}" \
    --state Enabled \
    --definition "@${LOGIC_APP_DEFINITION_FILE}" \
    --parameters "@${LOGIC_APP_PARAMETERS_FILE}"