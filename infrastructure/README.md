# Code-to-docs

This stack provides a shared Large Language Model (LLM) for use within each environment.

# Deploy

```BASH
# Initialize Terraform
terraform init
# Plan the deployment
terraform plan -out=tfplan
# Apply the deployment
terraform apply tfplan
```

Enable key access:

```
az resource update \
    --resource-group rg-shrabanidutta1-3864_ai \
    --name code-to-docs-openai-swedencentral \
    --resource-type "Microsoft.CognitiveServices/accounts" \
    --set properties.disableLocalAuth=false
``````