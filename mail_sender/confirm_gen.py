from django import forms


CHOICES = [('yes', 'Yes'), ('no', 'No, Get to VLZ report')]


class ConfirmForm(forms.Form):
    like = forms.ChoiceField(label="Do you want to go back to send some more ?", choices=CHOICES,
                             widget=forms.RadioSelect)
