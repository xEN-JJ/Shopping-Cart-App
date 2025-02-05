# Imports
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# Get the absolute path of the backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend directory
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))  # Adjusted frontend path

# Ensure the frontend directory exists
if not os.path.exists(FRONTEND_DIR):
    raise RuntimeError(f"Frontend directory '{FRONTEND_DIR}' does not exist. Check your project structure.")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=FRONTEND_DIR)

# Define data models
class Item(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class Order(BaseModel):
    item_id: int
    quantity: int

# Mock database
items = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
    {"id": 2, "name": "Phone", "price": 499.99, "stock": 20},
    {"id": 3, "name": "Headphones", "price": 149.99, "stock": 15},
    {"id": 4, "name": "Mouse", "price": 99.99, "stock": 17},
]

orders = []

# Home page route
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items, "orders": orders})

# View all items page
@app.get("/view-items", response_class=HTMLResponse)
async def view_items(request: Request):
    return templates.TemplateResponse("ViewItems.html", {"request": request, "items": items})

# View all orders page
@app.get("/purchase-orders", response_class=HTMLResponse)
async def purchase_orders(request: Request):
    return templates.TemplateResponse("PurchaseOrders.html", {"request": request, "orders": orders})

# API to get all items
@app.get("/items", response_model=List[Item])
async def get_items():
    return items

# API to get a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# API to create an order
@app.post("/purchase-orders")
async def create_order(order: Order):
    item = next((i for i in items if i["id"] == order.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item["stock"] < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    item["stock"] -= order.quantity
    orders.append({"item_id": order.item_id, "quantity": order.quantity})
    return {"message": "Order created successfully", "order": order}

# API to get all orders
@app.get("/orders")
async def get_orders():
    return {"orders": orders}