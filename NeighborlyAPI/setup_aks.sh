#!/usr/bin/env bash

# shellcheck disable=SC1091
source ./variables.sh

# Create Azure Container Registry
az acr create \
    -n "${ACR_REGISTRY}" \
    -g "${RG_NAME}" \
    --sku Basic

echo "When prompted for username/password go to:"
echo " Azure Portal > ACR > Settings > Access Keys > enable Admin User"
echo " and then copy paste login details."
docker login "${ACR_REGISTRY}.azurecr.io"

# Create AKS cluster
az aks create \
    -g "${RG_NAME}" \
    -n "${AKS_CLUSTER}" \
    --attach-acr "${ACR_REGISTRY}" \
    --node-count 2 \
    --enable-addons monitoring \
    --generate-ssh-keys

# Get credentials for AKS.
az aks get-credentials \
    -n "${AKS_CLUSTER}" \
    -g "${RG_NAME}"
