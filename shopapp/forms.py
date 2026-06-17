from django import forms
from django.db import models
from shopapp.models import User, Category


# ログインフォーム------------------------------------

class UserForm(forms.Form):
    id = forms.CharField(label="会員ID", max_length=128)
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(render_value=False))

    def clean_id(self):
        value = self.cleaned_data["id"]
        return value
    def clean_password(self):
        value = self.cleaned_data["password"]
        return value


# 会員登録フォーム------------------------------------

class RegisterUserForm(forms.Form): 
    user_id = forms.CharField(label="会員ID", max_length=50)
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label="パスワード(確認)", widget=forms.PasswordInput(render_value=False))
    name = forms.CharField(label="お名前", max_length=128)
    address = forms.CharField(label="ご住所", max_length=1000)

    def clean(self):
        cleaned_data=super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        user_id = cleaned_data.get("user_id")
        
        errors=[]
        if password != password_confirm:
            errors.append("パスワードと確認用パスワードが一致しません")
        if User.objects.filter(user_id=user_id).exists():
            errors.append("この会員IDは使用されています")
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data
        


# 会員情報更新フォーム------------------------------------
class RegisterUpdateForm(forms.Form): 
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label="パスワード(確認)", widget=forms.PasswordInput(render_value=False))
    name = forms.CharField(label="お名前", max_length=128)
    address = forms.CharField(label="ご住所", max_length=1000)

    def clean(self):
        cleaned_data=super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        return cleaned_data


# 管理者ログインフォーム------------------------------------

class AdminForm(forms.Form):
    id = forms.CharField(label="管理者", max_length=128)
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(render_value=False))

    def clean_id(self):
        value = self.cleaned_data["id"]
        return value
    def clean_password(self):
        value = self.cleaned_data["password"]
        return value


# 商品登録・修正フォーム------------------------------------

class ItemForm(forms.Form):
    item_id = forms.IntegerField(label="商品ID")
    name = forms.CharField(label="商品名", max_length=128)
    manufacturer = forms.CharField(label="メーカー名", max_length=32)
    color = forms.CharField(label="商品の色", max_length=16)
    price = forms.IntegerField(label="価格")
    stock = forms.IntegerField(label="在庫数")
    recommended = forms.BooleanField(label="オススメ", required=False)
    category = forms.ModelChoiceField(label="カテゴリ", queryset=Category.objects.all())