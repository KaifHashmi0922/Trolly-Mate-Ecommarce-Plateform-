graph TB
    A[👤 Customer] --> B[Bootstrap Frontend]
    B --> C[JavaScript AJAX]
    C --> D[Django Views]
    D --> E[Auth Middleware]
    E --> F[MySQL Database]
    
    G[👨‍💼 Admin] --> H[Analytics Dashboard]
    H --> I[Matplotlib Charts]
    I --> F
    
    style A fill:#e1f5fe
    style G fill:#f3e5f5


    sequenceDiagram
    C->>+F: Add to Cart → Session Storage
    C->>+F: Checkout → Order Creation
    F->>+DB: INSERT orders + UPDATE product.quantity
    Note over C,DB: Auto Stock Deduction
    DB->>-F: Success
    F->>-C: Order Confirmed


    erDiagram
    COMPANYS ||--o{ PRODUCTS : has
    CUSTOMER ||--o{ ORDERS : places
    ORDERS ||--o{ ORDERITEMS : includes
    
    PRODUCTS {
        int id PK
        varchar name
        decimal price
        int quantity
        int company_id FK
    }
    
    ORDERS {
        int id PK
        decimal total
        varchar status
        int customer_id FK
    }



    trolley_mate/
├── manage.py
├── admins/          # 🛠️ Admin Dashboard
│   ├── models.py    # Products, Companies
│   ├── views.py     # Analytics, CRUD
│   └── templates/
├── users/           # 👥 Customer Frontend
├── static/          # CSS/JS/Bootstrap
├── templates/       # HTML Templates
├── requirements.txt
└── .env


| Feature       | Admin ✅     | Customer ✅    | Tech              |
| ------------- | ----------- | ------------- | ----------------- |
| Shopping Cart | View Orders | Session-based | Django Sessions   |
| Inventory     | Real-time   | Stock Display | MySQL Triggers    |
| Analytics     | 7 Charts    | Order History | Pandas/Matplotlib |
| Low Stock     | Alerts <10  | N/A           | Custom Manager    |
| Search/Filter | Advanced    | Category      | django-filter     |
| Responsive    | Bootstrap 5 | Mobile-first  | CSS Grid          |



git clone https://github.com/yourusername/trolley-mate.git
cd trolley-mate
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver


URLs:

🛒 Store: http://localhost:8000

👨‍💼 Admin: http://localhost:8000/admin

📊 Analytics: http://localhost:8000/admins/analytics/



| Method | Endpoint        | Auth     | Description         |
| ------ | --------------- | -------- | ------------------- |
| GET    | /api/products/  | Optional | Filterable products |
| POST   | /api/cart/add/  | Session  | Add to cart         |
| POST   | /api/checkout/  | Required | Process order       |
| GET    | /api/analytics/ | Admin    | Dashboard metrics   |


| Category       | Key Metrics      | Sample    |
| -------------- | ---------------- | --------- |
| 💰 Revenue     | Total/YTD/AOV    | ₹3,06,250 |
| 📦 Inventory   | Low/Out of Stock | 8/150     |
| 📋 Orders      | Total/Pending    | 245       |
| 👥 Customers   | Active/New       | 127       |
| 📈 Performance | Conversion Rate  | 3.2%      |



