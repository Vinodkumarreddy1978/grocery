from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Cart
from django.contrib.auth.decorators import login_required

def home(r):
    return render(r, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password1 = request.POST['password2']
        
        if password != password1:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username.title()).exists():
            messages.error(request, "Username already exists...!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken...!")
        elif len(password) < 8:
            messages.error(request, "Password must be at least eight characters")
        else:
            user = User.objects.create_user(username=username.title(), email=email, password=password)
            login(request, user)
            return redirect('home')
    
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username.title(), password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid login credentials")
    
    return render(request, 'signin.html')

def products(r):
    data = Product.objects.all()
    return render(r, 'products.html', {'data': data})

def signout(request):
    logout(request)
    return redirect('/')

from django.http import JsonResponse

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({"message": "Item added to cart", "item_count": cart_item.quantity})
    
    return JsonResponse({"error": "Invalid request"})
