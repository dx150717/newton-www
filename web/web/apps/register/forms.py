from django import forms

class PasswordForm(forms.Form):
    password = forms.PasswordInput()
    repassword = forms.PasswordInput()

class EmailForm(forms.Form):
    email = forms.EmailField()