from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/accounts/admin_login/?next={request.path}")

        if not hasattr(request.user, "role"):
            return redirect("/accounts/admin_login/")

        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(request, "You do not have permission to access this page.")
                return redirect("admins:dashbord")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
