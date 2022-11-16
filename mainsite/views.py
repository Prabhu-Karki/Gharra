from django.contrib.auth.views import PasswordChangeView
from itertools import product
from os import link
from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from django.views import View
from django.db.models import Q 
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class IndexView(View):
    # cart = Cart.objects.filter(cart_user=user)
    def get(self, request):
        totalitem = 0
        apple= Product.objects.filter(category='AP')
        samsung= Product.objects.filter(category='SA')
        xiaomi = Product.objects.filter(category="XI")
        laptop = Product.objects.filter(category="L")
        mobile= Product.objects.filter(category='M')
        dell = Product.objects.filter(category='DE')
        hp = Product.objects.filter(category="HP")
        new_arrival = Product.objects.filter(product_status="NA")
        special_product = Product.objects.filter(category="SP")

        if request.user.is_authenticated:
            profile = Customer.objects.filter(user=request.user)
            cart= Cart.objects.filter(cart_user= request.user)
            totalitem = len(Cart.objects.filter(cart_user = request.user))
            return render(request, 'index.html', {'cart': cart, 'profile': profile, 'active': 'nav-link', 'new_arrival' : new_arrival, 'special_product': special_product, 'apple': apple, 'samsung': samsung, 'mobile': mobile, 'laptop': laptop, 'xiaomi': xiaomi, 'dell': dell, 'hp': hp, 'totalitem': totalitem})

        return render(request, 'index.html', {'active': 'nav-link', 'new_arrival' : new_arrival, 'special_product': special_product, 'apple': apple, 'samsung': samsung, 'mobile': mobile, 'laptop': laptop, 'xiaomi': xiaomi, 'dell': dell, 'hp': hp, 'totalitem': totalitem})



class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        productreview = Product.objects.get(pk=pk)
        review = Review.objects.filter(product=productreview)
        related = Product.objects.filter(brand='AP')
        item_exist = False

        if request.user.is_authenticated:
            profile = Customer.objects.filter(user=request.user)
            cart= Cart.objects.filter(cart_user= request.user)
            totalitem = len(Cart.objects.filter(cart_user = request.user))
        return render(request, 'product-detail.html', {'product': product, 'active': 'nav-link',  'item_exist': item_exist, 'related': related, 'reviews': review, 'profile': profile, 'cart': cart, 'totalitem': totalitem})


def review_rate(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'GET':
        prod_id = request.GET.get('product_id')
        product = Product.objects.get(id=prod_id)
        comment = request.GET.get('review')
        rating = request.GET.get('rating')
        user = request.user
        Review(customer_name=user, product=product, review=comment, rating=rating).save()
        return redirect(url)

def signin(request):
    if request.method == 'POST':
        username= request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password = password, username= username)
        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:   
            messages.info(request, 'Invalid Credentials. Please try again.')
            return redirect('signins')
    else:
        return render(request, 'user-login.html', {'profile': profile, 'active': 'nav-link'})

def signup(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('signups')
            else:
                user = User.objects.create_user(username = username, password=pass1, email= email)
                user.save();
                return redirect('signins')
        else:
            messages.info(request, "Password not matching")
            return redirect('signups')
    else: 
        return render(request, 'user-register.html',{'active': 'nav-link'})

@login_required
def signout(request):
    auth.logout(request)
    return redirect('/')


def iphone(request):
    pass

def ipad(request):
    pass

def macbook(request):
    pass


def passwordreset(request):
    return render(request, 'user-reset-password.html')


@login_required
def profile(request):
    profile = Customer.objects.filter(user=request.user)
    cart= Cart.objects.filter(cart_user= request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))

    if profile:
        return render(request, 'user-acount.html', {'profile': profile, 'active': 'nav-link', 'cart': cart, 'totalitem': totalitem})
 
    else:
        return redirect('create-user-account')


