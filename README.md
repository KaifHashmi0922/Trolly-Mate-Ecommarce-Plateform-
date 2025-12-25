# 🛒 Trolley Mate - Full-Stack E-Commerce Platform

**Complete Django e-commerce solution** with **admin dashboard**, **customer frontend**, **shopping cart**, **analytics**, and **inventory management**. Production-ready with stock alerts, order processing, and data visualization!

[![E-Commerce Demo](https://via.placeholder.com/1200x600/2563eb/ffffff?text=Trolley+Mate)](http://localhost:8000)

## ✨ Key Features

- **🛒 Shopping Cart** - Session-based cart with add/remove/update
- **📦 Inventory Management** - Real-time stock tracking & low stock alerts (<10)
- **📊 Advanced Analytics** - 7+ charts (Matplotlib/Seaborn) + 95+ metrics
- **👥 Dual Interface** - Admin panel + Customer frontend
- **💳 Checkout Flow** - Cart → Checkout → Order confirmation
- **📧 Email Notifications** - Order confirmations & stock alerts
- **🔍 Search & Filters** - Products, companies, categories
- **📱 Fully Responsive** - Bootstrap 5 mobile-first design

## 🛠️ Tech Stack

| Backend | Frontend | Database | Analytics | Tools |
|---------|----------|----------|-----------|-------|
| Django 5.2 | Bootstrap 5 | SQLite/MySQL | Pandas, NumPy | Custom Filters |
| DRF 3.16 | HTML5/CSS3/JS | PostgreSQL ready | Matplotlib | Pillow (images) |
| django-cors-headers | jQuery | MongoDB ready | Seaborn | django-filter |

## 📁 Project Structure

shoping_Website/
├── admins/
│ ├── models.py # Products, Companys
│ ├── views.py # Dashboard, Analytics, CRUD
│ ├── admin.py # Admin interface
│ ├── urls.py # Admin routes
│ └── templates/ # Admin HTML
├── Users/
│ ├── models.py # Customer profiles
│ └── views.py # Customer frontend
├── templates/
│ ├── admins/ # Dashboard, analytics.html
│ └── cart/ # Cart, checkout templates
├── manage.py
└── db.sqlite3






## 🚀 Quick Start (Single Terminal)

1. Activate virtual environment
source venv/bin/activate # Linux/Mac

or
venv\Scripts\activate # Windows

2. Install dependencies
pip install django==4.2.0 djangorestframework==3.14.0 django-cors-headers==4.0.0 django-filter==23.5 pillow==10.1.0 pandas numpy matplotlib seaborn

3. Setup database
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser

4. Run server
py manage.py runserver








**URLs:**
- **Admin Dashboard**: http://localhost:8000/admin/
- **Customer Frontend**: http://localhost:8000/
- **Analytics**: http://localhost:8000/admins/analytics/
- **Low Stock Alerts**: http://localhost:8000/admins/low_stock/

## 🎯 Admin Workflow

1. **Login**: `/admin/` → Add Companies & Products
2. **Stock Management**: Set quantities, monitor low stock (<10)
3. **Analytics**: `/admins/analytics/` → 7 charts + real-time metrics
4. **Customers**: View customer profiles & orders
5. **Low Stock**: Automatic alerts for items <10 quantity

## 🛒 Customer Workflow

1. **Browse**: Products by company/category
2. **Add to Cart**: Dynamic cart updates (session-based)
3. **Checkout**: Review cart → Place order
4. **Order Success**: Confirmation + stock automatically decreases
5. **Profile**: Customer account management

## 📊 Analytics Dashboard Features

🔥 7 Professional Charts:
├── Revenue Trends (Line)
├── Stock Distribution (Pie)
├── Top Products (Bar)
├── Company Breakdown (Donut)
├── Category Analysis (Stacked)
├── Low Stock Alerts (Gauge)
└── Order Status (Funnel)

📈 95+ Metrics:
├── Total Revenue, Orders, Customers
├── Low/Out of Stock Items
├── Top Companies/Products
├── Average Order Value
├── Stock Turnover Rate
└── Growth Indicators





## 🔧 Key Functions

Auto Stock Decrease on Purchase
def checkout(request):
cart_items = request.session.get('cart', {})
for item in cart_items:
product = Products.objects.get(id=item['id'])
product.quantity -= item['quantity']
product.save()

Low Stock Alert (<10)
LOW_STOCK_THRESHOLD = 10
low_stock = Products.objects.filter(quantity__lt=LOW_STOCK_THRESHOLD)

text

## 📋 Admin Models

| Model | Key Fields | Features |
|-------|------------|----------|
| **Companys** | name, category, image | Brands/Suppliers |
| **Products** | name, price, quantity, company | Inventory tracking |
| **Customer** | name, email, phone, address | User profiles |
| **Orders** | products, total, status | Order management |

## 🎨 Customization

Change primary color (CSS)
--primary-color: #2563eb → Your brand color

Database switch
DATABASES['default'] = { 'ENGINE': 'django.db.backends.postgresql' }

Email setup (settings.py)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

text

## 🚀 Production Deployment

1. requirements.txt (pip freeze > requirements.txt)
2. Collect static files
py manage.py collectstatic

3. Environment variables
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

4. Deploy: Heroku, Railway, PythonAnywhere, DigitalOcean
text

## 📈 Demo Metrics (Sample Data)

| Metric | Value |
|--------|-------|
| Total Products | 150+ |
| Active Companies | 25+ |
| Low Stock Items | 8 (<10) |
| Total Orders | 245 |
| Avg Order Value | ₹1,250 |
| Revenue YTD | ₹3,06,250 |

---

**Built for** TCS, Microsoft, Google interviews & freelance projects! 🚀

**👨‍💻 Recent BCA Graduate** | **Django Full-Stack Developer** | Delhi, India