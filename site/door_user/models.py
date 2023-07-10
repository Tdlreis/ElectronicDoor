from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_course = models.CharField(max_length=100)
    institution_code = models.IntegerField()
    authorization = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user_name
    
class Uuid(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()
    
class Rfid(models.Model):
    rfid_uid = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authorization = models.BooleanField(default=True)

class PunchCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    punch_in_time = models.DateTimeField()    
    punch_out_time = models.DateTimeField(null=True, blank=True)
    reviw =  models.BooleanField(default=False)
    out  = models.BooleanField(default=True)



