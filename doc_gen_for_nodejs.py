import openai
import os
import concurrent.futures  # For parallel processing
import hashlib  # For caching
import json  # For storing cache
import time

# Azure OpenAI API details
AZURE_OPENAI_ENDPOINT = "https://code-to-docs-gen-openai.openai.azure.com/"  # Replace with your endpoint
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = "code-to-docs-llm-gpt-4-8k"

if not AZURE_OPENAI_API_KEY:
    raise ValueError("Azure OpenAI API key is not set.")

# Configure OpenAI client
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_type = "azure"
openai.api_version = "2024-05-01-preview"

SRC_FOLDER = "src"
CACHE_FILE = "cache.json"

# Load cache to avoid redundant API calls
CACHE = {}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        CACHE = json.load(f)

def get_code_hash(code):
    """Generate a hash of the code for caching."""
    return hashlib.md5(code.encode()).hexdigest()

def generate_documentation(code):
    """Generate documentation using Azure OpenAI and cache results."""
    code_hash = get_code_hash(code)
    if code_hash in CACHE:
        return CACHE[code_hash]  # Return cached documentation

    prompt = f"Generate documentation for the following JavaScript/TypeScript function:\n\n```js\n{code}\n```"
    messages = [{"role": "user", "content": prompt}]

    start_time = time.time()
    try:
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=500,
            temperature=0,
            top_p=1.0,
        )
        elapsed_time = time.time() - start_time
        print(f"Model Response Time: {elapsed_time:.2f} seconds")

        documentation = response["choices"][0]["message"]["content"]
        CACHE[code_hash] = documentation  # Store in cache
        return documentation
    except Exception as e:
        print(f"Error generating documentation: {e}")
        return None

def process_file(file_path):
    """Read file, generate documentation, and update the file."""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read().strip()

    if not code:
        return None  # Skip empty files

    documentation = generate_documentation(code)
    if documentation:
        updated_code = f"/*\n{documentation}\n*/\n{code}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_code)
        print(f"Updated: {file_path}")
        return file_path
    return None

def traverse_and_update_files():
    """Traverse the directory and update JavaScript/TypeScript files using parallel processing."""
    updated_files = []

    # Find all `.js` and `.ts` files (excluding test and JSON files)
    valid_files = [
        os.path.join(dirpath, file_name)
        for dirpath, _, filenames in os.walk(SRC_FOLDER)
        for file_name in filenames
        if file_name.endswith((".js", ".ts")) and not file_name.endswith((".test.js", ".test.ts", ".json"))
    ]

    print(f"Found {len(valid_files)} JavaScript/TypeScript files to process.")

    # Use ThreadPoolExecutor for parallel API requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_file, valid_files))

    # Filter out None results
    updated_files = [file for file in results if file]

    # Save updated file list
    if updated_files:
        with open("updated_files.txt", "w", encoding="utf-8") as f:
            f.writelines("\n".join(updated_files))

    # Save cache
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(CACHE, f)

    return updated_files

if __name__ == "__main__":
    print("Starting documentation generation...")
    updated_files = traverse_and_update_files()
    print(f"Updated {len(updated_files)} files.") if updated_files else print("No files updated.")