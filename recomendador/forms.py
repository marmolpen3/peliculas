from django import forms

class UserForm(forms.Form):
    id = forms.IntegerField(label='Your id')