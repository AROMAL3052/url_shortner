from django import forms
from .models import urldb

class urlform(forms.ModelForm):
    class Meta:
        model = urldb
        fields = ['url','title']