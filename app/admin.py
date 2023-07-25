from django.contrib import admin
from app.models import User,Customer,Product,Category,ProductImages,Banner,Cart,OrderPlace



class UserAdmin(admin.ModelAdmin):
    model=User
    list_display=['username','mobile','email','otp']
admin.site.register(User,UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    model=Product
    list_display=['title','selling_price','discount_price','discription','brand','category','product_image']
admin.site.register(Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    model= Category
    list_display=['category']

admin.site.register(Category,CategoryAdmin)

# class SubCategoryAdmin(admin.ModelAdmin):
#     model= SubCategory
#     list_display=['category','subcategory']

# admin.site.register(SubCategory,SubCategoryAdmin)

class CartAdmin(admin.ModelAdmin):
    model=Cart
    list_display=['user','product','quantity']

admin.site.register(Cart,CartAdmin)


class OrderPlaceAdmin(admin.ModelAdmin):
    model=OrderPlace
    list_display=['user','customer','product','quantity','ordered_date','status']

admin.site.register(OrderPlace,OrderPlaceAdmin)


class ProductImagesAdmin(admin.ModelAdmin):
    model=ProductImages
    list_display=['product','multiple_image']
admin.site.register(ProductImages,ProductImagesAdmin)

class BannerAdmin(admin.ModelAdmin):
    model=Banner
    list_display=['banner']
admin.site.register(Banner,BannerAdmin)


class CustomerAdmin(admin.ModelAdmin):
    model=Customer
    list_display=['user','name','locality','city','zipcode','state']
admin.site.register(Customer,CustomerAdmin)