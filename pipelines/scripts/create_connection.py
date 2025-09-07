from azure.ai.ml import MLClient, command, Input
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration
from dotenv import load_dotenv
import os, json
from create_client import ml_client, workspace_name

load_dotenv()

# Define the connection information
import urllib.parse
snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
snowflake_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
snowflake_role = os.getenv("SNOWFLAKE_ROLE")
snowflake_db_username = os.getenv("SNOWFLAKEDB_USERNAME")
snowflake_db_password = os.getenv("SNOWFLAKEDB_PASSWORD")

snowflake_connection_string = f"jdbc:snowflake://{snowflake_account}.snowflakecomputing.com/?db={snowflake_database}&warehouse={snowflake_warehouse}&role={snowflake_role}"
connection_name = "Snowflake" 

# Create the connection
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

# Return list of connections to verify the new connection exists
verify_connection_creation = ml_client.connections.list(connection_type="snowflake")
print("\nConnection details:")
for connection in verify_connection_creation:
    print(json.dumps(connection._to_dict(), indent=4))