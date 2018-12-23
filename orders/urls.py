from django.urls import path
from django.contrib.auth.views import LoginView

from orders.views import index
from orders.forms import LoginForm

app_name = 'orders'

urlpatterns = [
    path("", index, name="index"),
    #path("register", views.register, name="register"),
    path("login", LoginView.as_view(authentication_form=LoginForm), name="login"),
    #path("logout", views.logout, name="logout"),
]
