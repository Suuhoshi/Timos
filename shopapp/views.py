from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import LoginForm
from .models import User


def index(request):
    return render(request, 'main.html')

class Login(View):
    def get(self, request):
        form = LoginForm()
        context = {
            "form":form
        }
        return render(request, "login.html", context)
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            password = form.cleaned_data["password"]

            user=User.objects.filter(user_id=user_id, password=password).first()

            if user:
                 return redirect("main.html")
            else:
                 error="ユーザーはいません（またはパスワードが違います）"

        context={"form":form, "error":error}
        return render(request, "login.html", context)


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