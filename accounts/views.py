from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import AdminRole


def login_view(request):
    if request.user.is_authenticated:
        return redirect("admins:dashbord")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        selected_role = request.POST.get("role")

        if not selected_role:
            messages.error(request, "Please select a role.")
            return render(request, "accounts/admin_login.html", {"form": form})

        if form.is_valid():
            user = form.get_user()

            # 🔐 ROLE VALIDATION (CORE FEATURE)
            if user.role != selected_role:
                messages.error(
                    request,
                    f"Role mismatch. You are not registered as {selected_role.replace('_', ' ').title()}."
                )
                return render(request, "accounts/admin_login.html", {"form": form})

            # ✅ role matches → login allowed
            login(request, user)

            next_url = request.GET.get("next") or "admins:dashbord"
            return redirect(next_url)

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/admin_login.html", {"form": form})



def admin_logout(request):
    logout(request)
    return redirect("accounts:admin_login")
