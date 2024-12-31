from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import os

def getFileName(request, fileName):
    now_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    new_fileName = "%s%s"%(now_time, fileName)
    return os.path.join('upload/', new_fileName)

# category
class Category(models.Model):
    name = models.CharField(max_length=150, null=False,blank=False)
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False, help_text="0-default, 1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#products
class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False,blank=False)
    vendor = models.CharField(max_length=150, null=False,blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    product_image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False, help_text="0-default, 1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default, 1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_qty * self.product.selling_price


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    total_cost = models.FloatField(null=False, blank=False)
    order_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} for {self.product.name}"
