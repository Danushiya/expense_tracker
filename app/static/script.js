const API = "http://127.0.0.1:8000";

const expenseTable = document.getElementById("expense-table");
const categorySelect = document.getElementById("category");
const expenseForm = document.getElementById("expense-form");
const summaryDiv = document.getElementById("summary");
const summaryButton = document.getElementById("summary-btn");

loadCategories();
loadExpenses();

async function loadCategories() {
    const query = `
    {
        categories {
            id
            name
        }
    }
    `;

    const response = await fetch(`${API}/graphql`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            query,
        }),
    });

    const data = await response.json();

    categorySelect.innerHTML =
        '<option value="">Select Category</option>';

    data.data.categories.forEach(category => {

        const option = document.createElement("option");

        option.value = category.id;
        option.textContent = category.name;

        categorySelect.appendChild(option);

    });
}

async function loadExpenses() {

    const response = await fetch(`${API}/expenses`);

    const expenses = await response.json();

    expenseTable.innerHTML = "";

    expenses.forEach(expense => {

        expenseTable.innerHTML += `
        <tr>
            <td>${expense.amount}</td>
            <td>${expense.description}</td>
            <td>${expense.spent_on}</td>
            <td>${expense.category_name}</td>
        </tr>
        `;

    });

}

expenseForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const expense = {

            amount: Number(
                document.getElementById("amount").value
            ),

            description:
                document.getElementById("description").value,

            spent_on:
                document.getElementById("spent_on").value,

            category_id: Number(
                categorySelect.value
            ),
        };

        await fetch(`${API}/expenses`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(expense),

        });

        expenseForm.reset();

        loadExpenses();

    }
);

summaryButton.addEventListener(
    "click",
    async function () {

        const month = document
            .getElementById("month")
            .value;

        if (!month) {
            alert("Select a month.");
            return;
        }

        const response = await fetch(
            `${API}/expenses/summary?month=${month}`
        );

        const summary = await response.json();

        summaryDiv.innerHTML = "";

        summaryDiv.innerHTML += `
        <h3>Total Spend: ₹${summary.total_spend}</h3>
        `;

        summary.categories.forEach(category => {

            summaryDiv.innerHTML += `
            <p>
                ${category.category}
                :
                ₹${category.total}
                (${category.percentage}%)
            </p>
            `;

        });

    }
);