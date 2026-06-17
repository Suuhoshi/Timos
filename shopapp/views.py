from django.shortcuts import render, redirect
# from django.views.generic import View
from .forms import UserForm, RegisterUserForm, RegisterUpdateForm, AdminForm, ItemForm
from .models import Category, Item, User, Itemsincart, Purchase, Admin
from django.contrib.auth import logout


#ランディングページ追加------------------------
def landing(request):
    return render(request, 'landing.html')
#ランディングページ追加------------------------



def main(request):
    name = request.session.get('name')
    categories = Category.objects.all().order_by("category_id")
    context ={
        "categories":categories,
        "name":name,
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
        "item":item,
        "range":range(1,item.stock+1)
    }
    return render(request, "itemDetail.html", context)



def login(request):
    if request.session.get('is_login', None):
        print("test")
        # return render(request, 'main.html', locals())
        return redirect('/shopapp/')
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
                name = user.name
                # context = {"name":name}
                request.session["name"]=name
                return redirect('/shopapp/')
                # return render(request, 'main.html', locals())
            else:
                message ='パスワードが正しくありません。'
                return render(request, "login.html", locals())
        else:
            return render(request, "login.html", locals())
    login_form = UserForm()
    return render(request, "login.html", locals())



def cart(request):
    if "user_id" not in request.session:
        return redirect("/shopapp/login")

    if request.method == "POST":
        item_id=request.POST.get("item_id")
        item = Item.objects.get(item_id=item_id)

        user_id=request.session["user_id"]
        user = User.objects.get(user_id=user_id)
        
        amount = request.POST.get("amount")

        cart = Itemsincart(item=item, user=user, amount=amount)
        cart.save()

    #カート一覧取得---------------------
    user = User.objects.get(user_id=request.session["user_id"])
    cart_list = (Itemsincart.objects.filter(user=user))
    
    total = 0
    for cart in cart_list:
        total += cart.item.price*cart.amount

    error = request.session.pop("error",None)
    context = {
        "cart_list":cart_list,
        "total":total,
        "error":error,
        }
    return render(request, "cart.html", context)



def register_user(request):
    form = RegisterUserForm()
    context = {
        "form":form,
    }
    return render(request, "registerUser.html", context)



def register_confirm(request):
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        context ={"form":form,
                  }
        return render(request, "registerUserConfirm.html", context)

    context={
        "form":form,
        "errors":form.errors
    }
    return render(request, "registerUser.html", context)



def register_commit(request):
    user = User(
        user_id=request.POST["user_id"],
        password=request.POST["password"],
        name=request.POST["name"],
        address=request.POST["address"],
        )

    user.save()
    context={
        "user":user
    }
    return render(request, "registerUserCommit.html", context)



def user_info(request):
    user_id=request.session["user_id"]
    user = User.objects.get(user_id=user_id)
    context={
        "user":user,
    }
    return render(request, "userInfo.html", context)




def update_user(request):
    user_id = request.session['user_id']
    print("userid=" + str(user_id))
    user = User.objects.get(user_id=user_id)
    form = RegisterUpdateForm(initial={
        "user_id":user.user_id,
        "name":user.name,
        "address":user.address,
    })
    context ={
        "user":user,
        "form":form,
    }
    return render(request, "updateUser.html", context)



