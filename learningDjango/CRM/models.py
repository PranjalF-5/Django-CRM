from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now  # Use timezone-aware now

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        # Use timezone-aware `now`
        return now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp}"



#Record Model


class Record(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
