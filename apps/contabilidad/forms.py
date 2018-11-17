from django import forms

from .models import *

class TransaccionForm(forms.ModelForm):

    class Meta:
        model = Transaccion
        
