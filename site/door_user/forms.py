from django import forms
from .models import User, Rfid

class UserForm(forms.ModelForm):
    # user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'name-2', 'name': 'user_name', 'placeholder': 'Nome'}))
    # user_course = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'name-1', 'name': 'user_course', 'placeholder': 'Curso'}))
    institution_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'name': 'institution_code', 'pattern': '[0-9]+', 'title': 'Only numeric characters are allowed.'}))
    # authorization = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'formCheck-2'}), required=False)
    class Meta:
        model = User
        fields = ['user_name', 'user_course', 'institution_code', 'authorization']

class RfidForm(forms.ModelForm):
    # rfid_uid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), required=False)
    # # authorization = forms.CharField(widget=forms.TextInput(attrs={'type': 'checkbox'}), required=False)
    rfid_uid = forms.CharField(label="")
    authorization = forms.BooleanField(label="", required=False)
    class Meta:
        model = Rfid
        fields = ["rfid_uid", "authorization"]