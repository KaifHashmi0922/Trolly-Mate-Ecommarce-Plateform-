from django.db import models
from datetime import date

# Create your models here.
from django.db import models

# Create your models here.
class Customer(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    pass1=models.CharField(max_length=100)
    phone=models.CharField(unique=True,max_length=10)
    image=models.FileField(upload_to="uploads/users/",null=True)
    dob = models.DateTimeField(blank=True, null=True)
    # completed_at = models.DateTimeField(blank=True, null=True)
    status=models.BooleanField(null=True)
    
    def __str__(self):
        return self.email
    
    
class Address(models.Model):
    cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    alt_phone = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    area = models.TextField(default="Local")
    house = models.TextField()
    status = models.BooleanField(default=True)


class Shoping(models.Model):
    # basic product snapshot at time of purchase
    p_id = models.CharField(max_length=20, null=True, blank=True)
    p_name = models.CharField(max_length=100)
    p_quantity = models.IntegerField(null=True, blank=True)
    p_price = models.IntegerField()  # store final per‑item price at order time
    p_image = models.FileField(upload_to="uploads/Shoping/", null=True, blank=True)

    # order meta
    p_date = models.CharField(max_length=100)  # or better: DateTimeField
    cust_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    shop_date = models.DateTimeField(blank=True, null=True)

    # status: True = delivered, False = cancelled/pending
    status = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.p_name} x{self.p_quantity}"

    @property
    def total_price(self):
        return (self.p_quantity or 0) * self.p_price
    
    
   