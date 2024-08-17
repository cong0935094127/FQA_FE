from django.shortcuts import redirect, render
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login,  logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart



def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        #Query The Products DB Model

        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "Sản phẩm đó không tồn tại...Vui lòng thử lại.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})



def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Thông tin của bạn đã được cập nhật!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form})
    else:
        messages.success(request, "Bạn phải đăng nhập để truy cập trang đó!")
        return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
           form = ChangePasswordForm(current_user, request.POST)
           
           if form.is_valid():
               form.save()
               messages.success(request, "Mật khẩu của bạn đã được cập nhật...")
            
               return redirect('update_user')
           else:
               for error in list(form.errors.values()):
                   messages.error(request, error)
                   return redirect('update_password')
               

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "Bạn phải đăng nhập để xem trang đó...")
        return redirect('home')




def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Người dùng đã được cập nhật!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "Bạn phải đăng nhập để truy cập trang đó!")
        return redirect('home')



def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})

def category(request,foo):
    foo = foo.replace('-','')
    print('check foood ::: ', foo)
    #
    try:
        category = Category.objects.get(name=foo)
        product = Product.objects.filter(category=category)
        print("check cate gory and product", category, product)
        return render(request, 'category.html', {'products':product, 'category':category})
    except:
        messages.success(request, ("Danh mục đó không tồn tại..."))
        return redirect('home')    



def product(request,pk):
    products = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':products})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, ("Bạn đã đăng nhập thành công"))
            return redirect('home')
        else:
            messages.success(request, ("Đã xảy ra lỗi, xin vui lòng thử lại"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Bạn đã đăng xuất...cảm ơn vì đã ghé qua cửa hàng Công Fish"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Tên người dùng đã được tạo - Vui lòng điền thông tin người dùng của bạn bên dưới..."))
            return redirect('update_info')
        else:
            messages.success(request, ("Rất tiếc! Đã xảy ra sự cố khi đăng ký, vui lòng thử lại..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
