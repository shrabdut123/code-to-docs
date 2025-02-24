# code-to-docs

This repository contains the infrastructure code for deploying a shared Large Language Model (LLM) using Terraform on Microsoft Azure.

Optimized Solution

💡 Break large files into smaller parts before sending them to OpenAI

Steps Taken to Fix:

✅ Splits large files into chunks (4,096 tokens per chunk)
✅ Processes each chunk separately and merges documentation
✅ Ensures model stays within context limits

This version fixes the context length issue, boosts performance, and keeps the code efficient.