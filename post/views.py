from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from . models import Bpost,Category,Cart,CartItem,Comment,CustomerFeedback,Clients,Order
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.


# def index(request):
    # search =request.GET.get("search","")
    # posts =list( Bpost.objects.filter(Q(title__icontains=search) | Q(description__icontains=search)).values())
    # posts = Bpost.objects.all()
    # posts_json = serializers.serialize('json', posts)
    # return JsonResponse(posts_json, safe=False)
    # return render(request,"index.html",{"posts":posts})

def postdetails(request,id):
    posts = Bpost.objects.get(id=id)
    comments = Comment.objects.filter(post=posts)
    return render(request,'postDetails.html',{'posts':posts,'comments': comments})


def index(request):
    search =request.GET.get("search","")
    clients = Clients.objects.all()
    categories = Category.objects.filter(status=True)
    category_posts_data = {}
    for category in categories:
        posts = Bpost.objects.filter(category=category)
        category_posts_data[category] = posts.filter(Q(title__icontains=search) | Q(description__icontains=search))[:4]

    return render(request, 'index.html', {'category_posts_data': category_posts_data, 'clients':clients})
    

def CategoryPost(request,id):
    category = get_object_or_404(Category, id=id)
    posts = Bpost.objects.filter(category=category)

    return render(request, 'CategoryDetails.html', {'category': category, 'posts': posts})
    

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=='POST':
        first_name=request.POST.get('first')
        last_name=request.POST.get('last')
        email=request.POST.get('email')
        username=request.POST.get('username')
        passw=request.POST.get('password1')
        data=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=passw)
        data.save()
        return redirect('login')
    return render(request,'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')



@login_required
def add_to_card(request,product_id):
    product = get_object_or_404(Bpost,id = product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart =cart,product = product)
   
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart,user = request.user)
    cart_item = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total_price() for item in cart_item)
    return render(request, 'cart.html', {'cart_items': cart_item, 'total': total})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')



@login_required
def add_comment(request, post_id):
    posts = get_object_or_404(Bpost, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content:
            comment = Comment(post=posts, author=request.user, content=content)
            comment.save()
            return redirect('postDetails', id=posts.id)
    
    return render(request, 'postDetails.html', {'posts': posts})

@login_required
def Feedback(request):
    if request.method =='POST':
        feedback = request.POST.get('feedback')
        if feedback:
            fb = CustomerFeedback(feedback=feedback,customer =request.user)
            fb.save()
            return redirect('contact')
        
    return redirect('contact')



def Contact(request):
    return render(request,'Contact.html')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total_price() for item in cart_items)
    if request.method == 'POST':
        
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            CartItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        # Clear the cart
        cart_items.delete()
        return redirect('cart', order_id=order.id)
    return render(request, 'checkout.html', {'cart_items': cart_items,'total':total})

@login_required
def send_email(request):
    # Assuming cart_items and total are already defined in your checkout view
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total_price() for item in cart_items)
    
    # Send email to the user
    subject = 'Order Confirmation'
    message = f'Thank you for your order! Your total is {total}.'
    from_email = settings.EMAIL_HOST_USER
    to_email = [request.user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)
    
    return HttpResponse('Email sent')

def Checkout(request):
    return render(request,'checkout.html')

