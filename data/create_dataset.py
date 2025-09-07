# Import Data
from azure.ai.ml.data_transfer import Database
from azure.ai.ml.entities import DataImport, Data, DataAsset, Datastore
from dotenv import load_dotenv
import os, json, mltable, pandas
from azure.core.exceptions import ResourceNotFoundError
from create_client import ml_client, workspace_name
from create_connection import connection_name
from create_datastore import raw_datastore_name

dataset_name = "raw_house_data"

# Create dataset
try:
    ml_client.data.get(name=dataset_name, version="1")
    print("Dataset '{dataset_name}' already exists")
except ResourceNotFoundError:
    print("Registering dataset")
    data_import = DataImport(
        name=dataset_name,
        source=Database(
            connection=connection_name,
            query=f"GLOBOREALTY.REAL_ESTATE.RAW"
        ),
        path=f"azureml://datastores/{raw_datastore_name}/paths/{dataset_name}",
        version="1"
    )
    ml_client.data.import_data(data_import=data_import)

# Return list of datasets to verify the new dataset exists
verify_dataset_creation = ml_client.datastores.list(include_secrets=False)

print("\nDatastore details:")
for dataset in verify_dataset_creation:
    print(json.dumps(dataset._to_dict(), indent=4))



