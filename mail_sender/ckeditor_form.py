from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import Form, CharField


class EmailComponent(Form):
    content = CharField(widget=CKEditorUploadingWidget())
