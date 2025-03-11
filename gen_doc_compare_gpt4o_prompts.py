import openai
import json
import os
from translations_prompts import code_snippet, prompt1_translation, prompt2_translation

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "https://code-to-docs-gen-openai.openai.azure.com/"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = "code-to-docs-llm-gpt-4-8k"

if not AZURE_OPENAI_API_KEY:
    raise ValueError("Azure OpenAI API key is not set.")

openai.api_base, openai.api_key, openai.api_type, openai.api_version = (
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, "azure", "2024-05-01-preview"
)


def compare_translations(code_snippet, prompt1_translation, prompt2_translation):
    evaluation_prompt = f"""
    You are an AI assistant that compares two natural language translations of a code snippet.

    **Code Snippet:**
    ```
    {code_snippet}
    ```

    **Translation 1 (prompt1):**
    "{prompt1_translation}"

    **Translation 2 (prompt2):**
    "{prompt2_translation}"

    Evaluate both translations on the following metrics (score 1-10):
    - **Clarity**: How easy is it to understand?
    - **Technical Accuracy**: Does it correctly describe the code?
    - **Detail**: Does it cover all relevant aspects?
    - **Readability**: Is the explanation well-structured and natural?

    Provide a JSON comparison like this:
    {{
        "copilot": {{
            "clarity": <score>,
            "technical_accuracy": <score>,
            "detail": <score>,
            "readability": <score>,
            "summary": "<brief evaluation>"
        }},
        "gpt4o": {{
            "clarity": <score>,
            "technical_accuracy": <score>,
            "detail": <score>,
            "readability": <score>,
            "summary": "<brief evaluation>"
        }},
        "comparison_summary": "<which one performed better and why>"
    }}
    """

    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,  # Your GPT-4o deployment in Azure
        messages=[
            {"role": "system", "content": "You are a strict AI translation evaluator."},
            {"role": "user", "content": evaluation_prompt}
        ],
        temperature=0.2,  # Low temperature for consistent evaluation
        max_tokens=400
    )

    return json.loads(response["choices"][0]["message"]["content"])

# Run Evaluation
evaluation_result = compare_translations(code_snippet, prompt1_translation, prompt2_translation)

# Print Output
print(json.dumps(evaluation_result, indent=2))