# MySQL Data Analytics Agent



An AI-powered analytics agent that converts natural-language questions into SQL, queries a MySQL database, and explains business results using a local Ollama model.

## Features

- Natural-language business questions
- SQL generation with Llama 3.2 (3B)
- MySQL read-only query execution
- SQL validation and security guardrails
- Business insight generation
- Numeric result validation

## Tech Stack

- Python
- MySQL
- Ollama
- Llama 3.2 (3B)
- mysql-connector-python
- python-dotenv

## Project Files

- `analytics_agent.py` — Main agent workflow
- `database.py` — Database connection
- `schema_tool.py` — Database schema information
- `sql_generator.py` — SQL generation
- `sql_guardrail.py` — SQL validation
- `query_tool.py` — Query execution and security tests
- `insight_generator.py` — Business insight formatting
- `requirements.txt` — Python dependencies

## Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1