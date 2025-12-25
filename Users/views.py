from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Customer,Address,Shoping
from admins.models import Products,Companys
import datetime as dt
from .otp import*
import math
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password
import os
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.contrib.auth.hashers import make_password

from django.core.cache import cache



from django.utils import timezone


from django.contrib.auth import update_session_auth_hash



class Query(Exception):
    def __init__(self,msg):
        self.msg=msg


class Const_t(Exception):
    def __init__(self,msg):
        self.msg=msg
   
class Data_Insert(Exception):
    def __init__(self,msg):
        self.msg=msg


class Product_Info(Exception):
    def __init__(self,msg):
        self.msg=msg
       
       
class Data_NOT(Exception):
     def __init__(self,msg):
        self.msg=msg
       
class OTP(Exception):
     def __init__(self,msg):
        self.msg=msg
       
       
class Payment(Exception):
     def __init__(self,msg):
        self.msg=msg
       


       
otp_data=()


counter=0



def index(request):
    try:
       prods=list(Products.objects.all())
       if  not  prods:
            raise Data_NOT("No products available")
    except Const_t as e:
        print(e)
        return render(request,"user/construct.html",{'message':"Site Under Cunstruction !!!"})
       
    except Exception as e:
        print(e)
        return render(request,"user/construct.html",{'message':"Site Under Cunstruction !!!"})
    else:
        return render(request,"user/index.html/",{'prods':prods,'status':None,'query':None})
   
   
   
def construct(request):
    return render(request,"user/construct.html")




def signup_view(request):
    if request.method=="POST":
        try:
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            pass1=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            dob=request.POST.get('dob')
            img=request.FILES.get('imag',0)
            if not img:
                raise Data_Insert("Image is Must For Register Account")
            else:
                if not (fname and lname and email and phone and pass1 and pass2 and dob and img) :
                    raise Data_Insert("Fill all field")
                else:  
                    if str(pass1)!=str(pass2):
                        raise Data_Insert("Both Password Not Matched")
                    else:
                        cobj=Customer(fname=fname,lname=lname,email=email,pass1=pass1,phone=phone,image=img,status=True,dob=dob)
                        cobj.pass1=make_password(cobj.pass1)
                        cobj.save()
                        request.session['cust_email']=email
                        print(cobj.pass1)
                        request.session['cust_password']=pass1
                        return redirect('/login/')
        except Data_Insert as e:
            return render(request,"user/signup.html",{'msg':e})
        # except Exception as e:
        #     return render(request,"user/signup.html",{'msg':e})
    return render(request,"user/signup.html",{'msg':None})




def login(request):
    email=request.session.get('cust_email')
    password=request.session.get('cust_password')
    if email == None:
        email=0    
    else:
        email=email
    try:
        if email:
            cust= Customer.objects.get(email=email)
            request.session['cust_id']=cust.id            
            request.session['cust_name']=cust.fname
            request.session['cust_email']=cust.email
            cust.status=True
            if cust.image:
                request.session['cust_image']=cust.image.url
            else:
                request.session['cust_image']=""
            cust.save()
            print(request.session.get('cust_email'),request.session.get('cust_password'))
            return redirect('/')
        else:
            if request.method=="POST":
                uname=request.POST.get('username')
                upass=request.POST.get('password')
                if uname and upass:
                    cust=Customer.objects.get(email=uname)
                    if cust:
                        is_valid=check_password(upass,cust.pass1)    
                        if is_valid :
                            request.session['cust_id']=cust.id
                            request.session['cust_name']=cust.fname
                            request.session['cust_email']=cust.email
                            cust.status=True
                            if cust.image:
                                request.session['cust_image']=cust.image.url
                            else:
                                request.session['cust_image']=""
                            cust.save()
                            print(request.session.get('cust_email'),request.session.get('cust_id'))
                            return redirect('/')
                    else:
                        raise Data_Insert("Customer Not Exist !!!")
                else:
                     raise Data_Insert("Pls Enter Email And Pass ")
            print(request.session.get('cust_email'),request.session.get('cust_password'))
            return render(request,"user/cust_login.html",{'msg':None})
    except Data_Insert as e:
        return render(request,"user/cust_login.html",{'msg':e})
    except Exception as e:
        return render(request,"user/cust_login.html",{'msg':e})
     


