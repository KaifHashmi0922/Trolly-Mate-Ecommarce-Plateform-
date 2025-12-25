from django.urls import path
from admins import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'admins'

urlpatterns = [
    # Dashboard & Profile
    path('dashbord/', views.dashbord, name='dashbord'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    
    # Company Management
    path('add_company/', views.add_comp, name='add_company'),
    path('view_companys/', views.company_view, name='company_view'),
    path('edit_company/<int:id>/', views.edit_company, name='edit_company'),
    path('soft_company/<int:id>/', views.soft_company, name='soft_company'),
    path('delete_company/<int:id>/', views.delete_company, name='delete_company'),
    
    # Product Management
    path('addproduct/', views.addproduct, name='addproduct'),
    path('admins_viewproduct/', views.admin_viewproduct, name='admin_viewproduct'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('soft_product/<int:id>/', views.soft_product, name='soft_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    
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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)