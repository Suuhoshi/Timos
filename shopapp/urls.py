from django.urls import path
from . import views

app_name="shopapp"

urlpatterns =[
    path('', views.main, name="main"),
    path('search/', views.search, name="search"),
    path('detail/<int:item_id>/', views.detail, name="detail"),
    path('login/', views.login, name="log"),
    path('cart/', views.cart, name="cart"),
    path('register/', views.register_user, name="register_user"),
    path('register/confirm', views.register_confirm, name="register_confirm"),
    path('register/commit', views.register_commit, name="register_commit"), 
    path('userinfo/', views.user_info, name="user_info"),
    path('updateUser/', views.update_user, name='update_user'),
    path('updateUserConfirm/', views.update_user_confirm, name="update_user_confirm"),   
    path('updateUserCommit/', views.update_user_commit, name='update_user_commit'),
    path('logout/', views.logout_view, name="logout"),
    path('deleteConfirm/', views.delete_confirm, name="delete_confirm"),
    path('deleteAccount/', views.delete_account, name="delete_account"),
    #任意機能-----------------
    path('cart/delete/<int:pk>', views.cart_delete, name="cart_delete"),
    path('cart/update/<int:pk>', views.cart_update, name="cart_update"),
    path('purchase/', views.purchase, name="purchase"),
    path('purchaseConfirm/', views.purchase_confirm, name="purchase_confirm"),
    path("purchaseCommit/", views.purchase_commit, name="purchase_commit"),

]



