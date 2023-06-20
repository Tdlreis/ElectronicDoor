from django.db import models


class User(models.Model):

    user_name = models.CharField(max_length=100)
    user_course = models.CharField(max_length=100)
    year = models.IntegerField()
    rfid_num = models.CharField(max_length=100)
    authorization = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user_name


class Punch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    punch_time = models.DateTimeField()
    is_in = models.BooleanField()


class HoursWorked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)