def update_user_confirm(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    form = RegisterUpdateForm(request.POST)
    if form.is_valid():
        context ={"form":form,
                  "user":user,
                  }
        return render(request, "updateUserConfirm.html", context)

    context={
        "form":form,
        "errors":form.errors,
        "user":user,
    }
    return render(request, "updateUser.html", context)




def update_user_commit(request):
    if request.method == 'POST':
        user_id=request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        user.password = request.POST['password']
        user.name = request.POST['name']
        user.address = request.POST['address']

        user.save()
        context={
            "user":user,
        }
    return render(request, 'updateUserCommit.html', context)



def logout_view(request):
    logout(request)
    return redirect("/shopapp/")



def delete_confirm(request):
    user_id=request.session["user_id"]
    user = User.objects.get(user_id=user_id)
    name = user.name
    context ={
        "name":name
    }
    return render(request, "withdrawConfirm.html", context)



def delete_account(request):
    if request.method == "POST":
        user_id=request.session["user_id"]
        user = User.objects.get(user_id=user_id)
        name = user.name
        context ={
            "name":name
        }
        logout(request)
        user.delete()
        return render(request, "withdrawCommit.html", context)
    


#任意機能----------------------------
def cart_delete(request, pk):
    if request.method == "POST":
        item = Itemsincart.objects.get(pk=pk)
        item.delete()
    return redirect("/shopapp/cart/")


def cart_update(request, pk):
    if request.method == "POST":
        cart = Itemsincart.objects.get(pk=pk)
        new_amount = int(request.POST.get("new_amount"))

        same_items = Itemsincart.objects.filter(user=cart.user, item=cart.item)
        total_amount = 0
        for row in same_items:
            total_amount += row.amount
        total_amount -= cart.amount
        total_amount += new_amount
        if total_amount > cart.item.stock:
            request.session["error"] = (f"{cart.item.name}の在庫数を超えています")
            return redirect("/shopapp/cart/")

        cart.amount = new_amount
        cart.save()
    return redirect("/shopapp/cart/")
# def cart_update(request, pk):
#     if request.method == "POST":
#         cart = Itemsincart.objects.get(pk=pk)
#         new_amount = int(request.POST.get("new_amount"))
#         # item.amount = int(new_amount)
#         # if new_amount > cart.item.stock:
#         #     request.session["error"]=("在庫数をこえています")
#         #     return redirect("/shopapp/cart/")
#         cart.amount =new_amount
#         cart.save()
#     return redirect("/shopapp/cart/")




def purchase(request):
    user = User.objects.get(user_id=request.session["user_id"])
    context = {
        "user": user
    }
    return render(request, "purchase.html", context)



def purchase_confirm(request):
    destination = request.POST["destination"]
    cash = request.POST["cash"]
    user_id=request.session["user_id"]
    user = User.objects.get(user_id=user_id)
    cart_list = Itemsincart.objects.filter(user=user)

    total = 0
    for cart in cart_list:
        total += (cart.item.price*cart.amount)

    context = {
        "user": user,
        "destination": destination,
        "cash":cash,
        "cart_list": cart_list,
        "total": total,
    }
    return render(request, "purchase_confirm.html", context)



def purchase_commit(request):
    user_id=request.session["user_id"]
    user = User.objects.get(user_id=user_id)

    destination = request.POST["destination"]

    cart_list = Itemsincart.objects.filter(user=user)

    for cart in cart_list:
        total_amount = 0
        same_items = Itemsincart.objects.filter(user=user,item=cart.item)

        for row in same_items:
            total_amount += row.amount

        if total_amount > cart.item.stock:

            context = {"error":f"{cart.item.item_name}の在庫が不足しています",
                "user": user,
                "destination": destination,
                "cart_list": cart_list,}
            return render(request,"purchase_confirm.html",context)
        
    purchase = Purchase()
    purchase.destination = destination
    purchase.user = user
    purchase.cancel = False
    purchase.save()


    cart_list = Itemsincart.objects.filter(user=user)

    for cart in cart_list:
        item = cart.item
        item.stock -= cart.amount
        item.save()


    Itemsincart.objects.filter(user_id=user_id).delete()
    name=user.name
    context ={
        "name":name
    }
    return render(request, "purchase_commit.html", context)
  
#管理者機能----------------------------
def admin_login(request):
    if request.session.get('is_admin_login', None):
        return redirect('/shopapp/admin/')
    if request.method == 'POST':
        admin_form = AdminForm(request.POST)
        message = "入力した内容を再度確認してください"

        if admin_form.is_valid():
            admin_id = admin_form.cleaned_data.get("id")
            password = admin_form.cleaned_data.get("password")
            try:
                admin = Admin.objects.get(admin_id=admin_id)
            except:
                message = "管理者が存在しません"
                return render(request, "adminLogin.html", locals())

            if admin.password == password:
                request.session['is_admin_login'] = True
                request.session['admin_id'] = admin.admin_id
                return redirect('/shopapp/admin/')
            else:
                message = 'パスワードが正しくありません。'
                return render(request, "adminLogin.html", locals())
        else:
            return render(request, "adminLogin.html", locals())
    admin_form = AdminForm()
    return render(request, "adminLogin.html", locals())


def admin_main(request):
    if not request.session.get('is_admin_login'):
        return redirect('/shopapp/admin/login/')

    # 商品の検索
    category_id = request.GET.get("category_id")
    keyword = request.GET.get("keyword")

    items = Item.objects.all().order_by("item_id")
    if category_id and category_id != "0":
        items = items.filter(category__category_id=category_id)
    if keyword:
        items = items.filter(name__icontains=keyword)
    else:
        keyword

    # 購入の履歴検索
    user_id = request.GET.get("user_id")
    purchase_id = request.GET.get("purchase_id")

    purchases = Purchase.objects.all().order_by("purchase_id")
    if user_id:
        purchases = purchases.filter(user__user_id__icontains=user_id)
    if purchase_id:
        purchases = purchases.filter(purchase_id=purchase_id)

    categories = Category.objects.all().order_by("category_id")

    context = {
        "admin_id": request.session.get('admin_id'),
        "items": items,
        "purchases": purchases,
        "categories": categories,
        "register_form": ItemForm(),
        "category_id": category_id,
        "keyword": keyword or "",
        "user_id": user_id,
        "purchase_id": purchase_id or "",
    }
    return render(request, "adminMain.html", context)


def admin_logout(request):
    request.session.pop('is_admin_login', None)
    request.session.pop('admin_id', None)
    return redirect("/shopapp/admin/login/")


def admin_item_register(request):
    if not request.session.get('is_admin_login'):
        return redirect('/shopapp/admin/login/')

    if request.method == "POST":
        form = ItemForm(request.POST)
        register_errors = None

        if form.is_valid():
            item_id = form.cleaned_data.get("item_id")
            if Item.objects.filter(item_id=item_id).exists():
                register_errors = "この商品IDは既に使用されています"
            else:
                item = Item(
                    item_id=item_id,
                    name=form.cleaned_data.get("name"),
                    manufacturer=form.cleaned_data.get("manufacturer"),
                    color=form.cleaned_data.get("color"),
                    price=form.cleaned_data.get("price"),
                    stock=form.cleaned_data.get("stock"),
                    recommended=form.cleaned_data.get("recommended"),
                    category=form.cleaned_data.get("category"),
                )
                item.save()
                return redirect("/shopapp/admin/")
        else:
            register_errors = form.errors

        context = {
            "admin_id": request.session.get('admin_id'),
            "items": Item.objects.all().order_by("item_id"),
            "purchases": Purchase.objects.all().order_by("purchase_id"),
            "categories": Category.objects.all().order_by("category_id"),
            "register_form": form,
            "register_errors": register_errors,
        }
        return render(request, "adminMain.html", context)

    return redirect("/shopapp/admin/")


def admin_item_update(request, item_id):
    if not request.session.get('is_admin_login'):
        return redirect('/shopapp/admin/login/')

    if request.method == "POST":
        item = Item.objects.get(item_id=item_id)
        form = ItemForm(request.POST)
        if form.is_valid():
            item.name = form.cleaned_data.get("name")
            item.manufacturer = form.cleaned_data.get("manufacturer")
            item.color = form.cleaned_data.get("color")
            item.price = form.cleaned_data.get("price")
            item.stock = form.cleaned_data.get("stock")
            item.recommended = form.cleaned_data.get("recommended")
            item.category = form.cleaned_data.get("category")
            item.save()
    return redirect("/shopapp/admin/")


def admin_item_delete(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(item_id=item_id)
        item.delete()
    return redirect("/shopapp/admin/")


def admin_purchase_cancel(request, purchase_id):
    if request.method == "POST":
        purchase = Purchase.objects.get(purchase_id=purchase_id)
        purchase.cancel = True
        purchase.save()
    return redirect("/shopapp/admin/")
