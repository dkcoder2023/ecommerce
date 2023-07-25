from django.shortcuts import render,redirect
from django.views import View
from app.models import Product,OrderPlace,Customer,Cart,Category,ProductImages,Banner,User
from django.contrib import messages
from django.db.models import Q
# from django.contrib.auth.models import User 
from django.core.mail import send_mail
import random
import http.client
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth import authenticate, login,logout


from django.contrib.auth.decorators import login_required ,permission_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totalitem=0
        product=Product.objects.all()
        Categories = Category.objects.all()

        banner=Banner.objects.all()
        # search=request.GET.get('search'="")
         
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))

        return render(request,'home.html',{'Categories':Categories,'product':product,'totalitem':totalitem,'banner':banner})


class ProductDetailView(View):
    def get(self,request,id):
        totalitem=0
        product=Product.objects.get(id=id)
        productimg=ProductImages.objects.filter(product=product)
        print(productimg)

        Categories = Category.objects.all()
       
        item_already_in_cart = False
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))
            item_already_in_cart =Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'productdetail.html',{'product':product ,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem,'productimg':productimg,'Categories':Categories})


class SingleCatProductView(View):
    def get(self, request,data=None):
        totalitem=0
        CategaryId=request.GET.get('category')

        Categories = Category.objects.all()
        product=Product.objects.filter(category=CategaryId)
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))
        # if data==None:
        #     product=Product.objects.filter(category=CategaryId)
        # elif data=='samsang' or data=='redmi':
        #     product=Product.objects.filter(category=CategaryId).filter(brand=data)
        
        # elif data=='below':
        #     product=Product.objects.filter(category=CategaryId).filter(selling_price__lt='10000')

        # elif data =='above':
        #     product=Product.objects.filter(category=CategaryId).filter(selling_price__gte='10000')
        return render(request, 'products.html', {'product':product,'totalitem':totalitem,'Categories':Categories})



@login_required(login_url='login')
def add_to_cart(request):
        
        user=request.user
        product_id=request.GET.get('pro_id')
        print(product_id)
        product=Product.objects.get(id=product_id)
        # Cart(user=user , product=product).save()
        if Cart.objects.filter(product = product).exists():
            return redirect('cart')
        else:
            Cart(user=user , product=product).save()
        return redirect('cart')
                
    
