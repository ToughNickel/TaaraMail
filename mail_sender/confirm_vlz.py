from django import forms


CHOICES = [('yes', 'Yes'), ('no', 'No, It`s done')]


class ConfirmFormVLZ(forms.Form):
    selection = forms.ChoiceField(label="Do you want to go back and send some more ?", choices=CHOICES,
                                  widget=forms.RadioSelect)
