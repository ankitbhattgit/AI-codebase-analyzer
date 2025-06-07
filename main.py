import os
from dotenv import load_dotenv
from code_loader import load_files
from llm_analyzer import analyze_files, save_results

# Load env variables
load_dotenv()

# Define paths
PROJECT_DIR = os.getenv("CODEBASE_PATH", "SakilaProject-master")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "output/analysis.json")

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def main():

    print(f"Loading code files from: {PROJECT_DIR}")
    code_files = load_files(PROJECT_DIR)

    if not code_files:
        print("No files found in the directory.")
        return

    print(f"{len(code_files)} Files loaded. Sending to LLM for analysis...")
    analysis_results = analyze_files(code_files)
    print(f"Analysis completed. Saving results to: {OUTPUT_FILE}")
    save_results(analysis_results, OUTPUT_FILE)
    print("Output saved successfully.")


if __name__ == "__main__":
    main()