# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    """
    Function-based login view for admins.
    Uses AuthenticationForm and renders accounts/login.html.
    """
    if request.user.is_authenticated:
        return redirect("dashbord")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next") or "dashbord"
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/admin_login.html", {"form": form})
