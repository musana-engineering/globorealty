# Import Data
from azure.ai.ml.data_transfer import Database
from azure.ai.ml.entities import DataImport, Data, DataAsset, Datastore
from azure.ai.ml.entities import AzureBlobDatastore, AccountKeyConfiguration
from dotenv import load_dotenv
import os, json
from azure.core.exceptions import ResourceNotFoundError
from create_client import ml_client, workspace_name


raw_datastore_name = "rawdata"
storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME")
storage_account_key = os.getenv("STORAGE_ACCOUNT_ACCESS_KEY")

# Create datastore for raw data
create_datastore = AzureBlobDatastore(
    name=raw_datastore_name,                      
    account_name=storage_account_name,    
    container_name=raw_datastore_name,           
    credentials=AccountKeyConfiguration(account_key=storage_account_key),
)

try:
    ml_client.datastores.get(name=raw_datastore_name)
    print(f"Datastore '{raw_datastore_name}' already exists")
except ResourceNotFoundError:
    ml_client.datastores.create_or_update(create_datastore)
    print(f"Datastore '{raw_datastore_name}' created")

# Return list of datastore to verify the new datastore exists
verify_datastore_creation = ml_client.datastores.list(include_secrets=False)

print("\nDatastore details:")
for datastore in verify_datastore_creation:
    print(json.dumps(datastore._to_dict(), indent=4))


