from django.urls import path
from . import views

app_name="shopapp"

urlspatterns =[
    path('', views.index),
    # path()
]