from django import forms
from django.db import models

# class CategoryForm(forms.Form):    
#     category = forms.ModelChoiceField(
#         models.Category.object_by('category_id'),
#         label="カテゴリ", to_field_name="category_id", initial="0")

class LoginForm(forms.Form):
    user_id = forms.CharField(label="会員ID")
    password = forms.CharField(label="パスワード")


class UserCreatForm(forms.Form): 
    user_id = forms.CharField(label="会員ID", max_length=50)
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={"class":"form-control","aria-describedby": "passwordHelpBlock"}))
    password_confirm = forms.CharField(label="パスワード(確認)", widget=forms.PasswordInput(attrs={"class":"form-control","aria-describedby": "passwordHelpBlock"}))
    name = forms.CharField(label="お名前", max_length=255)
    address = forms.CharField(label="ご住所", max_length=1000, widget=forms.TextInput(attrs={"class":"form-control"}))

    def clean(self):
        cleaned_data=super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
