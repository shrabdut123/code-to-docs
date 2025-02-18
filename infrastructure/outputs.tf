output "api_url-4-8k" {
  description = "API URL for LLM queries using code-to-docs4-8k"
  value       = "${azurerm_cognitive_account.ai_cogacc.endpoint}openai/deployments/${azurerm_cognitive_deployment.code-to-docs4-8k.name}"
}

output "api_url-4o-mini" {
  description = "API URL for LLM queries using code-to-docs4o-mini"
  value       = "${azurerm_cognitive_account.ai_cogacc.endpoint}openai/deployments/${azurerm_cognitive_deployment.code-to-docs4o-mini.name}"
}

output "api_key" {
  description = "Primary API key"
  value       = azurerm_cognitive_account.ai_cogacc.primary_access_key
  sensitive   = true
}