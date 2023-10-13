from django.shortcuts import render,redirect
from cart.models import Cart,Account,Order
from shop.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request,p):
    product=Product.objects.get(pname=p)
    user=request.user
    try:
        cart=Cart.objects.get(user=user,product=product)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
            cart.save()
    except Cart.DoesNotExist:
        cart=Cart.objects.create(product=product,user=user,quantity=1)
        cart.save()
    return redirect('cart:cart_view')
def cart_view(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    total=0
    for i in cart:
        total+=i.quantity * i.product.price
    return render(request,'cartview.html',{'c':cart,'total':total})

def cart_remove(request,p):
    product=Product.objects.get(pname=p)
    user=request.user
    try:
        cart=Cart.objects.get(user=user,product=product)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return redirect("cart:cart_view")
def full_remove(request,p):
    product=Product.objects.get(pname=p)
    user=request.user
    try:
        cart = Cart.objects.get(user=user, product=product)
        cart.delete()
    except:
        pass
    return redirect("cart:cart_view")
@login_required()
def order_form(request):
    if (request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']
        user=request.user
        cart=Cart.objects.filter(user=user)
        total=0
        for i in cart:
            total+=i.quantity*i.product.price
        acct=Account.objects.get(acctnumber=n)
        if(acct.balance>total):
            acct.balance=acct.balance-total
            acct.save()
            for i in cart:
                o=Order.objects.create(user=user,product=i.product,phone=p,address=a,noofitems=i.quantity,order_status="paid")
                o.save()
                i.product.stock=i.product.stock-i.quantity
                i.product.save()
            cart.delete()
            msg="Order Placed Successfully"


            return render(request,'orderconfirm.html',{'msg':msg})
        else:
            msg="Insufficient Amount.You can't place order"
            return render(request, 'orderconfirm.html',{'msg':msg})

    return render(request,'orderform.html')

def your_orders(request):
    user=request.user
    s=Order.objects.filter(user=user)
    return render(request,'yourorders.html',{'s':s,'u':user.username})





