from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Model1(models.Model):
    CHOICES_AVAILABLE = [
        ('CS', 'Computer Science'),
        ('ID', 'Industrial Design'),
        ('CH', 'Chemical'),
        ('BT', 'Biotechnology'),
        ('MN', 'Mining'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    date_added = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices=CHOICES_AVAILABLE)

    def __str__(self):
        return self.name


class Subject(models.Model):
    """
    A model for representing individual subjects that belong to branches.
    """
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Model1, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name 


class Model2(models.Model):
    """
    A model representing the relationship between subjects and users.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='user_subjects')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}"
