from django import forms

class FormularioUsuario(forms.Form):
    usuario_id = forms.IntegerField(label='Escribe tu id')
