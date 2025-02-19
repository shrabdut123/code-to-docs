## Infrastructure

The infrastructure is defined using Terraform and includes the following main components:

- **Resource Group**: Defined in [azure.tf](infrastructure/azure.tf) as `azurerm_resource_group.ai_rg`.
- **Cognitive Account**: Defined in [azure.tf](infrastructure/azure.tf) as `azurerm_cognitive_account.ai_cogacc`.
- **Cognitive Deployments**: Defined in [azure.tf](infrastructure/azure.tf) as `azurerm_cognitive_deployment.code-to-docs4-8k` and `azurerm_cognitive_deployment.code-to-docs4o-mini`.

## Variables

The variables used in the Terraform configuration are defined in [variables.tf](infrastructure/variables.tf).

## Outputs

The outputs of the Terraform configuration are defined in [outputs.tf](infrastructure/outputs.tf).

## Deployment

To deploy the infrastructure, follow these steps:

1. Initialize Terraform:
    ```sh
    terraform init
    ```

2. Plan the deployment:
    ```sh
    terraform plan -out=tfplan
    ```

3. Apply the deployment:
    ```sh
    terraform apply tfplan
    ```

4. Enable key access:
    ```sh
    az resource update \
        --resource-group code-to-docs-gen \
        --name code-to-docs-gen-openai \
        --resource-type "Microsoft.CognitiveServices/accounts" \
        --set properties.disableLocalAuth=false
    ```

## Development Environment

The development environment configuration is located in the [dev](infrastructure/dev) directory, including backend configuration in [backend.hcl](infrastructure/dev/backend.hcl) and variable values in [code2docs.auto.tfvars](infrastructure/dev/code2docs.auto.tfvars).
