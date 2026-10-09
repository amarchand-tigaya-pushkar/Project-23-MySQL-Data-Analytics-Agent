# 📊 MySQL Data Analytics Agent

An AI-powered business analytics application that converts natural-language questions into SQL queries, executes validated read-only queries against MySQL, and presents business insights through a Streamlit dashboard powered by a locally running Ollama model.

## ✨ Features

- 🤖 Natural-language business question answering
- 🧠 SQL generation using Ollama and Llama 3.2 (3B)
- 🗄️ MySQL database integration
- 🔐 SQL validation and security guardrails
- 🛡️ Dedicated MySQL read-only account
- 📈 Interactive Streamlit dashboard
- 💰 KPI cards with Indian currency formatting
- 📊 Data tables and charts
- 💡 Business insight generation
- ✅ Numeric result validation
- 🌙 Professional dark-theme interface
- 🖥️ Local AI execution without requiring OpenAI API credits

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| MySQL | Business database |
| Ollama | Local model runtime |
| Llama 3.2 (3B) | SQL generation |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| mysql-connector-python | MySQL connectivity |
| python-dotenv | Environment configuration |

## 📁 Project Structure

```text
Project-23-MySQL-Data-Analytics-Agent/
├── analytics_agent.py
├── dashboard.py
├── dashboard_backup.py
├── database.py
├── insight_generator.py
├── query_tool.py
├── schema_tool.py
├── sql_generator.py
├── sql_guardrail.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

`dashboard_backup.py` is a local backup and does not need to be uploaded to GitHub.

## ⚙️ Prerequisites

- Python 3.11 or a compatible Python version
- MySQL Server
- Ollama
- Git

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/amarchand-tigaya-pushkar/Project-23-MySQL-Data-Analytics-Agent.git
cd Project-23-MySQL-Data-Analytics-Agent
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Install and start Ollama

Download Ollama from https://ollama.com

Pull the required model:

```powershell
ollama pull llama3.2:3b
```

Ensure Ollama is running before starting the application.

### 5. Configure MySQL

Create and configure the MySQL database `business_analytics_db` with the required tables:

- `customers`
- `products`
- `sales`

Create a dedicated MySQL user with SELECT-only permissions for this database.

Copy `.env.example` to `.env` and configure the credentials locally. Use the exact environment variable names expected by `database.py`.

**Never commit `.env`, database passwords, or API keys to GitHub.**

### 6. Run the Streamlit dashboard

```powershell
python -m streamlit run dashboard.py
```

Open the local URL printed in the terminal, usually:

```text
http://localhost:8501
```

### 7. Run the command-line agent

```powershell
python analytics_agent.py
```

## 💬 Example Questions

Try asking:

- What is the total revenue?
- Which product generated the highest revenue?
- Who is the top customer by revenue?
- Which city generated the highest revenue?
- Which product sold the highest quantity?
- Show the top five customers by revenue.

## 📊 Sample Dataset Results

The following results were verified against the project's sample dataset.

| Business Metric | Sample Result |
|---|---:|
| Total revenue | ₹5,30,000 |
| Highest-revenue product | Laptop — ₹2,60,000 |
| Top customer | Rahul Sharma — ₹1,90,000 |
| Highest-revenue city | Jaipur — ₹1,90,000 |
| Highest-quantity product | Headphones — 9 units |

These are sample database results, not live business figures.

## 🔒 Security

- SQL is validated before query execution.
- A dedicated read-only MySQL account limits database permissions.
- Database-level SELECT-only permissions provide the primary write protection.
- Regex-based SQL guardrails are not a complete SQL parser.
- Never expose credentials in source code or public repositories.

Use the project only with databases you are authorized to access.

## 🧪 Security Tests

Run the SQL guardrail tests:

```powershell
python sql_guardrail.py
```

Run query-tool security integration tests:

```powershell
python query_tool.py
```

## 👨‍💻 Author

**AMARCHAND TIGAYA PUSHKAR**

- GitHub: https://github.com/amarchand-tigaya-pushkar
- LinkedIn: https://www.linkedin.com/in/amarchand-tigaya-pushkar

---

⭐ If you find this project useful, consider starring the repository.