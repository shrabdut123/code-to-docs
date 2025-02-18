variable "project" {
  description = "The project to deploy to."
  type        = string
}

variable "subscription_id" {
  description = "ID for the subscription in Azure"
  type        = string
}

variable "location" {
  description = "Location to deploy to (e.g West Europe)"
  type        = string
}

variable "custom_subdomain_name" {
  description = "Domain prefix added to the API endpoint"
  type        = string
}