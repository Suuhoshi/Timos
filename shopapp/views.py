from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import LoginForm
from .models import Category, Item


def main(request):
    categories = Category.objects.all().order_by("category_id")
    context ={
        "categories":categories
    }
    return render(request, 'main.html', context)


def search(request):
    category_id = request.GET.get("category_id")
    keyword = request.GET.get("keyword")

    items=Item.objects.all()
    category_name =""

    if category_id:
        # print('------------------------------')
        # print(category_id)
        # print(keyword)
        # print('------------------------------')
        category =Category.objects.get(category_id=category_id)
        category_name=category.name
        if category.category_id !=0:
            # print('------------------------------')
            # print(category)
            # print('------------------------------')
            items = items.filter(category=category)

    if keyword:
        items=items.filter(name__icontains=keyword)

    context={
        "items":items,
        "category_name":category_name,
        "keyword":keyword
    }
    return render(request, "searchResult.html",context)




def detail(request, item_id):
    print("---------------")
    print("item_id")
    item=Item.objects.get(item_id=item_id)
    context={
        "item_detail":item,
    }
    return render(request, "itemDetail.html", context)

# class Login(View):
#     def get(self, request):
#         form = LoginForm()
#         context = {
#             "form":form
#         }
#         return render(request, "login.html", context)
    
#     def post(self,request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data["user_id"]
#             password = form.cleaned_data["password"]

#             user=User.objects.filter(user_id=user_id, password=password).first()

#             if user:
#                  return redirect("main.html")
#             else:
#                  error="ユーザーはいません（またはパスワードが違います）"

#         context={"form":form, "error":error}
#         return render(request, "login.html", context)


# class SignupSuccess(View):
#       def get(self,request):
#             return render(request, "registerUserCommit.html")

# class Register(View):
#     def get(self, request):
#         form = SignupForm()
#         context = {
#             "form":form
#         }
#         return render(request, "signup.html", context)
    
#     def post(self, request):
#         form = SignupForm(request.POST)
#         if not form.is_valid():
#             context = {"form":form}
#             return render(request, "signup.html", context)
        
#         user = User()
#         user.name = form.cleaned_data.get("name")
#         user.password = form.cleaned_data.get("password")
#         user.save()

#         context={"name":user.name}
#         return render(request, "signup_success.html", context)

def cart(request):
    return render(request, "cart.html")