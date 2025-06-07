import os
import re
import json
from tqdm import tqdm
from dotenv import load_dotenv
from typing import List, Dict, Any
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.config import RunnableConfig

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")
llm = Ollama(model=MODEL_NAME)

# Prompt templates
FILE_PROMPT_TEMPLATE = """
You are a senior software engineer. Analyze the following Java code and return structured insights in JSON format:

1. File purpose
2. Methods (name, signature, description, complexity)
3. Noteworthy aspects

### Java Code:
{code}
"""

PROJECT_PROMPT_TEMPLATE = """
You are a software architect.

Summarize the overall purpose of this Java project in 1-2 sentences in JSON format.

### Code:
{code}
"""

# Regular functions for formatting prompts and parsing JSON
def format_file_prompt_fn(code: str) -> str:
    return FILE_PROMPT_TEMPLATE.format(code=code)

def format_project_prompt_fn(code: str) -> str:
    return PROJECT_PROMPT_TEMPLATE.format(code=code)


def parse_json_fn(text: str) -> Any:
    text = text.strip()

    # Remove markdown/code block indicators like ```json or ```
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = text.rstrip("`").strip()

    # Try parsing the full cleaned text first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: try to extract brace-enclosed blocks and parse one that works
    matches = re.findall(r'\{[\s\S]*?\}', text)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    raise ValueError("No valid JSON block found in LLM response.")
    

# Wrap functions in RunnableLambda
format_file_prompt = RunnableLambda(format_file_prompt_fn)
format_project_prompt = RunnableLambda(format_project_prompt_fn)
parse_json = RunnableLambda(parse_json_fn)

# Compose chains
file_chain = format_file_prompt | llm | parse_json
project_chain = format_project_prompt | llm | parse_json

def analyze_project(code_files: List[Dict[str, str]]) -> Dict[str, Any]:
    combined_code = ""
    for file in code_files:
        if file["path"].endswith(".java") and "test" not in file["path"].lower():
            combined_code += file["content"][:1000] + "\n\n"
            if len(combined_code) > 5000:
                break

    try:
        result = project_chain.invoke(combined_code[:6000], config=RunnableConfig(tags=["project-summary"]))
        return {"projectOverview": result}
    except Exception as e:
        return {"projectOverview": {"projectPurpose": f"Failed: {str(e)}"}}

def analyze_files(code_files: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    results = [analyze_project(code_files)]

    for file in tqdm(code_files, desc="Analyzing files"):
        try:
            result = file_chain.invoke(file["content"][:3000], config=RunnableConfig(metadata={"file": file["path"]}))
            results.append({"path": file["path"], "analysis": result})
        except Exception as e:
            results.append({"path": file["path"], "error": str(e)})

    return results

def save_results(data: List[Dict[str, Any]], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)