# Expense Tracker API - cURL Commands

## 1. Create an Expense

```bash
curl -X POST http://127.0.0.1:8000/expenses \
-H "Content-Type: application/json" \
-d '{
  "amount": 500,
  "description": "Lunch",
  "spent_on": "2026-03-20",
  "category_id": 1
}'
```

---

## 2. Get All Expenses

```bash
curl http://127.0.0.1:8000/expenses
```

---

## 3. Get Expense by ID

```bash
curl http://127.0.0.1:8000/expenses/1
```

---

## 4. Update Expense

```bash
curl -X PUT http://127.0.0.1:8000/expenses/1 \
-H "Content-Type: application/json" \
-d '{
  "amount": 650,
  "description": "Dinner",
  "spent_on": "2026-03-20",
  "category_id": 1
}'
```

---

## 5. Delete Expense

```bash
curl -X DELETE http://127.0.0.1:8000/expenses/1
```