@login_required
def create_profile(request):
    cart= Cart.objects.filter(cart_user= request.user)
    profile= Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))

    if request.method =='GET':
        form= CustomerProfileForm()
        return render(request, 'create-user-account.html', {'form': form, 'profile': profile,'active': 'nav-link', 'cart': cart, 'totalitem': totalitem})


    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name= form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            city= form.cleaned_data['city']
            state= form.cleaned_data['state']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            reg = Customer(user= usr, name=name, phone =phone, email=email, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, 'Congratulations! Your profile has been added sucessfully.')
        return render(request, 'user-acount.html', {'profile': profile, 'cart': cart,'active': 'nav-link', 'totalitem': totalitem})




@login_required
def editprofile(request):
    profile= Customer.objects.get(user=request.user)
    cart= Cart.objects.filter(cart_user= request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! Your profile has been updated sucessfully.')
        return redirect('profile')

    else:
        form = CustomerProfileForm(instance=profile)
        return render(request, 'edit-profile.html', {'form': form, 'profile': profile, 'cart': cart,'active': 'nav-link', 'totalitem': totalitem})

@login_required
def addtocart(request,id):
    user = request.user
    product= Product.objects.get(id=id)
    # profile = Customer.objects.filter(user=request.user)
    # cart= Cart.objects.filter(cart_user= request.user)
    storage = request.GET.get('storage', False)
    color = request.GET.get('color', False)
    if Cart.objects.filter(cart_user=user, cart_product=product).exists():
        return redirect('show_cart')
    else:
        Cart(cart_user = user, cart_product = product, product_storage=storage, product_color=color).save()
    return redirect('show_cart')
    
@login_required
def payment_method(request):
    profile = Customer.objects.filter(user=request.user)
    cart= Cart.objects.filter(cart_user= request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))
    return render(request, 'payment-method.html', {'profile' : profile, 'cart': cart, 'active': 'nav-link','totalitem': totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(cart_product=prod_id) & Q(cart_user= request.user))
        c.quantity +=1
        c.save()
        amount= 0.0
        shipping_amount= 80.0
        cart_product = [p for p in Cart.objects.all() if p.cart_user == request.user]
        for p in cart_product:
            temp_amount= (p.cart_product.discounted_price) * (p.quantity)
            amount += temp_amount

        data = {

            'quantity': c.quantity,
            'amount': amount, 
            'totalamount':  amount + shipping_amount
            }
        return JsonResponse(data)  

@login_required
def address(request):
    profile = Customer.objects.filter(user=request.user)
    cart= Cart.objects.filter(cart_user= request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))
    return render(request, 'address.html', {'profile': profile, 'cart': cart, 'active': 'nav-link', 'totalitem': totalitem})
    
@login_required
def checkout(request):
    user = request.user
    profile = Customer.objects.filter(user=request.user)
    cart= Cart.objects.filter(cart_user= request.user)
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(cart_user = user)
    amount = 0.0
    shipping_amount = 80.0
    cart_product = [p for p in Cart.objects.all() if p.cart_user == request.user]
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))
    if cart_product:
        for p in cart_product:
            temp_amount= (p.cart_product.discounted_price) * (p.quantity)
            amount += temp_amount
        totalamount= amount + shipping_amount
    return render(request, 'product-checkout.html', {'add': add, 'active': 'nav-link', 'totalamount': totalamount, 'cart_items': cart_items, 'profile': profile, 'cart': cart, 'totalitem': totalitem})


@login_required
def show_cart(request):
    profile = Customer.objects.filter(user=request.user)
    cart= Cart.objects.filter(cart_user= request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))

    if request.user.is_authenticated:
        user= request.user
        cart= Cart.objects.filter(cart_user=user)
        amount = 0.00
        shipping_amount = 80.0
        cart_product = [p for p in Cart.objects.all() if p.cart_user == user]
        
        if cart_product:
            for p in cart_product:
                temp_amount= (p.cart_product.discounted_price) * (p.quantity)
                amount += temp_amount
                total_amount = amount + shipping_amount
            return render(request, 'product-cart.html', {'carts': cart, 'amount': amount, 'totalitem': totalitem, 'total_amount': total_amount, 'profile': profile, 'cart': cart})
        else:
            return render(request, 'emptycart.html',{'profile': profile, 'active': 'nav-link', 'cart': cart, 'totalitem': totalitem})



