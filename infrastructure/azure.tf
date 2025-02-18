
resource "azurerm_resource_group" "code-to-docs" {
  name     = "code-to-docs-gen"
  location = var.location
}

resource "azurerm_cognitive_account" "code-to-docs" {
  name                               = "code-to-docs-openai"
  location                           = azurerm_resource_group.code-to-docs.location
  resource_group_name                = azurerm_resource_group.code-to-docs.name
  kind                               = "OpenAI"
  custom_subdomain_name              = var.custom_subdomain_name
  local_auth_enabled                 = true
  public_network_access_enabled      = true
  outbound_network_access_restricted = false

  sku_name = "S0"

  network_acls {
    default_action = "Allow"
  }
}


resource "azurerm_cognitive_deployment" "code-to-docs4-8k" {
  name                 = "code-to-docs-llm-gpt-4-8k"
  cognitive_account_id = azurerm_cognitive_account.code-to-docs.id
  model {
    format  = "OpenAI"
    name    = "gpt-4"
    version = "0613"
  }

  scale {
    type     = "Standard"
    capacity = 20
  }
}

resource "azurerm_cognitive_deployment" "code-to-docs4o-mini" {
  name                 = "code-to-docs-llm-gpt-4o-mini"
  cognitive_account_id = azurerm_cognitive_account.code-to-docs.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o-mini"
    version = "2024-07-18"
  }

  scale {
    type     = "Standard"
    capacity = 1000
  }
}
