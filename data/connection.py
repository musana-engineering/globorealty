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

# Verify the ML Client connection is succesful by querying the workspace
workspace_details = ml_client.workspaces.get(
    name=workspace_name
)

print(json.dumps(workspace_details._to_dict(), indent=4))

import urllib.parse
username = urllib.parse.quote(os.environ["SNOWFLAKEDB_USERNAME"], safe="")
password = urllib.parse.quote(os.environ["SNOWFLAKEDB_PASSWORD"], safe="")

snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
snowflake_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
snowflake_role = os.getenv("SNOWFLAKE_ROLE")
snowflake_db_username = os.getenv("SNOWFLAKEDB_USERNAME")
snowflake_db_password = os.getenv("SNOWFLAKEDB_PASSWORD")

snowflake_connection_string = f"jdbc:snowflake://{snowflake_account}.snowflakecomputing.com/?db={snowflake_database}&warehouse={snowflake_warehouse}&role={snowflake_role}"
connection_name = "Conn-Snowflake" 

try:
    ml_client.connections.get(name=connection_name)
    print("Connection with the same name already exists")
except:
    wps_connection = WorkspaceConnection(
        name=connection_name,
        type="snowflake",
        target=snowflake_connection_string,
        credentials=UsernamePasswordConfiguration(username=snowflake_db_username, password=snowflake_db_password)
    )
    ml_client.connections.create_or_update(workspace_connection=wps_connection)
    print("Workspace connection created.")
