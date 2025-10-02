from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import Registeruser,CustomerProfileForm, MyPasswordChangeForm
from .models import Usef
from django.contrib.auth.models import User
import string
import random
import decimal
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import SubCatg,Catg,prod_type,prodss,Customer,Cart,Orders,Buynow
from django.views import View
from django.urls import reverse_lazy,reverse
import stripe
from django.conf import settings
from .forms import SearchForm

# Create your views here.

def home(request):
    return render(request,'app/index.html')

def loginpage(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        validuser=authenticate(request,username=uname,password=pwd)
        if validuser!=None:
            login(request,validuser)
            return redirect('homeurl')
        else:
            return redirect('loginurl')
    return render(request,'app/login.html')

@login_required(login_url='loginurl')
def logoutpage(request):
    logout(request)
    return redirect('homeurl')

def signupPage(request):
    if request.method =='POST':
        dataform = Registeruser()
    
        # otp to signup 
        email = request.POST['email']

        Usef.otp = generate_otp()
        subject = 'User Signup OTP'
        message = f'Your OTP for email verification is: {Usef.otp}'
        from_email = 'poojithakatakam2@gmail.com' 
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return render(request,'app/register.html',{'form':dataform,'email':email})

    return render(request, 'app/signup.html')

def registerpage(request):
    empty=Registeruser()
    if request.method=='POST':
        df=Registeruser(request.POST)
        otp= request.POST['otp']
        if Usef.otp ==otp:
            Usef.otp =''

            if df.is_valid()==True:
                df.save()
                messages.success(request,'User Created Successfully')
                return redirect('loginurl')
            else:
                messages.error(request,'User Creation Failed')
                messages.error(request,df.errors)
                return render(request,'app/signup.html',{'form':df, 'errors':df.errors,})  
        else:
            error = "Invalid OTP"
            return render(request, 'app/register.html',{'form':df,'errors':error})
    return render(request,'app/register.html',{'form':empty})



def generate_otp(length=6):
    chars = string.digits + string.ascii_uppercase
    otp = ''.join(random.choice(chars) for _ in range(length))
    return otp



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = get_user_model().objects.get(email=email)
            Usef.otp = generate_otp()
            Usef.save()
            user.save()  # Save the generated OTP

            # Send email with OTP
            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {Usef.otp}'
            from_email = 'krishnabadham@gmail.com'  # Replace with your email
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return render(request, 'app/forget.html', {'email': email})
        except get_user_model().DoesNotExist:
            
            error="In valid email address"
            return render(request, 'app/forgotpass.html',{'error':error})
    return render(request, 'app/forgotpass.html')

def password_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        try:
            user = get_user_model().objects.get(email=email)
            if Usef.otp == otp:  # Verify OTP
                user.set_password(new_password)  # Set new password 
                Usef.otp = ''
                Usef.save()
                user.save()
                
                return render(request, 'app/reset.html',{'email':email})  
            else:
                
                error="Invalid OTP"
                return render(request, 'app/forget.html',{'error':error,'email':email})
        except get_user_model().DoesNotExist:
            
            error='User does not exits with this email'
            return render(request, 'app/forgotpass.html',{'error':error})
    return render(request, 'app/forget.html')


# def subcategory_list(request,category_id):
    # subcategories = SubCatg.objects.filter(category_id=category_id)
    # return render(request, 'app/subcategory_list.html', {'subcategories': subcategories})
# def subcategory_detail(request, category_id, subcategory_id):
#     category = Catg.objects.get(pk=category_id)
#     subcategory = SubCatg.objects.get(pk=subcategory_id, category=category)
#     product_types = prod_type.objects.filter(categories=subcategory)
#     return render(request, 'app/subcategory_list.html', {'category': category, 'subcategory': subcategory, 'product_types': product_types})

# def c1(request):
#     subcatego = SubCatg.objects.get(name='CZ')
#     data=prodss.objects.filter(subcategory=subcatego)
#     p1=prod_type.objects.all()
#     return render(request,'app/c1.html',{'data':data,'names':p1})

# def c2(request):
#     subcatego = SubCatg.objects.get(name='1 Gram Gold')
#     data=prodss.objects.filter(subcategory=subcatego)
#     return render(request,'app/c1.html',{'data':data,'name':subcatego.name})


def c_view(request, subcategory):
    try:
        subcatego = SubCatg.objects.get(name=subcategory)
    except SubCatg.DoesNotExist:
        return render(request, 'app/c1.html', {'error': 'Subcategory not found'})

    data = prodss.objects.filter(subcategory=subcatego)
    p1 = prod_type.objects.filter(categories=subcatego)

    no_data_message = "No Data Found"
    if not data.exists():
        no_data_message = "No products found in this subcategory."

    context = {
        'data': data,
        'product_types': p1,
        'subcategory': subcatego,
        'no_data_message': no_data_message,
        'error': None,
    }
    return render(request, 'app/c1.html', context)

def details(request, id):
    uprods = prodss.objects.filter(id=id).first()
    if not uprods:
        return render(request, 'app/uprods.html', {'error': 'Product not found', 'uprods': None})
    return render(request, 'app/uprods.html', {'uprods': uprods, 'error': None})



class ProfileView(View):
    def get(self, request) :
        form = CustomerProfileForm()
        return render (request,'app/address.html',locals())
    def post(self, request):
        form=CustomerProfileForm(request.POST)

        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,zipcode=zipcode)
            reg. save()
            messages. success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render (request,'app/address.html',locals())

