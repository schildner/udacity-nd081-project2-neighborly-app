# udacity-nd081-project2-neighborly-app

## Project 2: Neighborly App

See the full [project instructions](https://github.com/udacity/nd081-c2-Building-and-deploying-cloud-native-applications-from-scratch-project-starter/blob/c906b6f7a4842dfc409575740f69ebd3e0819d55/README.md) in Udacity's public project repo.

### Project Overview

1. Create function app
2. Deploy client-side web application
3. Dockerfize function app and deploy to AKS
4. Event Hubs and Logic App
5. Screenshot and Deliverables

### Getting Started

Clone the starter code.

```bash
git clone https://github.com/udacity/nd081-c2-Building-and-deploying-cloud-native-applications-from-scratch-project-starter.git
```

Run the script to

- Create a Function App
- Create a Cosmos DB Account
- Create a Cosmos Database with 2 Collections
- Import sample data into the DB Collections

```bash
./setup_project.sh
```

Then activate venv and install dependencies.

```bash
cd NeighborlyAPI
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

And deploy functions to the Function App in azure.

```bash
func azure functionapp publish neighborlyapp-es81 --python --build remote
```

### Deploy client-side web application

TODO...