def cust_soft(request):
    cust_id=request.session.get('cust_id')
    obj=Customer.objects.get(id=cust_id)
    obj.status=False
    print(obj.status)
    obj.save()
    return HttpResponse(cust_id)
   


def logout_view(request):
    request.session.clear()
    return redirect('/')


def profile_view(request):
    try:
        cust_id = request.session.get('cust_id')
        if not cust_id:
            messages.error(request, "Please login first.")
            return redirect('login')
        
        obj = Customer.objects.get(id=cust_id)
        
        # 🔥 Fetch YOUR Shoping orders
        orders = Shoping.objects.filter(cust_address__cid_id=cust_id).order_by('-shop_date')
        
        context = {
            'rec': obj,
            'recemail': obj.email,
            'orders': orders,
            'total_orders': orders.count(),
            'delivered_orders': orders.filter(status=True).count(),
            'pending_orders': orders.filter(status=False).count(),
        }
        return render(request, 'user/profile.html', context)
        
    except Customer.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login')
    except Exception as e:
        print(f"Profile error: {e}")
        messages.error(request, "Something went wrong.")
        return redirect('login')



def cart_view(request):
    try:
        p=request.session.get('cart',0)
        print(p,"in cart view")
        if p:
          prods=Products.objects.filter(id__in=p.keys())
          if not prods:
              raise Product_Info("Cart IS Empty")
        else:
            return render(request,'user/cart.html',{'status':1,'message':"Select Atliest One Product"})
    except Product_Info as e:
        return render (request,"user/cart.html",{'msg':e})
    else:
        return render(request,"user/cart.html",{'prods':prods,'msg':None})






def cart_update(request):
    """Minus auto-detects page: index→/, cart→/cart/"""
    if request.method != "POST":
        return redirect('/')
    
    cart = request.session.get('cart', {})
    print(cart,"cart int cart up")
    product_id = request.POST.get('plus') or request.POST.get('minus') or request.POST.get('c_plus') or request.POST.get('c_minus')
    print(product_id,"product id")
    if not product_id:
        messages.error(request, "Invalid product")
        return redirect('/')
    
    # Action detection
    action = 'add' if 'plus' in request.POST or 'c_plus' in request.POST else 'remove'
    delta = 1 if action == 'add' else -1
    
    # Atomic update
    qty = cart.get(product_id, 0)
    print(qty)
    new_qty = max(0, qty + delta)
    print(new_qty)
    
    if new_qty == 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = new_qty
    
    request.session['cart'] = cart
    print(cart)
    messages.success(request, "Cart updated")
    
    # ✅ SMART REDIRECT: Detects EXACT page context
    if request.POST.get('c_plus') or request.POST.get('c_minus'): # Cart + button
        return redirect('/cart/')
    else:
        return redirect('/')  # plus on index




def cart_delete(request):
    if request.method == "POST":
        pid = request.POST.get("product_id")
        cart = request.session.get("cart", {})
        if pid in cart:
            cart.pop(pid)
            request.session["cart"] = cart
    return redirect("cart")  # your cart page name



def change_password(request):
    email=request.session.get('email')
    if request.method=="POST":
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if str(password1)==str(password2):
            user=Customer.objects.get(email=email)
            user.pass1=make_password(password1)
            user.save()
            return redirect('/login/')
        else:
            return render(request,"user/change_password.html",{'message':"Both Password Not Matched"})
    return render(request,"user/change_password.html")


 
   
# @login_required(login_url='/login/')

