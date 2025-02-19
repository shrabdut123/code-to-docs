terraform {
  backend "azurerm" {  # Correct for Azure
    resource_group_name   = "code-to-docs-gen"
    storage_account_name  = "codetodocsstorage"
  }
}