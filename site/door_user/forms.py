from django import forms
from .models import User, Rfid

class UserForm(forms.ModelForm):
    institution_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'name': 'institution_code', 'pattern': '[0-9]+', 'title': 'Only numeric characters are allowed.'}))
    authorization = forms.BooleanField(required=False, initial=True)
    class Meta:
        model = User
        fields = ['user_name', 'user_course', 'institution_code', 'authorization']

class RfidForm(forms.ModelForm):
    rfid_uid = forms.CharField(label="")
    authorization = forms.BooleanField(label="", required=False, initial=True)
    class Meta:
        model = Rfid
        fields = ["rfid_uid", "authorization"]