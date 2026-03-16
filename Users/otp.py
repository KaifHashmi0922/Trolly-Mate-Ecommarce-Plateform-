import datetime as dt
import random as rm
import math
import os
import requests

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa


# ----------------------------------------------------------
# Time Helper
# ----------------------------------------------------------

time = dt.datetime


# ----------------------------------------------------------
# OTP GENERATION
# ----------------------------------------------------------

def genrate_otp():
    otp = rm.randint(100000, 999999)
    old_time = time.now()
    return otp, old_time


def check_time(old_time):
    old_time = dt.datetime.strptime(str(old_time), "%Y-%m-%d %H:%M:%S.%f")
    return old_time + dt.timedelta(minutes=5)


def time_limit(old_time):
    old_time = dt.datetime.strptime(str(old_time), "%Y-%m-%d %H:%M:%S.%f")
    return old_time + dt.timedelta(minutes=1)


def time_format(old_time):
    return dt.datetime.strptime(str(old_time), "%Y-%m-%d %H:%M:%S.%f")


def remaining_minutes(time_a, time_b):

    fmt = "%Y-%m-%d %H:%M:%S.%f"

    t_a = dt.datetime.strptime(str(time_a), fmt)
    t_b = dt.datetime.strptime(str(time_b), fmt)

    diff_minutes = (t_a - t_b).total_seconds() / 60

    return math.ceil(abs(diff_minutes))


# ----------------------------------------------------------
# VERIFY OTP
# ----------------------------------------------------------

def varify_otp(*a):

    gotp, cotp, old_time = a[0]

    new_time = check_time(old_time)

    if time.now() <= new_time:

        if str(gotp) == str(cotp):
            return True

        else:
            return False

    else:
        print("OTP Expired")
        return False


# ----------------------------------------------------------
# EMAIL OTP
# ----------------------------------------------------------

def email_otp(*a):

    fname, lname, email = a[0]

    otp, old_time = genrate_otp()

    subject = "TrollyMate OTP Verification"

    message = f"""
Hi {fname} {lname},

You requested a password reset.

Your OTP is: {otp}

This OTP is valid for 10 minutes.

If you did not request this, please ignore this email.

Thanks,
TrollyMate Team
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

    return otp, old_time


# ----------------------------------------------------------
# PHONE OTP
# ----------------------------------------------------------

def phone_otp(*a):

    api_root = "https://2factor.in/API/V1/"
    api_key = "YOUR_API_KEY/"
    type_otp = "SMS/"
    country_code = "+91"

    email, phone = a[0]

    otp, old_time = genrate_otp()

    url = f"{api_root}{api_key}{type_otp}{country_code}{phone}/{otp}"

    try:
        response = requests.get(url)
        print(response.text)

    except Exception as e:
        print("SMS Error:", e)

    return otp, old_time


# ----------------------------------------------------------
# LINK CALLBACK (for images in PDF)
# ----------------------------------------------------------

def link_callback(uri, rel):

    if uri.startswith(settings.MEDIA_URL):

        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    elif uri.startswith(settings.STATIC_URL):

        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))

    else:
        return uri

    return path


# ----------------------------------------------------------
# GENERATE PDF
# ----------------------------------------------------------

def generate_invoice_pdf(request, context):

    try:

        html = render_to_string("user/invoice_pdf.html", context)

        result = BytesIO()

        pdf = pisa.pisaDocument(
            BytesIO(html.encode("UTF-8")),
            result,
            link_callback=link_callback
        )

        if pdf.err:
            print("PDF Generation Error")
            return None

        return result.getvalue()

    except Exception as e:

        print("PDF generation failed:", e)
        return None


# ----------------------------------------------------------
# SEND INVOICE EMAIL
# ----------------------------------------------------------

def send_invoice_email(request, context):

    try:

        pdf = generate_invoice_pdf(request, context)

        if not pdf:
            print("PDF generation failed")
            return False

        email = EmailMessage(
            subject="Your Trollymate Invoice",
            body="Thank you for your purchase! Please find the invoice attached.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[context["cust_email"]],
        )

        email.attach("invoice.pdf", pdf, "application/pdf")

        email.send(fail_silently=False)

        return True

    except Exception as e:

        print("Email sending error:", e)

        return False