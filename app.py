import streamlit as st
import pandas as pd
import sqlite3
import tempfile
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ------------------ UI ------------------
st.set_page_config(page_title="AI Text-to-SQL (Live)", layout="centered")
st.title("AI-Powered Text-to-SQL — Upload Excel")
st.caption("Upload your Excel file and ask questions in plain English.")

# ------------------ LLM (OpenAI - Cloud) ------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ------------------ File Upload ------------------
uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type=["xlsx"])

if not uploaded_file:
    st.info("⬆️ Upload an Excel file to begin.")
    st.stop()

# ------------------ Load Excel ------------------
df = pd.read_excel(uploaded_file)

st.subheader("Preview of uploaded data")
st.dataframe(df.head(10), use_container_width=True)

# ------------------ Save to temp SQLite ------------------
tmp_db = os.path.join(tempfile.gettempdir(), "user_data.db")
TABLE_NAME = "user_data"

with sqlite3.connect(tmp_db) as conn:
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

# ------------------ Helpers ------------------
def get_columns_only(db_path, table_name):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name});")
        cols = [row[1] for row in cur.fetchall()]
    return cols

columns_only = get_columns_only(tmp_db, TABLE_NAME)
schema_text = f"Table {TABLE_NAME} has columns: {', '.join(columns_only)}"

# ------------------ Prompt (SQLite-safe) ------------------
prompt = ChatPromptTemplate.from_template("""
You are a senior data analyst and SQL expert working with SQLite.

Given this table schema:
{schema}

Write a correct SQLite SQL query to answer the user's question.

Rules:
- Use ONLY SQLite-compatible SQL
- Use only the columns listed above
- Prefer explicit column names over SELECT *
- Use GROUP BY for aggregations when needed
- Do NOT perform destructive operations (no DROP, DELETE, UPDATE, INSERT)
- Do NOT wrap the SQL in markdown or code blocks
- Return ONLY the SQL query, no explanation

Question:
{question}
""")

chain = prompt | llm | StrOutputParser()

# ------------------ Sidebar (Only column names) ------------------
st.sidebar.header("Available Fields")
for col in columns_only:
    st.sidebar.write(f"- {col}")

# ------------------ App ------------------
st.divider()
question = st.text_input("Ask a question about your uploaded data:")

if question:
    st.subheader("Generated SQL")
    sql_query = chain.invoke({"schema": schema_text, "question": question}).strip()

    # Clean markdown fences just in case
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    st.code(sql_query, language="sql")

    # Safety: block destructive SQL
    blocked = ["drop ", "delete ", "update ", "insert "]
    if any(b in sql_query.lower() for b in blocked):
        st.error("❌ Destructive queries are not allowed.")
        st.stop()

    try:
        with sqlite3.connect(tmp_db) as conn:
            cur = conn.cursor()
            cur.execute(sql_query)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()

        df_result = pd.DataFrame(rows, columns=cols)
        df_result.index = range(1, len(df_result) + 1)

        st.subheader("Result")
        st.dataframe(df_result, use_container_width=True)

    except Exception as e:
        st.error("❌ Query failed. Try rephrasing your question.")
        st.caption(f"Debug: {e}")

# ------------------ Example Questions ------------------
with st.expander("Example questions you can try"):
    st.write("- Show first 5 rows from user_data")
    st.write("- How many rows are in user_data?")
