from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from create_client import ml_client
from dotenv import load_dotenv
import os, mltable
from mltable import MLTableHeaders, MLTableFileEncoding, DataType
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# Connect to the AzureML workspace
subscription_id = os.getenv("SUBSCRIPTION_ID")
resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
workspace_name = os.getenv("WORKSPACE_NAME")
datastore_name = "rawdata"

load_dotenv()

path = f"azureml://subscriptions/{subscription_id}/resourcegroups/{resource_group_name}/workspaces/{workspace_name}/datastores/{datastore_name}/paths/house_data.csv"

# create an MLTable from the data files
tbl = mltable.from_delimited_files(
    paths=[{"file": path}],
    delimiter=",",
    header=MLTableHeaders.all_files_same_headers,
    infer_column_types=True,
    include_path_column=False,
    encoding=MLTableFileEncoding.utf8,
)

# show the first few records
print(tbl.show())

# save the data loading steps in an MLTable file
mltable_folder = "./mtable"
tbl.save(mltable_folder)

# Define the Data asset object
dataset = Data(
    path=mltable_folder,
    type=AssetTypes.MLTABLE,
    description="House Data - Raw",
    name="raw_house_data",
    version="1",
)

# Create the data asset in the workspace
ml_client.data.create_or_update(dataset)