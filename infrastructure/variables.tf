variable "project" {
  description = "The project to deploy to."
  type        = string
  default     = "ingka-code-to-docs-dev"
}

variable "subscription_id" {
  description = "ID for the subscription in Azure"
  type        = string
  default     = "409ebb7b-4c36-44b5-9677-67be9fecb752" 
}

variable "location" {
  description = "Location to deploy to (e.g West Europe)"
  type        = string
  default     = "Sweden Central" 
}

variable "custom_subdomain_name" {
  description = "Domain prefix added to the API endpoint"
  type        = string
  default     = "code-to-docs-gen-openai" 
}
