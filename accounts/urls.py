from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # /accounts/login/
    path("admin_login/", views.login_view, name="admin_login"),

    # /accounts/logout/
    path(
        "admin_logout/",
        auth_views.LogoutView.as_view(next_page="admin_login"),
        name="admin_logout",
    ),

]
