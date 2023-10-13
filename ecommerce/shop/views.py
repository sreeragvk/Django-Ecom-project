from django.shortcuts import render
from shop.models import category,Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def allprodcat(request):
    c=category.objects.all()
    return render(request,'category.html',{'c':c})
def allproduct(request,c):
    p=Product.objects.filter(category__cname=c)
    Category=category.objects.get(cname=c)
    return render(request,'products.html',{'p':p,'category':Category})

def detail(request,p):
    d=Product.objects.get(pname=p)
    return render(request,'detail.html',{'d':d})
def register(request):
    if request.method=="POST":
        u=request.POST['u']
        p1=request.POST['p1']
        p2=request.POST['p2']
        f=request.POST['f']
        l=request.POST['l']
        e=request.POST['e']
        if(p1==p2):
            u=User.objects.create_user(username=u,password=p1,first_name=f,last_name=l,email=e)
            u.save()
            return allprodcat(request)
    return render(request,'register.html')
def user_login(request):
    if request.method=='POST':
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return allprodcat(request)
        else:
            messages.error(request,"invalid credentials")
    return render(request,'login.html')
@login_required
def user_logout(request):
    logout(request)
    return user_login(request)