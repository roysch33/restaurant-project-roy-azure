from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,authenticate, logout

from .models import Cart, Item, Delivery
from management.models import Category, Dish

# Create your views here.

def main(request):
    return render(request, 'customers/main.html')

# user
def login_user(request):
    not_ok = False
    if request.user.is_authenticated:
        return redirect('menu') # אם יש לך קוקי מחובר - יזרוק לאתר של המשתמש
    if request.method == 'POST':
        user = authenticate(request, 
                            username=request.POST['username'], 
                            password = request.POST['password']
                            )
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect ('manager-page')
            else:
                return redirect ('menu')
        else:
            not_ok=True
    return render(request,'customers/login.html', {"not_ok":not_ok})


def signup(request):
    errors = {"field_required":"שדה זה חובה.","username_must_be_long":"על שם המשתמש להכיל לפחות 8 תווים.", "password_must_be_long":"על הסיסמה להכיל לפחות 8 תווים.","not_unique":"שם משתמש זה תפוס, אנא בחר שם משתמש אחר", "not_valid_email":"אנא בחר כתובת מייל תקינה"}
    error = False
    error2 = False
    users = User.objects.all()
    unique = True
    the_username = ""
    the_password = ""
    the_first_name = ""
    the_last_name = ""
    the_email = "" 
    email_check = True
    if request.method == 'POST':
        the_username = request.POST['username']
        the_password = request.POST['password']
        the_first_name = request.POST['first_name']
        the_last_name = request.POST['last_name']
        the_email = request.POST['email'] 
        if "@" not in the_email:
            the_email = ""
            email_check = False
        if len(the_username) < 8 :
            error = 'short_name'
        if len(the_password) < 8:
            error2 = 'short_password'
        for one_user in users:
            if one_user.username == the_username:
                unique = False
        if unique == True and error != 'short_name' and error != 'short_password':
            if len(the_username) == 0 or len(the_password) == 0 or len(the_first_name) == 0 or len(the_last_name) == 0 or len(the_email) == 0:
                pass
            else:
                new_user = User(
                    username = the_username,
                    password = make_password(the_password),
                    first_name = the_first_name,
                    last_name = the_last_name,
                    is_staff = False,
                    email = the_email
                )
                new_user.save()
                new_cart = Cart (
                        user_id = new_user
                    )
                new_cart.save()
                return redirect ('login')
    return render(request,'customers/signup.html', {"errors":errors, "error":error, "error2":error2, "unique":unique,"the_username":the_username,"the_password":the_password, "the_first_name":the_first_name, "the_last_name":the_last_name, "the_email":the_email, "email_check":email_check})

@login_required(login_url='main')
def edit_user(request, id, username):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.password = make_password(request.POST['password'])
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.email=request.POST['email']
        user.save()
        return redirect('menu')
    return render(request,'customers/edit_user.html', {'user':user})


@login_required(login_url='main')
def logout_user(request):
    logout (request)
    return redirect ('login')


@login_required(login_url='main')
def menu(request):
    categories = Category.objects.all()
    return render(request,'customers/menu.html', {'categories':categories})



@login_required(login_url='main')
def show_category(request, id, category_name):
    category = Category.objects.get(id=id)
    dishes = Dish.objects.all()
    amounts = []
    num1 = 1
    while num1 <= 50:
        amounts.append(num1)
        num1 += 1
    if request.method == 'POST':
        dish = Dish.objects.get(id=request.POST['dish'])
        carts = Cart.objects.all()
        items = Item.objects.all()
        last_cart_id = 0
        for cart in carts:
            if cart.user_id == request.user:
                if last_cart_id < cart.id:
                    last_cart_id = cart.id
                    last_cart = Cart.objects.get(id=last_cart_id)
        item_not_in_cart = 0
        for item in items:
            if item.cart_id == last_cart:
                if item.dish_id == dish:
                    item.amount += int(request.POST['amount'])
                    item.save()
                    item_not_in_cart = 1
        if item_not_in_cart == 0:
            new_item = Item(
                    cart_id = last_cart,
                    dish_id = dish,
                    amount = int(request.POST['amount'])
                )
            new_item.save()
        return redirect('menu')
    
    return render(request,'customers/show_category.html', {'category':category, 'dishes':dishes, "amounts":amounts})



# cart


@login_required(login_url='main')
def show_cart(request):
    carts = Cart.objects.all()
    items = Item.objects.all()
    full_amount = 0
    last_cart_id = 0
    user_doesnt_have_a_cart = 0
    for cart in carts:
        if cart.user_id == request.user:
            if last_cart_id < cart.id:
                last_cart_id = cart.id
                last_cart = Cart.objects.get(id=last_cart_id)
                user_doesnt_have_a_cart = 1
    for item in items:
        if item.cart_id== last_cart:
            sum_item_amount = item.dish_id.price * item.amount
            full_amount += sum_item_amount
    items = Item.objects.all()
    dishes = Dish.objects.all()

    return render(request,'customers/show_cart.html', {'items':items, "dishes":dishes, "user_doesnt_have_a_cart":user_doesnt_have_a_cart,"cart":last_cart, "full_amount":full_amount })

@login_required(login_url='main')
def delete_item_in_cart(request, id, item_name):
    item = Item.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('show-cart')

# delivery
@login_required(login_url='main')
def show_delivery(request, id):
    cart = Cart.objects.get(id=id)
    if request.method == 'POST':
        new_delivery = Delivery(
            order_id = cart,
            address = request.POST['address'],
            comment = request.POST['comment'],
        )
        new_delivery.save()
        new_cart = Cart (
                user_id = request.user
            )
        new_cart.save()
        return redirect('menu')
    return render(request,'customers/show_delivery.html', {"cart":cart})


@login_required(login_url='main')
def order_history(request):
    deliveries = Delivery.objects.all()
    carts = Cart.objects.all()
    user_carts = []
    user_deliveries = []
    for cart in carts:
         if cart.user_id == request.user:
              user_carts.append(cart)
    for delivery in deliveries:
        for cart in user_carts:
            if delivery.order_id == cart:
                 user_deliveries.append(delivery)

    return render(request,'customers/order_history.html', {'user_deliveries':user_deliveries, 'deliveries':deliveries,'user_carts':user_carts})
