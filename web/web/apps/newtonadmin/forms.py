from django import forms

class KycForm(forms.Form):
    first_name = forms.CharField(label="first_name", max_length=100)
    last_name = forms.CharField(label="last_name", max_length=100)
    country = forms.CharField(label="country", max_length=100)
    location = forms.CharField(label="location", max_length=100)
    country_code = forms.CharField(label="country_code", max_length=100)
    cellphone = forms.CharField(label="cellphone", max_length=100)
    email = forms.EmailField(label="email",required=True)
    id_card = forms.FileField(label="id_card")
    investment_btc = forms.IntegerField(label="investment_btc")
    investment_ela = forms.IntegerField(label="investment_ela")
    how_to_contribute = forms.Textarea()
    what_is_newton = forms.Textarea()
    