@login_required(login_url='loginurl')    
def profile(request) :
    add = Customer.objects.filter(user=request.user)
    return render (request,'app/profile.html', locals())

   
class updateAddress(View):
    def get(self, request, pk):
        add=Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render (request, 'app/updateaddress.html' ,locals())
    def post (self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            
            add.save()
            messages. success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
            return render(request, 'app/updateaddress.html',locals())
        return redirect('profile')

@login_required(login_url='loginurl')  
def changepass(request):
    form = MyPasswordChangeForm(user=request.user)
    if request.method =='POST':
        form=MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            
            form.save()
            messages. success(request, "Congratulations! Password changed Successfully")
            return render(request,'app/changepassdone.html')
        else:
            messages.error(request,form.errors)
            return render(request,'app/changepass.html',locals())
    return render(request,'app/changepass.html',locals())

@login_required(login_url='loginurl')
def cart(request):
    user=request.user
    df=Cart.objects.filter(user=request.user)

    amount =decimal.Decimal(0)
    shipping_amount=decimal.Decimal(50)

    cp= [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    total_amount=amount+shipping_amount
    return render(request,'app/cart.html',locals())

@login_required(login_url='loginurl')
def add_to_cart(request):
    user=request.user
    msg='Add to Cart Successful'
    product_id = request.GET.get('prod_id')
    uprods=prodss.objects.get(id=product_id)
    product = get_object_or_404(prodss,id=product_id)
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    # return redirect('cart')
    return render(request,'app/uprods.html',locals())

@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('cart')

    # detail_url = reverse_lazy('detailurl')
    # success_url = f"{detail_url}?prod_id={product_id}"  # Append product_id as a query parameter

    # return redirect(succes_url)
       
    # return render(request,'app/uprods.html',locals())
@login_required
def checkout(request):
    user=request.user
    addresses=Customer.objects.filter(user=user)
    return render(request,'app/checkout.html',locals())

@login_required
def checkout1(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    address_id=request.GET.get('address')
    address=get_object_or_404(Customer,id=address_id)
    for c in cart:
        Orders(user=user,address=address,product=c.product,quantity=c.quantity).save()
        # Orders.objects.create(user=user, address=address, product=c.product, quantity=c.quantity)
        c.delete()
    return redirect('orders')

@login_required
def orders(request):
    all_orders=Orders.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request,'app/orders.html',{'orders':all_orders})


    
def aboutus(request):
    return render(request,'app/aboutus.html')

def services(request):
    return render(request,'app/services.html')

@login_required(login_url='loginurl')
def add_to_buynow(request, itemid):
    user=request.user
    bn=Buynow.objects.filter(user=user)
    for p in bn:
        p.delete()
    pro=prodss.objects.get(id=itemid)
    Buynow(user=user, product=pro).save()
    a=Buynow.objects.get(product=pro)
    return redirect('buynow',itemid=a.id)


@login_required(login_url='loginurl')
def buynow(request,itemid):    
    user=request.user
    
    a=Buynow.objects.get(id=itemid)

    amount =decimal.Decimal(0)
    shipping_amount=decimal.Decimal(50)

    cp= [p for p in Buynow.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    total_amount=amount+shipping_amount
    return render(request,'app/buynow.html',locals())

def payment(request):
    return render(request,'app/payment.html')


@login_required
def remove_buy(request, item_id):
    if request.method == 'GET':
        c = get_object_or_404(Buynow, id=item_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
        return redirect('homeurl')


@login_required
def plus_buy(request, item_id):
    if request.method == 'GET':
        cp = get_object_or_404(Buynow, id=item_id)
        cp.quantity += 1
        cp.save()
    # return redirect('buynow',item_id=item_id)
    return redirect('buynow',itemid=item_id)


@login_required
def minus_buy(request, item_id):
    if request.method == 'GET':
        cp = get_object_or_404(Buynow, id=item_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('buynow',itemid=item_id)

@login_required
def buycheckout(request):
    user=request.user
    addresses=Customer.objects.filter(user=user)
    return render(request,'app/buycheckout.html',locals())

@login_required
def buycheckout1(request):
    user=request.user
    buy = Buynow.objects.filter(user=user)
    address_id=request.GET.get('address')
    address=get_object_or_404(Customer,id=address_id)
    for c in buy:
        Orders(user=user,address=address,product=c.product,quantity=c.quantity).save()
        # Orders.objects.create(user=user, address=address, product=c.product, quantity=c.quantity)
        c.delete()
    return redirect('orders')

def search_view(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            product = form.cleaned_data.get('product')
            
            # Filter products based on search parameters
            products = prodss.objects.all()
            products = products.filter(name__icontains=product)
            
            return render(request, 'app/search.html', {'products': products, 'form': form})
    else:
        form = SearchForm()
    return render(request, 'app/search.html', {'form': form})

def sort_view(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on the price range
    products = prodss.objects.all()
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Sort products by price low to high by default
    sort_by = request.GET.get('sort_by', 'low_to_high')
    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')

    return render(request, 'app/sort.html', {'products': products})
