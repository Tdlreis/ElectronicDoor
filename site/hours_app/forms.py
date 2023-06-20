from django.forms import ModelForm
from hours_app.models import User


class UserForm(ModelForm):

     class Meta:
         model = User
         fields = ['user_name', 'user_course', 'year', 'rfid_num', 'authorization']