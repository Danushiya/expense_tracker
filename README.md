# 💰 TrackMySpend - Expense Tracker 

A full-stack backend project built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Strawberry GraphQL**. The application exposes both **REST** and **GraphQL** APIs from a single FastAPI application and includes a simple frontend built with **HTML, CSS, and JavaScript**.

This project was developed as a capstone project to demonstrate REST API development, GraphQL integration, database management, testing, and frontend integration.

---

## 🚀 Features

### REST API
- CRUD operations for Categories
- CRUD operations for Expenses
- Filter expenses by:
  - Category
  - From Date
  - To Date
- Monthly expense summary
- Proper HTTP status codes
- Input validation with Pydantic
- Interactive Swagger documentation

### GraphQL API
- Query all categories
- Query expenses with filters
- Nested category and expense relationships
- Add Expense mutation
- Delete Expense mutation

### Frontend
- View all expenses
- Add new expenses
- Category dropdown loaded using GraphQL
- Monthly summary
- Responsive design
- Built using plain HTML, CSS, and JavaScript

### Testing
- REST API tests with Pytest
- GraphQL endpoint tests
- Separate test database
- FastAPI TestClient

---

## 🛠️ Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Strawberry GraphQL
- SQLite
- Pydantic
- Pytest
- HTML
- CSS
- JavaScript

---

## 📁 Project Structure

```
expense-tracker/
│
├── app/
│   ├── graphql/
│   │   └── schema.py
│   │
│   ├── routes/
│   │   ├── categories.py
│   │   └── expenses.py
│   │
│   ├── static/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_categories.py
│   ├── test_expenses.py
│   └── test_graphql.py
│
├── seed.py
├── requirements.txt
├── curl.md
├── postman_collection.json
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/expense-tracker.git
```

Move into the project

```bash
cd expense-tracker
```

Create a virtual environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🌱 Seed the Database

Populate the database with sample categories and expenses.

```bash
python seed.py
```

---

## ▶️ Run the Application

```bash
fastapi dev app/main.py
```

Server runs at

```
http://127.0.0.1:8000
```

---

## 📖 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 🔗 GraphQL Playground

```
http://127.0.0.1:8000/graphql
```

---

## 🖥️ Frontend

Open in your browser

```
http://127.0.0.1:8000
```

The frontend allows you to:

- View expenses
- Add new expenses
- View monthly summaries
- Load categories using GraphQL

---

## 📬 REST Endpoints

### Categories

| Method | Endpoint |
|---------|----------|
| GET | /categories |
| GET | /categories/{id} |
| POST | /categories |
| PUT | /categories/{id} |
| DELETE | /categories/{id} |

### Expenses

| Method | Endpoint |
|---------|----------|
| GET | /expenses |
| GET | /expenses/{id} |
| POST | /expenses |
| PUT | /expenses/{id} |
| DELETE | /expenses/{id} |
| GET | /expenses/summary?month=YYYY-MM |

---

## 🔷 GraphQL Operations

### Queries

- categories
- expenses

### Mutations

- addExpense
- deleteExpense

---

## ✅ Running Tests

Run all tests

```bash
python -m pytest
```

Example output

```
15 passed
```

---

## 📮 Postman Collection

Import the included Postman collection to test every REST endpoint.

---

## 💻 cURL Examples

The project includes a `curl.md` file containing sample cURL commands for:

- Create Expense
- Get Expense
- Update Expense
- Delete Expense

---

## 📷 Screenshots

### Home Page

> Add your project screenshot here.

```
assets/home.png
```

### Swagger UI

> Add Swagger screenshot here.

```
assets/swagger.png
```

### GraphQL Playground

> Add GraphQL screenshot here.

```
assets/graphql.png
```

---

## 📚 Learning Outcomes

This project demonstrates:

- REST API design
- GraphQL API development
- FastAPI dependency injection
- SQLAlchemy ORM
- Database relationships
- Pydantic validation
- CRUD operations
- Filtering and query parameters
- Automated testing with Pytest
- GraphQL queries and mutations
- Frontend integration using Fetch API
- Responsive web design

---

## 👩‍💻 Author

**Danushiya**

GitHub: https://github.com/Danushiya

LinkedIn: https://www.linkedin.com/in/danushiya

---

## 📄 License

This project was created for learning purposes.
