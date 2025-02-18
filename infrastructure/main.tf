# Azure Provider source and version being used
terraform {
  required_version = "~> 1.9.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116.0"
    }
  }

  backend "azurerm" {
    resource_group_name   = "rg-shrabanidutta1-3864_ai"
    storage_account_name  = "stshrabanidu776063308980"
    container_name        = "b850f95d-6040-4e01-9d2e-252204deadf8-azureml-blobstore"
    key                   = "container_name.tfstate"
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  subscription_id            = var.subscription_id
  skip_provider_registration = true
}

locals {
  environment = "dev"
}