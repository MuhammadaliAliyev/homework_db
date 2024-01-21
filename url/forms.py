from django import forms

class Url(forms.Form):
    url = forms.CharField(label='URL', max_length=200)