def place_order(request):
    c_id = request.session.get('cust_id')
    c_name = request.session.get('cust_name')
    c_email = request.session.get('cust_email')

    if not (c_id and c_email):
        return redirect('/login/')

    cart_ids = request.session.get('cart', {}).keys()
    prods = Products.objects.filter(id__in=cart_ids)

    selected_id = request.session.get('selected_address_id')
    if selected_id:
        address = Address.objects.filter(id=selected_id, cid=c_id).first()
    else:
        address = Address.objects.filter(cid=c_id).first()

    # ✅ COMPLETE ORDER PROCESSING
    if request.method == 'POST' and prods.exists() and address:
        cart = request.session.get('cart', {})
        order_count = 0
        
        for prod_id, cart_item in cart.items():
            product = Products.objects.get(id=prod_id)
            quantity = cart_item.get('quantity', 1)
            
            # ✅ 1. STOCK CHECK (your field: quantity)
            if product.quantity < quantity:
                messages.error(request, f"❌ Insufficient stock for {product.name}")
                return render(request, "user/placeorder.html", context)
            
            # ✅ 2. MINUS STOCK (quantity field)
            product.quantity -= quantity
            product.save()
            
            # ✅ 3. CREATE Shoping record (EXACT field mapping)
            shop_order = Shoping(
                p_id=str(product.id),
                p_name=product.name,           # ✅ Your field
                p_quantity=quantity,
                p_price=int(product.price),    # ✅ Your field (convert to int)
                p_image=product.image,         # ✅ Your field
                p_date=str(date.today()),
                cust_address=address,
                shop_date=timezone.now(),
                status=False  # Pending
            )
            shop_order.save()
            order_count += 1
        
        # ✅ 4. Clear cart & Success
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, f"✅ Order placed! {order_count} items added to history.")
        return redirect('payment_gateway')

    context = {
        'prods': prods,                    # ✅ Products list
        'address': address,               # ✅ Address object
        'total_amount': "1001",     # ✅ Calculate: sum(p.price for p in prods)
        'order_id': '12345',             # ✅ Optional
    }
    return render(request, 'user/placeorder.html', context)



 
def forget_password_phone(request):
    timer_s=request.session.get('timer')
    if request.method == "POST":
        phone = request.POST.get('phone')
        try:
            if not  phone:
                raise OTP("Phone Number is Must For Varify")
            else:
                obj = Customer.objects.get(phone=phone)
                user_info = [str(obj.email), str(obj.phone)]
                if user_info:
                    while(1):
                        times=dt.datetime.now()
                        timer_s=time_format(timer_s)
                        if times>=timer_s:
                            print("if")
                            global counter
                            if counter<=3:
                                print("if counter")
                                print(counter)
                                otp,old_time=phone_otp(user_info)
                                request.session['time_temp']=str(old_time)
                                timer=time_limit(str(old_time))
                                if otp:
                                    print("otp")
                                    request.session['gotp']=otp
                                    request.session['phone']=obj.phone
                                    request.session['old_time']=str(old_time)
                                    counter=0
                                    print(counter,"counter")
                                    return redirect('/phone_varify')
                                else:
                                    counter+=1
                                    print(counter,"counter")
                                    request.session['timer']=str(timer)
                            else:
                                raise OTP("Too many OTP requests—please try again after 1 Minuts.")
                        else:
                            ltime=str(dt.datetime.now())
                            stime=str(request.session.get('timer'))
                            rem_time=remaining_minutes(stime,ltime)
                            raise OTP(f"Too many OTP requests—please try again after {rem_time} Minuts.")
                else:            
                    raise OTP("Invalid Phone !!!")
        except OTP as e:
            return render(request, "user/forget_pass_phone.html",{'status':0,'message':e})
    if not request.session.get('timer'):
        t=str(dt.datetime.now())
        nt=str(time_format(t))
        request.session['timer']=nt
    print(request.session.get('timer'))
    return render(request, "user/forget_pass_phone.html",{'status':0,'message':None})



