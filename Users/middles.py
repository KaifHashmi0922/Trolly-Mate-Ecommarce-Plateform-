from django.shortcuts import redirect
from django.contrib import messages
from .views import OTP_msg

class OTPExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except OTP_msg as e:
            messages.error(request, str(e))
            return redirect('/forget_pass_phone/')