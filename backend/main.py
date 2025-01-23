from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

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
]

orders = []

# API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Shopping Cart API"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    # Find the item with the given ID
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/orders")
async def create_order(order: Order):
    # Check if the item exists
    item = next((i for i in items if i["id"] == order.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if there is enough stock
    if item["stock"] < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    # Deduct stock and create order
    item["stock"] -= order.quantity
    orders.append({"item_id": order.item_id, "quantity": order.quantity})
    return {"message": "Order created successfully", "order": order}

@app.get("/orders")
async def get_orders():
    return {"orders": orders}