def phone_otp_varify(request):
    temp=[]
    if request.method == "POST":
        try:
            phone=request.POST.get('phone')
            cotp=request.POST.get('otp')
            if  cotp :
                gotp=request.session.get('gotp')
                old_time=request.session.get('old_time')
                temp.append(gotp)
                temp.append(cotp)
                temp.append(old_time)
                temp=tuple(temp)
                result=varify_otp(temp)
                if result:
                   obj=Customer.objects.get(phone=phone)
                   request.session['email']=obj.email
                   return redirect('/change_password/')
                else:      
                    return redirect('/forget_pass_phone/')        
            else:
                raise OTP("OTP IS Must For Varification")
               
        except OTP as e:
            return render(request,"user/forget_pass_phone.html",{'status':0,'message':e})
    phone=request.session.get('phone')
    print(phone)
    return render(request, "user/forget_pass_phone.html",{'phone':phone,'status':1,'message':None})




def forget_password_email(request):
    """Admin-style forgot password: Single template, cache-based."""
    context = {'status': 0, 'message': None}
    
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            context['message'] = 'Email required'
            return render(request, "user/forget_pass_email.html", context)
        
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            context['message'] = 'Email not found'
            return render(request, "user/forget_pass_email.html", context)
        
        # Cache rate limiting
        cache_key = f'otp_email_{email}'
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 3:
            context['message'] = 'Too many requests. Try again later.'
            return render(request, "user/forget_pass_email.html", context)
        
        # Generate OTP
        otp, otp_time = email_otp([customer.fname, customer.lname, customer.email])
        if otp:
            cache.set(f'otp_data_{email}', (otp, str(otp_time), email), 300)
            cache.set(cache_key, attempts + 1, 300)
            # ✅ Switch to verify screen
            context.update({'status': 1, 'email': email})
            return render(request, "user/forget_pass_email.html", context)
        
        cache.set(cache_key, attempts + 1, 300)
        context['message'] = 'OTP generation failed'
    
    return render(request, "user/forget_pass_email.html", context)

def email_otp_varify(request):
    """Verify step (redirects to main flow)."""
    return forget_password_email(request)  # Single source of truth



def change_password(request):
    """Change password after OTP verification. Updates DB + login redirect."""
    context = {'status': 0, 'message': None, 'email': None}
    
    # Check if user verified (email in session)
    email = request.session.get('email')
    if not email:
        messages.error(request, 'Verification expired. Please start again.')
        return redirect('forget_pass_email')
    
    context['email'] = email
    
    if request.method == "POST":
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        
        # Validation
        if not password1 or not password2:
            context['message'] = 'Both passwords required'
            return render(request, "user/change_password.html", context)
        
        if password1 != password2:
            context['message'] = "Passwords don't match"
            return render(request, "user/change_password.html", context)
        
        if len(password1) < 8:
            context['message'] = 'Password must be 8+ characters'
            return render(request, "user/change_password.html", context)
        
        try:
            # ✅ UPDATE PASSWORD IN DB
            customer = Customer.objects.get(email=email)
            customer.pass1 = make_password(password1)  # Secure hash
            customer.save()
            
            # ✅ CLEANUP
            del request.session['email']
            cache.delete(f'otp_data_{email}')  # Remove OTP cache
            
            messages.success(request, 'Password changed successfully!')
            return redirect('login')  # Go to login page
            
        except Customer.DoesNotExist:
            context['message'] = 'User not found'
    
    return render(request, "user/change_password.html", context)


