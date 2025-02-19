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
    resource_group_name   = "code-to-docs-gen"
    storage_account_name  = "codetodocsstorage"
    container_name        = "codetodocscontainer"
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