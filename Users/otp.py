from django.core.mail import send_mail
from django.conf import settings
import requests
import datetime as dt
import random as rm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.conf import settings
from admins.models import Products
import math
# Create your views here.

#--------------------------------------------------------------------------------------------------------------
time=dt.datetime


def email_otp(*a):   
    fname, lname, email = a[0]
    otp,old_time=genrate_otp()
    subject = 'Hello Brother'
    message = f"""Hi [ {fname} {lname} ],

requested a password reset. Use the code below to proceed:

🔐 OTP: {otp}

This code is valid for 10 minutes. If you didn’t request this, just ignore this email.

Thanks,  The [ TrollyMate ] Team
                """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list)
    return otp,old_time

    
def check_time(time):
        time = dt.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        new_time=time+dt.timedelta(minutes=5)
        return new_time
    
def time_limit(time):
        time = dt.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        new_time=time+dt.timedelta(minutes=1)
        return new_time 
def time_format(time):
    new_time = dt.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    return new_time
    


def remaining_minutes(time_a, time_b):
    # Define the format for parsing
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    
    # Parse the input time strings into datetime objects
    t_a = dt.datetime.strptime(time_a, fmt)
    t_b = dt.datetime.strptime(time_b, fmt)
    
    # Calculate the difference in minutes
    # Calculate difference in total seconds
    diff_minutes = (t_a - t_b).total_seconds() / 60
    # Return absolute value of the minutes
    return math.ceil(abs(diff_minutes))


def genrate_otp():
    otp=rm.randint(100000,999999)
    old_time=time.now()
    return otp,old_time

def varify_otp(*a):
        gotp,cotp,old_time=a[0]
        new_time=check_time(old_time)
        if time.now()<=new_time:
           if str(gotp)==str(cotp):
              return True
           else:
              return False
        else:
           print(" Otp Expired")
           return False
        




# ---------------------------------------------------------------------------
def phone_otp(*a):
    api_root="https://2factor.in/API/V1/"
    api_key="a0780a7e-aa8b-11ef-8b17-0200cd936042/"
    type_otp="SMS/"
    cuntry_code="+91"
    email, phone = a[0]
    number=phone+"/"
    otp,old_time=genrate_otp()
    otp=str(otp)
    url=api_root+api_key+type_otp+cuntry_code+number+otp
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return otp,old_time

#

# def send_invoice_email():
#     pass


def generate_invoice_pdf(request, email, product_ids):
    products = Products.objects.filter(id__in=product_ids)

    # Include `request` in the context
    html = render_to_string(
        'user/invoice.html',
        {
            'email': email,
            'prods': products,
            'request': request,  # ✅ this line fixes the error
        }
    )
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None

def send_invoice_email(request ,email, product_ids):
    pdf = generate_invoice_pdf(request,email, product_ids)

    if pdf:
        subject = 'Your Invoice from Our Shop'
        message = 'Please find attached your invoice.'
        email_msg = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        email_msg.attach('invoice.pdf', pdf, 'application/pdf')
        email_msg.send()