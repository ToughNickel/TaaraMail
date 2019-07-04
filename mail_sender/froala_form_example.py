from django import forms
from froala_editor.widgets import FroalaEditor


class ExampleFroalaForm(forms.Form):
  content = forms.Field(widget=FroalaEditor)
