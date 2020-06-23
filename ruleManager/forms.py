
from django import forms
from .models import *

class UploadFileForm(forms.Form):
    file = forms.FileField()

class CreateTag(forms.Form):
    newTag = forms.CharField(max_length=128)

