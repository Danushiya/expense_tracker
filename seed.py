from datetime import date

from app.database import SessionLocal, engine, Base
from app.models import Category, Expense

# Create tables if they don't already exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Prevent duplicate seeding
if db.query(Category).first():
    print("Database already contains data. Seed skipped.")
    db.close()
    exit()

# Create categories
food = Category(name="Food")
transport = Category(name="Transport")
rent = Category(name="Rent")
fun = Category(name="Fun")
shopping = Category(name="Shopping")

categories = [food, transport, rent, fun, shopping]

db.add_all(categories)
db.commit()

# Refresh objects so they have IDs
for category in categories:
    db.refresh(category)

# Create expenses
expenses = [
    Expense(amount=250, description="Lunch", spent_on=date(2026, 3, 2), category_id=food.id),
    Expense(amount=120, description="Bus Ticket", spent_on=date(2026, 3, 4), category_id=transport.id),
    Expense(amount=12000, description="House Rent", spent_on=date(2026, 3, 5), category_id=rent.id),
    Expense(amount=600, description="Movie", spent_on=date(2026, 3, 10), category_id=fun.id),
    Expense(amount=900, description="Groceries", spent_on=date(2026, 3, 18), category_id=food.id),
    Expense(amount=1800, description="Shoes", spent_on=date(2026, 3, 22), category_id=shopping.id),

    Expense(amount=300, description="Dinner", spent_on=date(2026, 4, 3), category_id=food.id),
    Expense(amount=150, description="Train Ticket", spent_on=date(2026, 4, 5), category_id=transport.id),
    Expense(amount=12000, description="House Rent", spent_on=date(2026, 4, 5), category_id=rent.id),
    Expense(amount=500, description="Bowling", spent_on=date(2026, 4, 12), category_id=fun.id),
    Expense(amount=1400, description="Clothes", spent_on=date(2026, 4, 16), category_id=shopping.id),
    Expense(amount=1100, description="Supermarket", spent_on=date(2026, 4, 25), category_id=food.id),
]

db.add_all(expenses)
db.commit()

db.close()

print("Database seeded successfully!")