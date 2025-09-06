from azure.ai.ml import MLClient, command, Input
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os, json

from azure.ai.ml.entities import (
    AzureBlobDatastore,
    AzureFileDatastore,
    AzureDataLakeGen2Datastore,
    AccountKeyConfiguration,
    Environment
)

load_dotenv()

subscription_id = os.getenv("SUBSCRIPTION_ID")
resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
workspace_name = os.getenv("WORKSPACE_NAME")

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id=subscription_id,
    resource_group_name=resource_group_name,
    workspace_name=workspace_name
)

# Test Workspace connection
workspace_details = ml_client.workspaces.get(
    name=workspace_name
)

print

"""

# If using username/password, the name/password values should be url-encoded
import urllib.parse
username = urllib.parse.quote(os.environ["SNOWFLAKEDB_USERNAME"], safe="")
password = urllib.parse.quote(os.environ["SNOWFLAKEDB_PASSWORD"], safe="")

target= "jdbc:snowflake://<myaccount>.snowflakecomputing.com/?db=<mydb>&warehouse=<mywarehouse>&role=<myrole>"
# add the Snowflake account, database, warehouse name and role name here. If no role name provided it will default to PUBLIC
name="snowflake-connection" # name of the connection
wps_connection = WorkspaceConnection(name= name,
type="snowflake",
target= target,
credentials= UsernamePasswordConfiguration(username=username, password=password)
)

ml_client.connections.create_or_update(workspace_connection=wps_connection)

"""