from django import forms
from froala_editor.widgets import FroalaEditor
import os
from TaaraMail.settings import MEDIA_ROOT


class ExampleFroalaForm(forms.Form):
  content = forms.CharField(widget=FroalaEditor(options={
    'placeholderText': "Email Body",
  }))
