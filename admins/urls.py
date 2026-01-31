from django.urls import path
from admins import views

app_name = 'admins'

urlpatterns = [
    # Dashboard & Profile
    path('', views.dashbord, name='dashbord'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    
    path('profile/update/', views.admin_profile_update, name='admin_profile_update'),
    path("admin_logout/", views.admin_logout, name="admin_logout"),
    # Company Management
    path('company_add/', views.add_comp, name='company_add'),
    path('companys_view/', views.company_view, name='companys_view'),
    path('company_edit/<int:id>/', views.edit_company, name='company_edit'),
    path('company_soft/<int:id>/', views.soft_company, name='company_soft'),
    path('company_delete/<int:id>/', views.delete_company, name='company_delete'),
    
    # Product Management
    path('product_add/', views.addproduct, name='product_add'),
    path('admins_viewproduct/', views.admin_viewproduct, name='admin_viewproduct'),
    path('product_edit/<int:id>/', views.edit_product, name='product_edit'),
    path('product_soft/<int:id>/', views.soft_product, name='product_soft'),
    path('product_delete/<int:id>/', views.delete_product, name='product_delete'),
    
    # Customer Management
    path('view_custmers/', views.view_custmer, name='view_custmers'),
    
    # Search/Query
    path('query/', views.query, name='query'),
    
    # Shopping Cart & Checkout
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Low Stock Alert
    path('low-stock-alert/', views.get_low_stock_products, name='low_stock_alert'),
    
    # Analytics
    path('analytics/', views.admin_analytics, name='admin_analytics'),
]