# def forget_password_email(request):
#     timer_s=str(request.session.get('timer'))
#     if request.method == "POST":
#         try:
#             email = request.POST.get('email')
#             if not email:
#                 raise OTP("Email is Must For Forget Password")
#             else:
#                 obj = Customer.objects.get(email=email)  
#                 user_info = [obj.fname, obj.lname, obj.email]
#                 if user_info:
#                         while(1):
#                             times=dt.datetime.now()
#                             timer_s=time_format(timer_s)
#                             if times>=timer_s:
#                                 print("if")
#                                 global counter
#                                 if counter<=3:
#                                     print("if counter")
#                                     print(counter)
#                                     otp,old_time=email_otp(user_info)
#                                     request.session['time_temp']=str(old_time)
#                                     timer=time_limit(str(old_time))
#                                     if otp:
#                                         print("otp")
#                                         global otp_data
#                                         otp_data=(otp,old_time,obj.email)
#                                         counter=0
#                                         print(counter,"counter")
#                                         return redirect('/email_varify/')
#                                     else:
#                                         counter+=1
#                                         print(counter,"counter")
#                                         request.session['timer']=str(timer)
#                                 else:
#                                     raise OTP("Too many OTP requests—please try again after 1 Minuts.")
#                             else:
#                                 ltime=str(dt.datetime.now())
#                                 stime=str(request.session.get('timer'))
#                                 rem_time=remaining_minutes(stime,ltime)
#                                 raise OTP(f"Too many OTP requests—please try again after {rem_time} Minuts.")
#                 else:            
#                         raise OTP("Invalid Phone !!!")
#         except OTP as e:
#           return render(request, "user/forget_pass_email.html",{'status':0,'message':e})
#     if not request.session.get('timer'):
#         t=str(dt.datetime.now())
#         nt=str(time_format(t))
#         request.session['timer']=nt
#     print(request.session.get('timer'))
#     return render(request, "user/forget_pass_email.html",{'status':0,'message':None})


   


# def email_otp_varify(request):
#     temp=[]
#     gotp,old_time,email=otp_data
#     if request.method=="POST":
#         try:
#             email=request.POST.get('email')
#             cotp=request.POST.get('otp')
#             temp.append(gotp)
#             temp.append(cotp)
#             temp.append(str(old_time))
#             temp=tuple(temp)
#             result=varify_otp(temp)
#             if result:
#                 obj=Customer.objects.get(email=email)
#                 request.session['email']=obj.email
#                 return redirect('/change_password/')
#             else:
#                 raise OTP("OTP IS Must For Varification")
#         except OTP as e:
#             return render(request, "user/forget_pass_email.html",{'status':0,'message':e})
#     return render(request,"user/forget_pass_email.html",{'status':1,'email':email})



def payment_gateway(request):
    cart = request.session.get('cart', {})
    ids = cart.keys()
    prods = Products.objects.filter(id__in=ids)


    # total
    total = 0
    for p in prods:
        qty = int(cart.get(str(p.id), 1))
        total += int(p.price) * qty


    # selected address (read only)
    c_id = request.session.get('cust_id')
    selected_id = request.session.get('selected_address_id')
    address = None
    if c_id and selected_id:
        address = Address.objects.filter(id=selected_id, cid=c_id).first()
    elif c_id:
        address = Address.objects.filter(cid=c_id).first()


    context = {
        "prods": prods,
        "address": address,
        "total": total,
    }
    return render(request, "user/payment.html", context)


def payment(request):
    cart = request.session.get('cart', {})
    product_ids = list(cart.keys())
    if not product_ids:
        return redirect('/cart/')

    products = Products.objects.filter(id__in=product_ids)
    
    # 🔥 STORE YOUR Shoping orders
    c_id = request.session.get('cust_id')
    selected_id = request.session.get('selected_address_id')
    
    if c_id:
        address = None
        if selected_id:
            address = Address.objects.filter(id=selected_id, cid_id=c_id).first()
        elif c_id:
            address = Address.objects.filter(cid_id=c_id).first()
        
        # Create Shoping records (YOUR exact fields)
        for p in products:
            qty = int(cart.get(str(p.id), 1))
            Shoping.objects.create(
                p_id=str(p.id),
                p_name=p.name,  # Adjust to your Products.name field
                p_quantity=qty,
                p_price=int(p.price),
                p_image=p.image,  # Adjust to your Products.image field
                p_date=str(timezone.now().date()),
                cust_address=address,
                shop_date=timezone.now(),
                status=True
            )
    
    # Rest of YOUR existing code (unchanged)
    line_items = []
    grand_total = 0
    for p in products:
        qty = int(cart.get(str(p.id), 1))
        total_price = int(p.price) * qty
        grand_total += total_price
        line_items.append({"product": p, "qty": qty, "price": p.price, "total": total_price})

    email = request.session.get('cust_email')
    cust_name = request.session.get('cust_name')
    
    request.session['cart'] = {}
    request.session.modified = True

    if email:
        send_invoice_email(request, email, product_ids)

    today = timezone.now().date()
    context = {
        'line_items': line_items, 'grand_total': grand_total, 'email': email,
        'cust_name': cust_name, 'cust_email': email, 'address': address,
        'order_id': None, 'payment_mode': 'Online (Demo)', 'order_date': today,
    }
    return render(request, "user/invoice.html", context)



