from django import forms

class UserForm(forms.Form):
    id = forms.IntegerField(label='Your id')

class MostSimilarFilmsForm(forms.Form):
    id = forms.IntegerField(label='Film id')