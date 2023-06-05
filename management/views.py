from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from customers.models import Delivery
from .models import Dish, Category
# Create your views here.


# managers 
def manager_signup (request):
    errors = {"field_required":"שדה זה חובה.","username_must_be_long":"על שם המשתמש להכיל לפחות 8 תווים.", "password_must_be_long":"על הסיסמה להכיל לפחות 8 תווים.","not_unique":"שם משתמש זה תפוס, אנא בחר שם משתמש אחר", "not_valid_email":"אנא בחר כתובת מייל תקינה","manager_code_wrong":"קוד סודי שהוזן אינו תקין"}
    error = False
    error2 = False
    users = User.objects.all()
    unique = True
    the_username = ""
    the_password = ""
    the_first_name = ""
    the_last_name = ""
    the_email = "" 
    the_manager_code = ""
    email_check = True
    if request.method == 'POST':
        the_username = request.POST['username']
        the_password = request.POST['password']
        the_first_name = request.POST['first_name']
        the_last_name = request.POST['last_name']
        the_email = request.POST['email'] 
        the_manager_code = request.POST['manager_code']
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
                if the_manager_code == "123123":
                    new_manager = User(
                    username = the_username,
                    password = make_password(the_password),
                    first_name = the_first_name,
                    last_name = the_last_name,
                    is_staff = True,
                    email = the_email
                    )
                    new_manager.save()
                    return redirect ('login')
    return render(request,'management/manager_signup.html', {"errors":errors, "error":error, "error2":error2, "unique":unique,"the_username":the_username,"the_password":the_password, "the_first_name":the_first_name, "the_last_name":the_last_name, "the_email":the_email,"the_manager_code":the_manager_code, "email_check":email_check})


@login_required(login_url='main')
def manager_page(request):
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    return render(request,'management/manager_page.html')
    

# delivery    
@login_required(login_url='main')
def manager_deliveries(request):
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    deliveries = Delivery.objects.all()
    if request.method == 'POST':
        delivery = request.POST['delivery']
        change_delivery = Delivery.objects.get(order_id=delivery)
        if change_delivery.is_delivered == True:
            change_delivery.is_delivered = False
        else:
            change_delivery.is_delivered = True
        change_delivery.save()
        
    return render(request,'management/manager_deliveries.html', {'deliveries':deliveries})


# catagories
@login_required(login_url='main')
def manager_categories(request):
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    categories = Category.objects.all()    
    return render(request,'management/manager_categories.html', {'categories':categories})

@login_required(login_url='main')
def edit_category(request, id, category_name):
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.image = request.POST['image']
        category.save()
        return redirect('manager-categories')
    return render(request,'management/edit_category.html', {'category':category})    

@login_required(login_url='main')
def add_category(request):
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    if request.method == 'POST':
        new_category = Category (
            name = request.POST['name'],
            image = request.POST['image']
        )
        new_category.save()
        return redirect('manager-page')
    return render(request,'management/add_category.html')    

def delete_category(request,id, category_name):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('manager-categories')


# dishes
@login_required(login_url='main')
def show_dishes(request, id, category_name): 
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    category = Category.objects.get(id=id)
    dishes = Dish.objects.all()
    return render(request,'management/show_dishes.html', {'category':category, 'dishes':dishes})

@login_required(login_url='main')
def edit_dish(request, id, dish_name):
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    dish = Dish.objects.get(id=id)
    categories = Category.objects.all()
    category_id=""
    if request.method == 'POST':
        category = Category.objects.get(id=request.POST['category_id'])
        if request.POST['is_gluten_free'] == 'on':
            gluten_free = True
        else:
            gluten_free = False
        if request.POST['is_vegeterian'] == 'on':
            vegeterian = True
        else:
            vegeterian = False
        dish.dish_name = request.POST['dish_name']
        dish.price = request.POST['price']
        dish.description=request.POST['description']
        dish.image=request.POST['image']
        dish.is_gluten_free=gluten_free
        dish.is_vegeterian=vegeterian
        dish.category_id= category
        dish.save()
        return redirect('manager-categories')
    return render(request,'management/edit_dish.html', {'dish':dish, 'categories':categories, "category_id":category_id})

@login_required(login_url='main')
def add_dish(request, ):
    if request.user.is_staff == False:
        return render(request,'management/not_staff.html')
    categories = Category.objects.all()
    if request.method == 'POST':
        category = Category.objects.get(id=request.POST['category_id'])
        if request.POST.get('is_gluten_free') == 'on':
            gluten_free = True
        else:
            gluten_free = False
        if request.POST.get("is_vegeterian") == 'on':
            vegeterian = True
        else:
            vegeterian = False
        
        new_dish = Dish (
            dish_name = request.POST['dish_name'],
            price = request.POST['price'],
            description=request.POST['description'],
            image=request.POST['image'],
            is_gluten_free=gluten_free,
            is_vegeterian=vegeterian,
            category_id= category
        )
        new_dish.save()
        return redirect('manager-page')
    return render(request,'management/add_dish.html', {"categories":categories})


def delete_dish(request,id, dish_name):
    dish = Dish.objects.get(id=id)
    if request.method == 'POST':
        dish.delete()
        return redirect('manager-categories')