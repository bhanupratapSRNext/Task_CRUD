# Task Management API

A simple **Flask + SQLAlchemy** based Task Management REST API with authentication, CRUD operations, filtering, and validation.

---

## 📌 Features
- User authentication 
- Create, view, update, delete tasks
- Data validation for due dates, title, and enums

---

## 🛠️ Tech Stack
- **Backend:** Python 3.x, Flask, Flask-SQLAlchemy
- **Database:** SQLite (default) or PostgreSQL/MySQL
- **Environment:** `.env` for config variables

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/bhanupratapSRNext/Task_CRUD.git
cd task-api

2️⃣ Create Virtual Environment
python -m venv env
source env/bin/activate     # Mac/Linux
env\Scripts\activate        # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables
Create a .env file in the project root:
API_VERSION=v1


6️⃣ Run the Server
python app.py

API will be available at:

http://127.0.0.1:5000/v1
📡 API Endpoints

🔹 Register
POST /v1/register

json
{
  "username": "john",
  "password": "mypassword"
}
🔹 Login
POST /v1/login
json
{
  "username": "john",
  "password": "mypassword"
}

🔹 Create Task
POST /v1/tasks

json
{
  "title": "Complete Python project",
  "description": "Finish Flask API module",
  "due_date": "2025-08-20",
  "status": "todo",
  "priority": "high"
}

🔹 Get Task by ID
GET /v1/tasks/<id>

🔹 Update Task
PATCH /v1/tasks/<id>

json
{
  "status": "done",
  "priority": "low"
}

🔹 Delete Task
DELETE /v1/tasks/1
