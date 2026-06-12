from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserForm
from .models import Category, Item, User


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
        category =Category.objects.get(category_id=category_id)
        category_name=category.name
        if category.category_id !=0:
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
    item=Item.objects.get(item_id=item_id)
    context={
        "item_detail":item,
        "range":range(1,item.stock+1)
    }
    return render(request, "itemDetail.html", context)



def login(request):
    if request.session.get('is_login', None):
        print("test")
        return render(request, 'main.html', locals())
        # return redirect('/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = "入力した内容を再度確認してください"

        if login_form.is_valid():
            user_id = login_form.cleaned_data.get("id")
            password = login_form.cleaned_data.get("password")
            try:
                user = User.objects.get(user_id=user_id)
            except:
                message = "ユーザが存在しません"
                return render(request, "login.html", locals())
            
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.user_id
                return redirect('shopapp:main')
            else:
                message ='パスワードが正しくありません。'
                return render(request, "shopapp/login.html", locals())
        else:
            return render(request, "login.html", locals())
    login_form = UserForm()
    return render(request, "login.html", locals())




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