# Project 2: Neighborly App

See the full [project instructions](https://github.com/udacity/nd081-c2-Building-and-deploying-cloud-native-applications-from-scratch-project-starter/blob/c906b6f7a4842dfc409575740f69ebd3e0819d55/README.md) in Udacity's public project repo.

## Project Overview

1. Create function app
2. Deploy client-side web application
3. Dockerize function app and deploy to AKS
4. Event Hubs and Logic App
5. Screenshot and Deliverables

## Getting Started

The [starter code](https://github.com/udacity/nd081-c2-Building-and-deploying-cloud-native-applications-from-scratch-project-starter/tree/10fec75928fcffe1c94004133c3b385c73535f9a) was provided by Udacity. Minor adaptions for both Backend and Frontend were necessary in order to deploy both parts.

### Necessary code modifications

#### Frontend

- Values of `SERVER_HOST` and `APP_URL` in `settings.py` file need to match deployed webapp URL and function app URL + "/api".

#### Backend

:warning: Note that connection strings need to be updated after each (re-)deployment of the Cosmos DB Account :warning:

- Variables in API functions need the deployed db name and the db connection string(`database` and `url` vars in each `__init__.py` file)
- The `MyDbConnection` needs to be added to deployed Function App. It shall hold the db connection string.

    <details>
        <summary>There are two ways to achieve this...</summary>

  1. Azure Portal: Function App > Configuration > Application Settings > Add Application Settings
  2. Edit `local.settings.json`, then deploy the function overwriting Function App settings in Azure with local settings.

     ```bash
     # Bring the Function App settings to the local settings file.
     func azure functionapp fetch-app-settings <functionAppName>

     # Add the value "MyDbConnection" to the local.settings.json file.

     # Then upload and overwrite the Function App settings in Azure.
     func azure functionapp publish <functionAppName> \
       --build local \
       --publish-settings-only
     ```

    </details>

## Run the script to deploy

```bash
./setup_project.sh
```

1. Database

   - Create a Cosmos DB Account
   - Create a Cosmos Database with 2 Collections
   - Import sample data into the DB Collections

2. Backend

   - Create a Storage Account
   - Create an App Service Plan
   - Create a Function App
   - Deploy the Functions to the Function App

3. Frontend

   - Create a Web App
   - Deploy the Web App to the Web App

## Re-deploy the project

After further code adaptions each part can be deployed separately overwriting the running app.

### Functions :arrow_right: Function App

```bash
# If some other venv is activated, deactivate it
cd NeighborlyFrontEnd
source .venv/bin/activate

func azure functionapp publish "${FUNCTION_APP_NAME}"\
    --python \
    --build remote
```

### Frontend :arrow_right: App Service

```bash
# If some other venv is activated, deactivate it
cd NeighborlyAPI
source .venv/bin/activate

az webapp up \
    -n "${WEB_APP_NAME}" \
    -g "${RG_NAME}" \
    -r PYTHON:3.8 \
    -p frontend_asp \
    --sku F1 \
    --os-type Linux
```

## Dockerize the Function App

Run the script to set up a new Azure Container Registry and AKS Cluster.

```bash
cd NeighborlyAPI
./setup_aks.sh

# Generate Dockerfile
func init --docker-only --python

# Build the docker image
docker build -t "${ACR_REGISTRY}.azurecr.io/${FUNCTION_APP_NAME}:latest" .
```

Push the image & optionaly test it locally (typically **saves time :eyes:**)

```bash
docker run -p 7071:7071 -it "${ACR_REGISTRY}.azurecr.io/${FUNCTION_APP_NAME}:latest"
docker push "${ACR_REGISTRY}.azurecr.io/${FUNCTION_APP_NAME}:latest"
```

Then deploy the app to AKS.

```bash
func kubernetes deploy \
    --python \
    --name "${FUNCTION_APP_NAME}" \
    --registry "${ACR_REGISTRY}.azurecr.io" --dry-run > deploy.yml

# Beware!!! doesnt seem to work with event hub trigger function - temporarily deleted
# https://stackoverflow.com/questions/71901186/event-hub-triggered-azure-function-running-on-aks-with-keda-does-not-scale-out
```

## Logic App

Configured in Azure Portal as follows:

1. Create Communcation Service: Resource Group > Add > Communication Service: `cs-es81`
   - Copy the connection string from the newly created resource: Keys > Primary Connection String
2. Create Communication Email Service: Resource Group > Add > Communication Email Service: `ces-es81`
   - Provision Domains > Add Domain (Free) - You can only have one Azure subdomain per Email Communication Services!
   - Domain name auto-created: `915cc553-5a4d-4598-8a5b-ac1d2001332d.azurecomm.net`
     - Click on the domain > MailFrom addresses > Add:

       Property | Value
       --- | ---
       Display name | `Udacity Project EduBot`
       MailFrom address | `edubot-es81` @15cc553-5a4d-5a.....`

3. Create a Logic App: Resource Group > Add > Logic App: `logic-app-es81`
4. Logic App Designer

   - Trigger: When a HTTP request is received

     Property | Value
     --- | ---
     Method | `GET`
     URL (auto-generated after save) | `https://prod-36.eastus.logic.azure.com:443/workflows/3e0348e4aaef479db702cd04371eeb33/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=5dVi8Ivn_-TRSTUUoGtHgBZ7OI2xAfyeoV7ggubcP50`

   - Action: Send email (Preview)
     - :information_source: Connection: make sure it's connected to the `cs-es81` resource, paste Connection String from step 1.

       Property | Value
       --- | ---
       Subject | `Somebody triggered Logic App's Custom HTTP Request`
       To | `eduard.***@gmail.com`
       From | `edubot-es81@915cc553-5a4d-4598-8a5b-ac1d2001332d.azurecomm.net`
       Body | `Yep, the logic-app-es81's custom HTTP GET Request was triggered.`

