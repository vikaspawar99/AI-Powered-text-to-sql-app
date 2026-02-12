Turn plain-English questions into SQL queries on your Excel data — instantly.
Upload any .xlsx file and ask questions like “Sum of Total_Sales by City” to get results in a clean table. Built with Streamlit + Groq LLM.

✨ Features

📁 Upload Excel (.xlsx) — bring your own data

🧠 Natural Language → SQL — powered by Groq LLM

🗃️ SQLite backend — fast, lightweight querying

📋 Schema-aware prompts — reduces SQL errors

🔎 Column names in sidebar — helps users ask correct questions

🧼 Safe SQL guardrails — blocks destructive queries

🌐 Deployed on Streamlit Cloud — shareable live app

🧰 Tech Stack

Frontend: Streamlit

LLM: Groq (Llama 3.1)

Backend: SQLite

Data: Pandas

Orchestration: LangChain

🖼️ Demo

Live App: (Add your Streamlit URL here)

Example questions you can try:

Show first 5 rows from user_data

Sum of Total_Sales by City

How many rows are in user_data?

🏗️ How It Works

User uploads an Excel file

App loads it into a temporary SQLite database

LLM converts the natural-language question into SQLite SQL

SQL is executed safely

Results are displayed in a table

⚙️ Local Setup
# Clone repo
git clone https://github.com/<your-username>/AI-Powered-text-to-sql-app.git
cd AI-Powered-text-to-sql-app

# Create and activate venv (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install deps
pip install -r requirements.txt

# Set Groq API key (PowerShell)
setx GROQ_API_KEY "gsk_your_key_here"

# Run app
python -m streamlit run app.py

🌐 Deployment (Streamlit Cloud)

Push code to GitHub

Create app on Streamlit Cloud

Add secret:

GROQ_API_KEY = "gsk_your_key_here"


Reboot app

🔐 Security Notes

API keys are stored using Streamlit Secrets (not in code)

Destructive SQL commands are blocked

Uploaded files are processed in-memory (no permanent storage)

⚠️ Limitations

LLM-generated SQL may be imperfect for complex queries

Column names must match the schema shown in the sidebar

Large Excel files may slow down the app

🛣️ Future Improvements

CSV export of query results

Query history / saved questions

Charts & visualizations

User authentication

Support for CSV + Google Sheets

👨‍💻 Author

Built by Vicky
If you liked this project, ⭐ the repo!
