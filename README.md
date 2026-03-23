🛒 Grocery Delivery System API

A RESTful backend application built using FastAPI to manage grocery items, cart operations, and order processing.

This project was developed as part of my FastAPI Internship at Innomatics Research Labs.

The system demonstrates real-world backend concepts such as API design, data validation, cart workflow management, search, sorting, and pagination.



🚀 Project Highlights

✔ RESTful API development using FastAPI
✔ Structured data validation using Pydantic
✔ Cart-based workflow (Add → View → Checkout → Order)
✔ Item search and filtering functionality
✔ Sorting and pagination support
✔ Combined browsing (search + sort + pagination)
✔ Interactive API testing using Swagger UI



 🛠 Tech Stack

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Core programming language   |
| FastAPI    | Backend API framework       |
| Pydantic   | Data validation             |
| Uvicorn    | ASGI server                 |
| Swagger UI | API testing & documentation |



## 📂 Project Structure

id="n1kq7g"
grocery_fastapi/
│
├── main.py
├── README.md
├── requirements.txt
└── screenshots/




⚙️ Installation & Setup

1️⃣ Clone the Repository

```bash id="0c2m5o"
git clone https://github.com/your-username/grocery-fastapi.git
cd grocery-fastapi
```

### 2️⃣ Install Dependencies

bash id="b9i3kp"
pip install fastapi uvicorn


### 3️⃣ Run the Application

bash id="k6kz6y"
uvicorn main:app --reload

🌐 API Documentation

After running the server, open:

👉 http://127.0.0.1:8000/docs

👉 http://127.0.0.1:8000/redoc

Swagger UI provides an interactive interface to test all APIs directly.
 📌 API Endpoints

🛍️ Items

* GET /items
* GET /items/{item_id}
* POST /items
* PUT /items/{item_id}
* DELETE /items/{item_id}

🔍 Search & Filtering

* GET /items/search
* GET /items/filter
* GET /items/sort
* GET /items/page
* GET /items/browse

 🛒 Cart

* POST /cart/add
* GET /cart
* DELETE /cart/{item_id}
* POST /cart/checkout

📦 Orders

* GET /orders
* POST /orders
* GET /orders/search
* GET /orders/sort

 📊 System Summary

* GET /items/summary



 🔄 Workflow

1. Browse available grocery items
2. Add items to the cart
3. View cart details
4. Proceed to checkout
5. Orders are created successfully



📊 Example API Request

 Create Order

POST /orders

```json id="3v2i7a"
{
  "customer_name": "Hasitha",
  "item_id": 1,
  "quantity": 2,
  "address": "Visakhapatnam, Andhra Pradesh",
  "order_type": "delivery"
}
```

 Response

json id="7u8d2s"
{
  "order_id": 1,
  "customer_name": "Hasitha",
  "item": "Rice",
  "quantity": 2,
  "total": 130
}


 📚 What I Learned

Through this project, I gained practical experience in:

• Building backend APIs using FastAPI
• Designing RESTful API structures
• Implementing input validation using Pydantic
• Creating multi-step workflows (Cart → Checkout → Order)
• Adding search, sorting, and pagination features
• Testing APIs using Swagger UI



👩‍💻 Author

Hasitha Pyla
FastAPI Intern
Innomatics Research Labs



  Acknowledgment

This project was developed as part of the FastAPI Internship Program at Innomatics Research Labs, focusing on real-world backend development skills.


