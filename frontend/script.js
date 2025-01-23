// Base URL of the backend API
const API_BASE_URL = "http://127.0.0.1:8000"; // Replace with your actual backend URL if different

// Fetch and display all items
async function fetchItems() {
    try {
        const response = await fetch(`${API_BASE_URL}/items`);
        if (!response.ok) throw new Error("Failed to fetch items");

        const items = await response.json();
        const itemsList = document.getElementById("items-list");
        itemsList.innerHTML = ""; // Clear existing content

        items.forEach(item => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <img src="https://via.placeholder.com/150" class="card-img-top" alt="${item.name}">
                <div class="card-body">
                    <h5 class="card-title">${item.name}</h5>
                    <p class="card-text">Price: $${item.price.toFixed(2)}</p>
                    <p class="card-text">Stock: ${item.stock}</p>
                </div>
            `;
            itemsList.appendChild(card);
        });
    } catch (error) {
        console.error("Error fetching items:", error);
    }
}

// Fetch and display all orders
async function fetchOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`);
        if (!response.ok) throw new Error("Failed to fetch orders");

        const data = await response.json();
        const ordersTable = document.getElementById("orders-table");
        ordersTable.innerHTML = ""; // Clear existing content

        data.orders.forEach((order, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <th scope="row">${index + 1}</th>
                <td>${order.item_id}</td>
                <td>${order.quantity}</td>
            `;
            ordersTable.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching orders:", error);
    }
}

// Handle order form submission
async function handleOrderForm(event) {
    event.preventDefault();

    const itemId = document.getElementById("item-id").value;
    const quantity = document.getElementById("quantity").value;

    if (!itemId || !quantity) {
        alert("Please fill out all fields");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/orders`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                item_id: parseInt(itemId, 10),
                quantity: parseInt(quantity, 10)
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to create order");
        }

        alert("Order created successfully!");
        document.getElementById("order-form").reset(); // Clear form
        fetchItems(); // Refresh items to update stock
        fetchOrders(); // Refresh orders
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Event Listeners
document.getElementById("order-form").addEventListener("submit", handleOrderForm);

// Initial Data Fetch
fetchItems();
fetchOrders();