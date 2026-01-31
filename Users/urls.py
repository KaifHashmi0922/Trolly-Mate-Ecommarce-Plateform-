from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'users'

urlpatterns = [

    # Home & Auth
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.cust_logout, name='logout'),
    path('guest/', views.login, name='guest'),

    # Profile
    path('cust_profile/', views.profile_view, name='cust_profile'),

    path('cust_update/', views.cust_update, name='cust_update'),
    path('cust_soft/', views.cust_soft, name='cust_soft'),

    # Cart & Order
    path('cart/', views.cart_view, name='cart'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('bynow/', views.buynow, name='bynow'),

    # Order Flow
    path('place_order/', views.place_order, name='place_order'),
    path('payment_gateway/', views.payment_gateway, name='payment_gateway'),
    path('genrate_invoice/', views.payment, name='genrate_invoice'),
    path("payment/", views.payment, name="payment"),


    # Address Management ✅
    path('show_address/', views.show_address, name='show_address'),
    path('add_address/', views.add_address, name='add_address'),

    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),

    # Password & OTP
    path('change_password/', views.change_password, name='change_password'),
    path('forget_pass_email/', views.forget_password_email, name='forget_pass_email'),
    path('forget_pass_phone/', views.forget_password_phone, name='forget_pass_phone'),
    path('email_varify/', views.email_otp_varify, name='email_varify'),
    path('phone_varify/', views.phone_otp_varify, name='phone_varify'),

    # Search
    path('query/', views.query, name='query'),

    # Misc
    path('cons/', views.construct, name='cons'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
