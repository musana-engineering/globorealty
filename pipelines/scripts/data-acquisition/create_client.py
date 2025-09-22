from azure.ai.ml import MLClient
from azure.ai.ml.entities import WorkspaceConnection
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os, json

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

# Verify the client connection is succesful by querying the workspace
workspace_details = ml_client.workspaces.get(name=workspace_name)
print(json.dumps(workspace_details._to_dict(), indent=4))