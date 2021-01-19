from django import forms

class FormularioUsuario(forms.Form):
    usuario_id = forms.IntegerField(label='Escribe tu id')

class MostSimilarFilmsForm(forms.Form):
    id = forms.IntegerField(label='Film id')
