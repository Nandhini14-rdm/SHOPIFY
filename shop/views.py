from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from django.contrib import messages
from django.http import HttpResponse , JsonResponse
from shop.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
import json


def home(request):
    products = Products.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect('/')
            else:
                messages.error(request, "Invalid credentials!")
                return redirect('/login')
        return render(request, "shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have successfully logged out!")
        return redirect('/')


def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully registered! You can login now.")
            return redirect('/login')
    return render(request, "shop/register.html", {"form": form})

def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category": category})

def collectionsview(request, name):
    if(Category.objects.filter(name=name, status=0)):
        products = Products.objects.filter(category__name = name )
        return render(request, "shop/products/index.html", {"products": products, "category_name":name})
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')


def product_details(request, cname, pname):
    if(Category.objects.filter(name=cname, status=0)):
        if(Products.objects.filter(name=pname, status=0)):
            products = Products.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products})
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
        return redirect('collections')
    

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status = Products.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Out of Stock'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add to Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
    

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    else:
        return redirect('/')
    
def remove_cart(request, cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id=data['pid']
            #print(request.user.id)
            product_status = Products.objects.get(id=product_id)
            if product_status:
                if Favorite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favorite'}, status=200)
                else:
                    Favorite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product added to Favourite'}, status=200)
           
        else:
            return JsonResponse({'status':'Login to Add to Favorite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
    
def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favorite.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {"fav": fav})
    else:
        return redirect('/')
    
def remove_fav(request, fid):
    favitem = Favorite.objects.get(id=fid)
    favitem.delete()
    return redirect("/favviewpage")

def payment_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    # Handle POST request to process payment
    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        if quantity > product.quantity:
            return render(request, 'shop/outofstock.html')
        total_cost = quantity * product.selling_price
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_cost=total_cost
        )
        # Handle the payment processing here (e.g., integrate with a payment gateway)
        # After successful payment, update the order status:
        order.order_status = 'Paid'
        order.save()

        # Reduce stock quantity
        product.quantity -= quantity
        product.save()

        return render(request, 'shop/payment_success.html')
    return render(request, 'shop/payment.html', {'product': product})


def item_detail(request, cname, pname):
    """
    View function to display the details of a product in a specific category.
    """

    # Check if the category exists
    category = get_object_or_404(Category, name=cname, status=0)
    
    # Check if the product exists within the given category
    product = get_object_or_404(Products, name=pname, category=category, status=0)
    
    # Pass the product details to the template
    return render(request, "shop/products/product_details.html", {
        'product': product,
        'category': category
    })