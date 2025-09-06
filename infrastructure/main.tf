locals {
  location       = "eastus2"
  infrastructure_id = "0fec8a51-9bf7-4ae3-9f7d-edfc8654c1d4"
  infrastructure_prefix = substr(local.infrastructure_id, 0, 6)
  user_object_id = "jim@musana.engineering"

  tags = {
    provisioner = "terraform"
    project     = "predictive-ai"
  }
}

resource "azurerm_resource_group" "ml" {
  name     = "rg-${local.infrastructure_prefix}"
  location = local.location
  tags     = local.tags
}

resource "azurerm_application_insights" "ml" {
  name                = "appi-${local.infrastructure_prefix}"
  location            = azurerm_resource_group.ml.location
  resource_group_name = azurerm_resource_group.ml.name
  application_type    = "web"
  tags                = local.tags

  depends_on = [azurerm_resource_group.ml]
}

resource "azurerm_key_vault" "ml" {
  name                            = "kv-${local.infrastructure_prefix}"
  location                        = azurerm_resource_group.ml.location
  resource_group_name             = azurerm_resource_group.ml.name
  tenant_id                       = data.azurerm_client_config.current.tenant_id
  sku_name                        = "standard"
  enable_rbac_authorization       = true
  enabled_for_deployment          = true
  enabled_for_template_deployment = true
  tags                            = local.tags
  depends_on                      = [azurerm_resource_group.ml]
}

resource "azurerm_storage_account" "ml" {
  name                       = "sa${local.infrastructure_prefix}"
  location                   = local.location
  resource_group_name        = azurerm_resource_group.ml.name
  account_tier               = "Standard"
  min_tls_version            = "TLS1_2"
  https_traffic_only_enabled = true
  account_replication_type   = "LRS"

  depends_on = [azurerm_resource_group.ml]
}

resource "azurerm_storage_container" "raw" {
  name                  = "rawdata"
  storage_account_id    = azurerm_storage_account.ml.id
  container_access_type = "private"

  depends_on = [azurerm_resource_group.ml]
}

resource "azurerm_storage_container" "cleaned" {
  name                  = "cleandata"
  storage_account_id    = azurerm_storage_account.ml.id
  container_access_type = "private"

  depends_on = [azurerm_resource_group.ml]
}

resource "azurerm_machine_learning_workspace" "ml" {
  name                          = "mlw-${local.infrastructure_prefix}"
  location                      = azurerm_resource_group.ml.location
  resource_group_name           = azurerm_resource_group.ml.name
  application_insights_id       = azurerm_application_insights.ml.id
  key_vault_id                  = azurerm_key_vault.ml.id
  storage_account_id            = azurerm_storage_account.ml.id
  high_business_impact          = true
  tags                          = local.tags
  friendly_name                 = "mlw-${local.infrastructure_prefix}"
  public_network_access_enabled = true
  description                   = "Machine Learning Operations"

  #  managed_network {
  #    isolation_mode = "AllowInternetOutbound"
  #  }

  identity {
    type = "SystemAssigned"
  }

  depends_on = [
    azurerm_resource_group.ml,
  azurerm_key_vault.ml]
}

resource "azurerm_role_assignment" "sa" {
  scope                = azurerm_storage_account.ml.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_machine_learning_workspace.ml.identity[0].principal_id
}

resource "azurerm_role_assignment" "kv" {
  scope                = azurerm_key_vault.ml.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_machine_learning_workspace.ml.identity[0].principal_id

}

/*
resource "azurerm_machine_learning_compute_cluster" "ml" {
  name                          = "vm-${local.infrastructure_prefix}"
  location                      = azurerm_resource_group.ml.location
  vm_priority                   = "Dedicated"
  vm_size                       = "Standard_DS11_v2"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.ml.id
  #  subnet_resource_id            = data.azurerm_subnet.ml.id

  scale_settings {
    min_node_count                       = 0
    max_node_count                       = 2
    scale_down_nodes_after_idle_duration = "PT30S" # 30 seconds
  }

  identity {
    type = "SystemAssigned"
  }

  depends_on = [azurerm_machine_learning_workspace.ml]
}

resource "azurerm_role_assignment" "cluster" {
  scope                = azurerm_machine_learning_compute_cluster.ml.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_machine_learning_compute_cluster.ml.identity[0].principal_id

  depends_on = [azurerm_machine_learning_compute_cluster.ml]
}
*/