@method_decorator(login_required, name='dispatch')
class ShowCartView(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))

            user= request.user
            carts=Cart.objects.filter(user=user)
            amount=0.0
            shipping_amount=70
            totalamount=0.0

            cart_product=[p for p in Cart.objects.all() if p.user==user]
            if cart_product:
                for p in cart_product:
                    temamount=(p.quantity * p.product.discount_price)
                    amount += temamount
                    totalamount=amount+shipping_amount

                return render(request,'addtocart.html',{'carts':carts,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
            else:
                return render(request,'emptycart.html',{'totalitem':totalitem})
       
           

class PlusCartView(View):
    def get(self, request):
        if request.method =='GET':
            prod_id=request.GET['prod_id']
            print(prod_id)
            c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          


            c.quantity+=1
            c.save()
            amount=0.0
            shipping_amount=70
            totalamount=0.0
            cart_product=[p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                temamount=(p.quantity * p.product.discount_price)
                amount += temamount
            totalitem=0
            if request.user.is_authenticated: 
               totalitem=len(Cart.objects.filter(user=request.user))  
                
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount,
                'totalitem':totalitem
            }
            return JsonResponse(data)


class MinusCartView(View):
    def get(self, request):
        if request.method =='GET':
            prod_id=request.GET['prod_id']
            print(prod_id)
            c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    
            c.quantity-=1
            c.save()
            amount=0.0
            shipping_amount=70
            totalamount=0.0
            cart_product=[p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                temamount=(p.quantity * p.product.discount_price)
                amount += temamount
            totalitem=0
            if request.user.is_authenticated: 
               totalitem=len(Cart.objects.filter(user=request.user))
              
                
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount,
                'totalitem':totalitem
            }
            return JsonResponse(data)



class RemoveCartView(View):
    def get(self, request):
        if request.method =='GET':
            prod_id=request.GET['prod_id']
            print(prod_id)
            c=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
            c.delete()
        
            amount=0.0
            shipping_amount=70
            totalamount=0.0
            cart_product=[p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                temamount=(p.quantity * p.product.discount_price)
                amount += temamount   
            data={
                
                'amount':amount,
                'totalamount':amount+shipping_amount,
            }
            return JsonResponse(data)
         

@login_required(login_url='login') 
def buy_now(request):
    return render(request, 'buynow.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated: 
           totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'profile.html',{'totalitem':totalitem})

    def post(self,request):
        if request.method == 'POST':
            get_user=request.user
            name = request.POST.get('name')
            locality = request.POST.get('locality')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
        
            reg=Customer(user=get_user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()

            context = {'message' : 'Congratulations!! Profile Updated Successfully' , 'class' : 'success', 'active':'btn-primary'}
            
        return render(request, 'profile.html' ,context)


class AddressView(View):
     def get(self, request):
        totalitem=0
        address=Customer.objects.filter(user=request.user)
        if request.user.is_authenticated: 
           totalitem=len(Cart.objects.filter(user=request.user))
        
        return render(request, 'address.html',{'address':address , 'active':'btn-primary','totalitem':totalitem})

@login_required(login_url='login') 
def orders(request):
    totalitem=0
    op =OrderPlace.objects.filter(user=request.user)
    if request.user.is_authenticated: 
           totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'orders.html',{'order_place':op,'totalitem':totalitem})


@login_required(login_url='login') 
def change_password(request):
 return render(request, 'changepassword.html')



class MessageHandler:
    mobile=None 
    otp=None
    def __init__(self,mobile,otp) -> None:
        self.mobile=mobile
        self.otp=otp

    def send_otp(self):     
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{self.mobile}')
        return None


def login_attempt(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email = email).first()
        
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'login.html' , context)
        
        # otp = str(random.randint(1000 , 9999))
        # user.otp = otp
        user.save()
        send_otp_via_mail(email)

        # send_otp(mobile , otp)
        # MessageHandler(mobile, otp).send_otp()
        request.session['email'] = email
        return redirect('login_otp')        
    return render(request,'login.html')


def login_otp(request):
    email = request.session['email']
    context = {'email':email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        
        
        if otp == user.otp:
            user = User.objects.get(id = user.id)
            
        

            login(request , user)
            return redirect('profile')
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','email':email }
            return render(request,'login_otp.html' , context)
    
    return render(request,'login_otp.html' , context)
    
def send_otp_via_mail(email):
    subject="Your account varification email"
    otp=random.randint(1000,9999)
    message=f'Your otp is {otp}'
    email_from=settings.EMAIL_HOST
    print(email)
    send_mail(subject,message,email_from,[email])
    user_obj=User.objects.get(email= email)
    user_obj.otp = otp
    user_obj.save()    

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')

        check_user = User.objects.filter(email = email).first()
        check_profile = User.objects.filter(mobile = mobile).first()
        
        if check_user or check_profile:
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'register.html' , context)
        
        user = User.objects.create(email = email,username=username,mobile=mobile)
        user.save()
        send_otp_via_mail(email)


        # otp = str(random.randint(1000 , 9999))
        # User = User(user = user , mobile=mobile , otp = otp) 
        # User.save()
        # # send_otp(mobile, otp)
        # MessageHandler(mobile, otp).send_otp()
        request.session['email'] = email
        return redirect('otp')
    return render(request,'register.html')



def otp(request):
    email = request.session['email']
    context = {'email':email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        
        if otp == user.otp:
            context = {'message' : 'Congratulations!! Registered Successfully' , 'class' : 'success','email':email }
            return render(request,'register.html' , context)
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','email':email }
            return render(request,'otp.html' , context)
            
        
    return render(request,'otp.html' , context)


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")


@login_required(login_url='login') 
def checkout(request):
    profile=Customer.objects.filter(user=request.user)
    if profile:
        user=request.user
        add=Customer.objects.filter(user=user)
        
        cart_item=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temamount=(p.quantity * p.product.discount_price)
                amount += temamount
            totalamount=amount + shipping_amount
        totalitem=0
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))

        return render(request, 'checkout.html',{'add':add,'cart_item':cart_item,'totalamount':totalamount,'totalitem':totalitem})
    else:
        return redirect('profile')

@login_required(login_url='login') 
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart= Cart.objects.filter(user=user)
    for c in cart :
        OrderPlace(user=user, customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()

    return redirect('orders')





@login_required(login_url='login') 
def delete_cust_detail(request, id):
    cust = Customer.objects.filter(id=id)
    cust.delete()
    return redirect('profile')



