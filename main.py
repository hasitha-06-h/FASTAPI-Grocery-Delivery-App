from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional
import math

app = FastAPI()

# -------------------- DATA --------------------

items = [
    {"id": 1, "name": "Rice", "price": 50, "category": "Grains", "is_available": True},
    {"id": 2, "name": "Milk", "price": 30, "category": "Dairy", "is_available": True},
    {"id": 3, "name": "Apple", "price": 80, "category": "Fruits", "is_available": False},
    {"id": 4, "name": "Bread", "price": 40, "category": "Bakery", "is_available": True},
    {"id": 5, "name": "Eggs", "price": 60, "category": "Protein", "is_available": True},
    {"id": 6, "name": "Oil", "price": 120, "category": "Cooking", "is_available": True}
]

orders = []
cart = []
order_counter = 1

# -------------------- MODELS --------------------

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    address: str = Field(..., min_length=10)
    order_type: str = "delivery"


class NewItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True


class CheckoutRequest(BaseModel):
    customer_name: str
    address: str


# -------------------- HELPERS --------------------

def find_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price, quantity, order_type):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total


# -------------------- DAY 1 --------------------

@app.get("/")
def home():
    return {"message": "Welcome to Grocery Delivery App"}


@app.get("/items")
def get_items():
    return {"items": items, "total": len(items)}


@app.get("/items/summary")
def summary():
    available = [i for i in items if i["is_available"]]
    categories = list(set(i["category"] for i in items))

    return {
        "total": len(items),
        "available": len(available),
        "unavailable": len(items) - len(available),
        "categories": categories
    }


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}


# -------------------- DAY 2 + 3 --------------------

@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_item(order.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not item["is_available"]:
        raise HTTPException(status_code=400, detail="Item not available")

    total = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total": total
    }

    orders.append(new_order)
    order_counter += 1

    return new_order


@app.get("/items/filter")
def filter_items(category: Optional[str] = None,
                 max_price: Optional[int] = None,
                 is_available: Optional[bool] = None):

    result = items

    if category is not None:
        result = [i for i in result if i["category"] == category]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]

    return {"items": result, "count": len(result)}


# -------------------- DAY 4 (CRUD) --------------------

@app.post("/items")
def add_item(new_item: NewItem, response: Response):
    for item in items:
        if item["name"].lower() == new_item.name.lower():
            raise HTTPException(status_code=400, detail="Item already exists")

    item = new_item.dict()
    item["id"] = len(items) + 1
    items.append(item)

    response.status_code = 201
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int,
                price: Optional[int] = None,
                is_available: Optional[bool] = None):

    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    items.remove(item)
    return {"message": f"{item['name']} deleted"}


# -------------------- DAY 5 (CART WORKFLOW) --------------------

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)

    if not item or not item["is_available"]:
        raise HTTPException(status_code=400, detail="Item not available")

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return c

    cart.append({"item_id": item_id, "quantity": quantity})
    return {"message": "Added to cart"}


@app.get("/cart")
def view_cart():
    total = 0
    for c in cart:
        item = find_item(c["item_id"])
        total += item["price"] * c["quantity"]

    return {"cart": cart, "grand_total": total}


@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Removed from cart"}
    raise HTTPException(status_code=404, detail="Item not in cart")


@app.post("/cart/checkout")
def checkout(data: CheckoutRequest, response: Response):
    global order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    placed_orders = []
    total = 0

    for c in cart:
        item = find_item(c["item_id"])
        cost = item["price"] * c["quantity"]

        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item": item["name"],
            "quantity": c["quantity"],
            "total": cost
        }

        placed_orders.append(order)
        orders.append(order)
        total += cost
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {"orders": placed_orders, "grand_total": total}


# -------------------- DAY 6 --------------------

@app.get("/items/search")
def search(keyword: str):
    result = [
        i for i in items
        if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()
    ]

    if not result:
        return {"message": "No items found"}

    return {"results": result, "total_found": len(result)}


@app.get("/items/sort")
def sort_items(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    reverse = True if order == "desc" else False
    sorted_items = sorted(items, key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted_by": sort_by, "order": order, "items": sorted_items}


@app.get("/items/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    total = len(items)
    total_pages = math.ceil(total / limit)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": items[start:start + limit]
    }


@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    return result


@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    return sorted(orders, key=lambda x: x["total"], reverse=(order == "desc"))


@app.get("/items/browse")
def browse(keyword: Optional[str] = None,
           sort_by: str = "price",
           order: str = "asc",
           page: int = 1,
           limit: int = 4):

    result = items

    # FILTER
    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    # SORT
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # PAGINATION
    total = len(result)
    total_pages = math.ceil(total / limit)
    start = (page - 1) * limit

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "items": result[start:start + limit]
    }