from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django import forms


class EmailComponent(forms.Form):
    content = forms.CharField(widget=SummernoteWidget)
