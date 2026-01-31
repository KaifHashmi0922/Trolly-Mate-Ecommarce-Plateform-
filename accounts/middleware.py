from django.shortcuts import redirect
from django.urls import reverse


class AdminURLProtectionMiddleware:
    """
    If user hits /admins/* without login → admin login page
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_login_url = reverse("accounts:admin_login")

        if request.path.startswith("/admins/"):
            if not request.user.is_authenticated:
                return redirect(f"{admin_login_url}?next={request.path}")

        return self.get_response(request)
