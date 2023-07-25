from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import (
    UserManager
)


class User(AbstractUser):
    username = models.CharField(max_length=50,unique=True)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_verified =models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True,blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects=UserManager()

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return str(self.email)




# state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

# class CustomUser(AbstractUser):
#     username = models.CharField(max_length=256)
#     email = models.EmailField(unique=True)
#     mobile = models.CharField(max_length=20)
#     otp = models.CharField(max_length=6)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ('username',)

    

#     class Meta:
#         verbose_name_plural = "User"
   
#     def __str__(self):
#         return str(self.username)







class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=255)
    locality=models.CharField(_("locality"), max_length=255)
    city=models.CharField(_("city"), max_length=150)
    zipcode=models.IntegerField(_("zipcode"))
    state=models.CharField(_("state"),max_length=255)
    
    def __str__(self):
        return str(self.id)


# categary_choices=(

#     ('M','Mobile'),
#     ('L','Laptop'),
#     ('TW','Top Wear'),
#     ('BW','Bottom Wear')
# )

class Category(models.Model):
    category=models.CharField(_("category"), max_length=150)
    def __str__(self):
        return str(self.category)

# class SubCategory(models.Model):
#     category=models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory=models.CharField(_("subcategory"), max_length=150)
#     def __str__(self):
#         return str(self.category)


class Product(models.Model):
    title=models.CharField(_("title"), max_length=150)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    discription=models.TextField(_("discription"))
    brand=models.CharField(_("brand"),max_length=255)
    category=models.ForeignKey(Category, related_name='pro_cat',on_delete=models.CASCADE)
    product_image=models.ImageField(_("product_image"), upload_to='producting')

    def __str__(self):
        return str(self.title)


    
 
    
class Cart(models.Model):
    user=models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    product=models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(_("quantity"),default=1)
    
    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
status_choices=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)
class OrderPlace(models.Model):
    user=models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, verbose_name=_("customer"), on_delete=models.CASCADE)
    product=models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(_("quantity"),default=1)
    ordered_date=models.DateTimeField(_("ordered_date"), auto_now_add=True)
    status=models.CharField(_("status"),choices= status_choices,max_length=50,default='Pending')
    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

# class Profile(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     mobile = models.CharField(max_length=20)
#     otp = models.CharField(max_length=6)
#     def __str__(self):
#         return str(self.user)


#     def get_count(self):
#         return Cart.objects.filter(user=self.user).count()

class ProductImages(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    multiple_image=models.ImageField(upload_to='multiple_image')
    def __str__(self):
        return str(self.product)


class Banner(models.Model):
    banner=models.ImageField(upload_to='banner')
    def __str__(self):
        return str(self.banner)

        