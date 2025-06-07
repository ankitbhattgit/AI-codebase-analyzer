# Codebase Analyzer using LLMs

## 🚀 Overview

This project is designed to analyze a given codebase using a Large Language Model (LLM), extract meaningful insights, and present them in a structured, machine-readable JSON format. It leverages LangChain, Ollama (with local LLMs like `llama3.2`), and Python's filesystem utilities to read and interpret Java source code.

## 🧩 Project Structure

```
codeAnalyzer/
├── code_loader.py         # Handles codebase traversal and file reading
├── llm_analyzer.py        # Interacts with the LLM for knowledge extraction
├── output/
│   └── analysis.json      # Final structured JSON output
├── main.py                # Entry point of the application
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

## ⚙️ Technologies Used

- **Python 3.12+**
- **LangChain** (`langchain`, `langchain_community`)
- **Ollama** (for local LLM models)

## 🧠 Methodology

### 1. Code Loading (`code_loader.py`)

- Recursively walks through the given codebase folder.
- Filters and reads only Java source files (`.java`).
- Stores the content and metadata (path, size) in memory-safe format.

### 2. Prompt Engineering & LLM Interaction (`llm_analyzer.py`)

- A well-defined prompt template is crafted to instruct the LLM on:
  - File purpose
  - Method signatures and descriptions
  - Complexity estimation
  - Noteworthy architectural or stylistic elements
- Prompts are dynamically created with file contents.
- Prompt is chunked or truncated (if needed) to comply with model context length limits.

### 3. Result Structuring

- Each LLM response is parsed into a consistent JSON format.
- Results for each file are saved into a consolidated `analysis.json` output.

## ✅ Best Practices Followed

- **Token Limit Management**: Truncated file content to avoid exceeding context window.
- **Prompt Escaping**: Escaped all literal `{}` in JSON format within the prompt template.
- **Error Handling**: Try-catch implemented around LLM calls for robust file-level resilience.
- **File Logging**: Detailed logs for each file’s analysis and any LLM failures.

## 📦 Output Structure

Example `analysis.json` entry:

```json
{
  "path": "src/main/java/com/example/MyClass.java",
  "filePurpose": "Handles user authentication logic.",
  "methods": [
    {
      "name": "authenticateUser",
      "signature": "public boolean authenticateUser(String username, String password)",
      "description": "Validates the user's credentials and returns authentication status.",
      "complexity": "Medium"
    }
  ],
  "noteworthyAspects": [
    "Uses BCrypt for password hashing",
    "Follows Singleton pattern",
    "Minimal inline documentation"
  ]
}
```

## 📌 Assumptions

- The codebase being analyzed is primarily Java-based.
- Source files are readable, non-binary, and text-encoded.
- Local LLM (e.g., via Ollama) is correctly set up and accessible at `localhost:11434`.

## ⚠️ Limitations

- Currently, only Java files are processed. Other languages would require language-specific parsing or prompts.
- No deep code parsing (e.g., AST traversal) is used—analysis is purely LLM-driven based on textual context.
- Large files may be truncated due to token limits unless further chunking and context merging are implemented.
- Accuracy depends on the LLM's code understanding capabilities.

## 🏁 Getting Started

### Prerequisites

- Python 3.12+
- [Ollama installed](https://ollama.com/) and running with a model (e.g., `ollama run llama3`)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/code-analyzer-llm.git
cd code-analyzer-llm

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Analyzer

```bash
python main.py
```

## 👨‍💻 Author

**Ankit Bhatt**

## 📄 License

This project is licensed under the MIT License.