def minus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(cart_product=prod_id) & Q(cart_user= request.user))
        c.quantity -=1
        c.save()
        amount= 0.0
        shipping_amount= 80.0
        cart_product = [p for p in Cart.objects.all() if p.cart_user == request.user]

        for p in cart_product:
            temp_amount= (p.cart_product.discounted_price) * (p.quantity)
            amount += temp_amount

        data = {
            'quantity': c.quantity,
            'amount': amount, 
            'totalamount':  amount + shipping_amount,
            }
        return JsonResponse(data)
        

def remove_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        print('printing the c')
        c = Cart.objects.get(Q(cart_product=prod_id) & Q(cart_user= request.user))
        c.delete()
        amount = 0.0
        shipping_amount= 80.0
        cart_product = [p for p in Cart.objects.all() if p.cart_user == request.user]

        for p in cart_product:
            temp_amount= (p.cart_product.discounted_price) * (p.quantity)
            amount += temp_amount
    

        data = {
            'amount': amount, 
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

def handle_not_found(request, exception):
    return render(request, '404.html')

@login_required
def payment_method(request):
    cart= Cart.objects.filter(cart_user= request.user)
    user = request.user
    custid = request.GET.get('custid')
    print(custid)
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(cart_user = user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product = c.cart_product, quantity= c.quantity).save()
        c.delete()
        return redirect('orders')

@login_required
def orders(request):
    profile = Customer.objects.filter(user=request.user)
    cart= Cart.objects.filter(cart_user= request.user)
    op = OrderPlaced.objects.filter(user= request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(cart_user = request.user))
    return render(request, 'orders.html', {'order_placed': op, 'active': 'nav-link', 'profile': profile, 'cart': cart, 'totalitem': totalitem})


def aboutus(request):
    if request.user.is_authenticated:
        profile = Customer.objects.filter(user=request.user)
        cart= Cart.objects.filter(cart_user= request.user)
        totalitem = len(Cart.objects.filter(cart_user = request.user))
        return render(request, 'about-us.html', {'totalitem': totalitem, 'profile': profile, 'cart': cart, 'about': 'nav-link'})
    else:
        return render(request, 'about-us.html', {'about': 'nav-link'})

def contact(request):
    if request.user.is_authenticated:
        cart= Cart.objects.filter(cart_user= request.user)
        profile = Customer.objects.filter(user=request.user)
        totalitem = len(Cart.objects.filter(cart_user = request.user))
        return render(request, 'contact.html', {'totalitem': totalitem, 'profile': profile, 'cart': cart, 'cont': 'nav-link'})
    else:
        return render(request, 'contact.html', {'cont': 'nav-link'})

def search(request):
    query = request.GET['query']
    url = request.META.get('HTTP_REFERER')

    if request.user.is_authenticated:
        cart= Cart.objects.filter(cart_user= request.user)
        profile = Customer.objects.filter(user=request.user)
        totalitem = len(Cart.objects.filter(cart_user = request.user))

    if len(query) > 20:
        search_item = []

    elif query==' ' or query =='':
        return redirect(url)

    else:
        search_item_by_title = Product.objects.filter(title__icontains = query)
        search_item_by_brand = Product.objects.filter(brand__icontains = query)
        search_item_by_desc = Product.objects.filter(description__icontains = query)
        search_item = search_item_by_title.union(search_item_by_brand, search_item_by_desc)

    return render(request, 'search.html', {'search_item': search_item, 'query': query, 'active': 'nav-link', 'cart': cart, 'totalitem': totalitem, 'profile': profile})

def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("/")

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

