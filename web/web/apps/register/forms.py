from django import forms

class PasswordForm(forms.Form):
    password = forms.PasswordInput()