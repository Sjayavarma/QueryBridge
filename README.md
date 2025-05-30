# QueryBridge
NL2SQL Assistant using Gemini Pro API


# GenDB – Natural Language to SQL Assistant (Powered by Gemini Pro)

## 📄 Project Overview
GenDB is an AI-powered web application that allows users to query databases using **natural language**, without needing to know SQL. It converts questions into SQL queries using Google's **Gemini Pro API**, executes them on a real database, and shows the results in a clean user interface.

---

## 🚀 Features
- ✨ Natural Language to SQL conversion using Gemini Pro
- 🔗 Works with both SQLite and PostgreSQL
- 📊 Visual results displayed instantly
- 💳 Secure and isolated environment (via virtualenv)
- ✨ Dark-themed, responsive Streamlit UI

---

## 📈 Use Case Examples
| Question                                | Output                                       |
|-----------------------------------------|----------------------------------------------|
| "List all employees older than 30"      | Table of matching employee records           |
| "What offers are available on snacks?"  | Discounts from the product_offers database   |
| "Show emails of employees in HR dept"   | Filtered employee contact data               |

---

## 📁 Project Structure
```
GenDB/
├── GenDB.py               # Main Streamlit application
├── offer db.py            # Creates product_offers.db
├── company.py             # Creates company.db
├── product_offers.db      # Sample SQLite database
├── company.db             # Another sample database
├── SECURITY.md            # Security policy (optional)
├── venv/                  # Virtual environment (optional)
```

---

## 🌐 Tech Stack
- **Frontend**: Streamlit
- **Language Model**: Gemini Pro API
- **Databases**: SQLite, PostgreSQL
- **Backend**: Python, SQLite3, SQLAlchemy
- **Other**: Pandas, Google GenerativeAI SDK

---

## ⚡ How It Works
1. User selects a database (SQLite/PostgreSQL)
2. GenDB extracts and formats the DB schema
3. User types a natural language query
4. Schema + question sent to Gemini Pro
5. Gemini returns valid SQL
6. SQL is executed on the database
7. Results are shown in the app

---

## 🎓 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/GenDB.git
cd GenDB
```

### 2. Set Up Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
```

### 3. Install Requirements
```bash
pip install streamlit pandas sqlalchemy google-generativeai faker
```

### 4. Create Databases
```bash
python "offer db.py"
python "company.py"
```

### 5. Set Gemini API Key
Edit `GenDB.py`:
```python
genai.configure(api_key="YOUR_ACTUAL_API_KEY")
```
Get it from: https://aistudio.google.com/app/apikey

### 6. Run the App
```bash
streamlit run GenDB.py
```

---

## 🚩 Troubleshooting
- ❌ **API Error**: Check if Gemini API key is valid and set.
- ❌ **Empty results**: Likely no matching data in your database.
- ❌ **Virtualenv error**: Use CMD instead of PowerShell or allow scripts.

---

## 🌟 Credits
Developed by **Jaya Varma** as a final year project.

Powered by:
- Google Gemini Pro API
- Streamlit
- SQLite
- Python

---

## 🏑 License
MIT License - see `LICENSE` file for details.

