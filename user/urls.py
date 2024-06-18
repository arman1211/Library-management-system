from django.urls import path,include
from . import views

urlpatterns = [
    path("register/", views.user_register,name='register'),
    path("login/", views.UserLoginView.as_view(),name='login'),
    path("logout/", views.UserLogoutView.as_view(),name='logout'),
    path("deposit/", views.deposit_money,name='deposit'),
    path("profile/", views.profile,name='profile'),
    
]