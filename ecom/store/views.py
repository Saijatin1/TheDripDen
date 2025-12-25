from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
def search(request):
    default_products = Product.objects.all().order_by('-id')[:4]  # latest 4 as fallback

    if request.method == 'POST':
        query = request.POST.get('searched', '').strip()

        if query:
            searched = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
            )

            if searched.exists():
                # case 2: show search results
                return render(request, 'search.html', {
                    'searched': searched,
                    'query': query,
                })
            else:
                # case 3: no results found → show default products
                messages.warning(request, "That product does not exist")
                return render(request, 'search.html', {
                    'searched': None,
                    'default_products': default_products,
                    'query': query,
                })

    # case 1: GET request → only default products
    return render(request, 'search.html', {
        'default_products': default_products,
    })


def update_info(request):
    if request.user.is_authenticated:
        current_user, created = Profile.objects.get_or_create(user=request.user)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated.")
            return redirect('home')

        return render(request, 'update_info.html', {'form': form})
    
    else:
        messages.error(request, "You must be logged in to access that page.")
        return redirect('home')




    return render(request,'update_info.html',{})    


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated.")
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')  # ← indent was wrong

        else:
            form = ChangePasswordForm(current_user)  # fixed variable name
            return render(request, 'update_password.html', {'form': form})  # fixed variable name

    else:
        messages.error(request, "You must be logged in to access that page.")
        return redirect('home' )
         
    

def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None,instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request,"user has been updated")
            return redirect('home')
        return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.success(request,"u must be loggedin to acess that page")
        return redirect('home')



    return render(request,'update_user.html',{})        

     

def category(request,foo):
    foo=foo.replace('-',' ')
    try:
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})        
    except:
        messages.success(request,('that category doesnt exist'))
        return redirect('home')

def category_summary(request):
    categories=Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})  

def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method=="POST":
        username=request.POST['Username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)

            current_user = Profile.objects.get(user__id=request.user__id)
            #getting the saved cart from the database
            saved_cart=current_user.old_cart
            if saved_cart:
                #convert to dict with json
                converted_cart=json.loads(saved_cart)
                #add the loaded dictionary
                cart=Cart(request)
                #looping and adding 
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)


            messages.success(request,("you have been logged in"))
            return redirect('home')
        else:
            messages.success(request,("Invalidcredientials"))
            return redirect('login')
    
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect('home')



def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "Account created successfully! Please complete your profile.")
            return redirect('update_info')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    

