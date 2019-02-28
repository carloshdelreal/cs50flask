from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from orders.views import index, profile, menu, cart, register, succesfullyordered, customizeorder, myorders, pendingorders
from orders.forms import LoginForm

app_name = 'orders'

urlpatterns = [
    path("", index, name="index"),
    path("profile", profile, name="profile"),
    path("menu", menu, name="menu"),
    path("customizeorder", customizeorder, name="customizeorder"),
    path("cart", cart, name="cart"),
    path("successfully_ordered", succesfullyordered, name='succesfullyordered'),
    path("myorders", myorders, name="myorders"),
    path("pendingorders", pendingorders, name="pendingorders"),
    #path("register", views.register, name="register"),
    path("login", LoginView.as_view(authentication_form=LoginForm), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", register, name='register' )
]