def buynow(request):
    cart=request.session.get('cart',{})
    print(cart)
  
    if request.method=="POST":
        p_id=request.POST.get('bynow')
        print(p_id)
       
        prod=cart.get(p_id)
        print(prod)
        
        if prod:
            return redirect('/cart/')
        else:
            cart[p_id]=1
            request.session['cart']=cart
            print(cart)
            return redirect('/cart/')    
    request.session['cart']=cart
    return redirect('/')









@csrf_exempt
def payment_callback(request):
    if request.method != "POST":
        return redirect("/")


    rzp_order_id = request.POST.get("razorpay_order_id", "")
    rzp_payment_id = request.POST.get("razorpay_payment_id", "")
    rzp_signature = request.POST.get("razorpay_signature", "")


    params_dict = {
        "razorpay_order_id": rzp_order_id,
        "razorpay_payment_id": rzp_payment_id,
        "razorpay_signature": rzp_signature,
    }


    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
        # mark success -> store some info in session for invoice
        request.session["payment_success"] = True
        request.session["payment_method"] = "Online"
        request.session["razorpay_payment_id"] = rzp_payment_id
        return redirect("payment")   # go to invoice view
    except:
        request.session["payment_success"] = False
        return render(request, "user/payment_failed.html")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# pending




class SearchError(Exception):
    pass



def query(request):
    q = request.GET.get('query', '').strip()


    if not q:
        return render(request, "user/index.html", {
            'prods': Products.objects.filter(status=True),
            'status': None,
            'query': "Please enter a search term."
        })


    words = q.split()
    prods = Products.objects.filter(status=True)


    q_objects = Q()
    for word in words:
        q_objects |= Q(name__icontains=word)
        q_objects |= Q(des__icontains=word)
        q_objects |= Q(category__icontains=word)
        q_objects |= Q(company__name__icontains=word)


    results = prods.filter(q_objects)


    if not results.exists():
        return render(request, "user/index.html", {
            'prods': prods,
            'status': None,
            'query': "No matching products found."
        })


    return render(request, "user/index.html", {
        'prods': results,
        'status': 1,
        'query': q
    })










def cust_edit(request):
    cid = request.session.get('cust_id')
    if not cid:
        return redirect('/login/')


    try:
        obj = Customer.objects.get(id=cid)
    except Customer.DoesNotExist:
        return redirect('/login/')


    if request.method == "POST":
        obj.fname = request.POST.get('fname')
        obj.lname = request.POST.get('lname')
        obj.email = request.POST.get('email')
        obj.Phone = request.POST.get('phone')


        image = request.FILES.get('image')
        if image:
            if obj.image:
                obj.image.delete(save=False)
            obj.image = image


        obj.save()


    return render(request, 'user/profile.html', {'rec': obj})




def show_address(request):
    c_id = request.session.get('cust_id')
    if not c_id:
        return redirect('/login/')


    try:
        cust = Customer.objects.get(id=c_id)
    except Customer.DoesNotExist:
        return redirect('/login/')


    addresses = Address.objects.filter(cid=cust)


    if request.method == "POST":
        # radio button value
        addr_id = request.POST.get("address_id")
        if addr_id:
            request.session["selected_address_id"] = int(addr_id)
            request.session.modified = True
            return redirect('/place_order/')   # go back to order summary


    selected_id = request.session.get("selected_address_id")


    return render(request, "user/show_address.html", {
        'cust': cust,
        'address': addresses,
        'selected_address_id': selected_id,
    })



