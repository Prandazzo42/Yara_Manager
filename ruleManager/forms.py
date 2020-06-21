
from django import forms

class UploadRuleForm(forms.Form):
    file = forms.FileField()

