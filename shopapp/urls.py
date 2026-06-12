from django.urls import path
from . import views

app_name="shopapp"

urlpatterns =[
    path('', views.main, name="main"),
    path('search/', views.search, name="search"),
    path('detail/<int:item_id>/', views.detail, name="detail"),
    path('login/', views.login, name="login"),
    path('cart/', views.cart, name="hoge"),
    # path('signup_success', views.SignupSuccess.as_view(), name="signup_success"),
    # path('', views.register, name="M02"),
    # path('', views. ,name="")
    # path('' ,views.index),
]