from django import forms
from django.contrib.auth.models import User
from .models import WynikZPost, Kandydat, Wynik


class WynikZPostForm(forms.ModelForm):

    class Meta:
        model = WynikZPost
        kandydaci = Kandydat.objects.all()
        fields = ('w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'w10', 'w11', 'w12')