def add_address(request):
    cid = request.session.get('cust_id')
    email = request.session.get('cust_email')


    # Login check
    if not cid or not email:
        return redirect('/login/')


    if request.method == "POST":
        cust = Customer.objects.get(email=email)


        Address.objects.create(
            cid=cust,
            fullname=request.POST.get('fullname'),
            phone=request.POST.get('phone'),
            alt_phone=request.POST.get('alt_phone') or None,
            pincode=request.POST.get('pincode'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            country=request.POST.get('country'),
            house=request.POST.get('house'),
            area=request.POST.get('area'),
            status=True
        )


        return redirect('/place_order/')


    return render(request, "user/address_form.html")



def edit_address(request, id):
    cid = request.session.get('cust_id')
    if not cid:
        return redirect('/login/')


    address = Address.objects.get(id=id, cid_id=cid)


    if request.method == "POST":
        address.fullname = request.POST.get('fullname')
        address.phone = request.POST.get('phone')
        address.alt_phone = request.POST.get('alt_phone')
        address.pincode = request.POST.get('pincode')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.house = request.POST.get('house')
        address.area = request.POST.get('area')
        address.save()


        return redirect('/show_address/')


    return render(request, "user/edit_address.html", {'address': address})



def delete_address(request, id):
    cid = request.session.get('cust_id')
    if not cid:
        return redirect('/login/')


    address = Address.objects.get(id=id, cid_id=cid)
    address.delete()


    return redirect('/show_address/')







def cust_update(request):
    print("POST DATA:", dict(request.POST))  # ✅ DEBUG
    
    if request.method == 'POST':
        cust_id = request.session.get('cust_id')
        if not cust_id:
            messages.error(request, "Please login first.")
            return redirect('cust_profile')
        
        try:
            customer = Customer.objects.get(id=cust_id)
            
            # PROFILE UPDATE - Check for fname (profile form)
            if request.POST.get('fname'):
                print("PROFILE UPDATE")
                customer.fname = request.POST.get('fname')
                customer.lname = request.POST.get('lname')
                customer.email = request.POST.get('email')
                customer.phone = request.POST.get('phone')
                
                if 'image' in request.FILES:
                    customer.image = request.FILES['image']
                
                customer.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('cust_profile')
            
            # PASSWORD UPDATE - Check for new_password (password form)
            elif request.POST.get('new_password'):
                print("PASSWORD UPDATE")
                print("Current pass:", request.POST.get('current_password')[:3] + "***")
                print("New pass length:", len(request.POST.get('new_password')))
                
                current_password = request.POST.get('current_password', '')
                new_password = request.POST.get('new_password', '')
                confirm_password = request.POST.get('confirm_password', '')
                
                # Check current password
                print("Checking password...")
                if not check_password(current_password, customer.pass1):
                    print("❌ Current password WRONG")
                    messages.error(request, "Current password is incorrect!")
                    return redirect('cust_profile')
                print("✅ Current password CORRECT")
                
                # Check match
                if new_password != confirm_password:
                    print("❌ Passwords don't match")
                    messages.error(request, "New passwords don't match!")
                    return redirect('cust_profile')
                
                # Length check
                if len(new_password) < 6:
                    print("❌ Password too short")
                    messages.error(request, "Password must be at least 6 characters!")
                    return redirect('cust_profile')
                
                # UPDATE!
                print("✅ UPDATING PASSWORD")
                customer.pass1 = make_password(new_password)
                customer.save()
                print("✅ SAVED!")
                
                messages.success(request, "✅ Password changed successfully!")
                return redirect('cust_profile')
            
            else:
                print("❌ NO FORM DATA")
                messages.error(request, "Invalid form data!")
                return redirect('cust_profile')
                
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found!")
            return redirect('login')
    
    return redirect('cust_profile')
