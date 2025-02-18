terraform {
  backend "azurerm" {  # Correct for Azure
    resource_group_name   = "code-to-docs-gen-swedencentral"
    storage_account_name  = "stshrabanidu776063308980"
  }
}