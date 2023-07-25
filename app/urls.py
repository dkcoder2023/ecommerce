from django.urls import path
from app import views



urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:id>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.ShowCartView.as_view(), name='cart'),
    path('pluscart/', views.PlusCartView.as_view(),name="pluscart"),
    path('minuscart/', views.MinusCartView.as_view(),name="minuscart"),
    path('removecart/', views.RemoveCartView.as_view(),name="removecart"),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),

    path('product/',views.SingleCatProductView.as_view(), name='product'),
    path('product/<slug:data>/',views.SingleCatProductView.as_view(), name='productdata'),

    path('login/', views.login_attempt, name='login'),
    path("logout", views.logout_request, name='logout'),
    path('register/' ,views.register , name="register"),
    path('otp/' , views.otp , name="otp"),
    path('login-otp/', views.login_otp , name="login_otp"),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    # path('faltu/', views.faltu_function, name='faltu_function'),
 
    path('delete/<int:id>/', views.delete_cust_detail, name='delete'),

]
